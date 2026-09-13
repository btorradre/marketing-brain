import { prisma } from '../config/database';
import { AppError } from '../api/middleware/errorHandler';
import { processors } from '../core/processors';
import { Ledger } from '../core/ledger';
import { WebhookService } from './webhook.service';
import { decrypt } from '../utils/encryption';
import { logger } from '../config/logger';
import { Prisma } from '@prisma/client';

export class PayoutService {
  /**
   * Calculate available balance for a merchant.
   * Available = settled transactions net amounts - already paid out - pending payouts.
   */
  static async getAvailableBalance(merchantId: string) {
    const [settled, paidOut, pending] = await Promise.all([
      // Total net from settled transactions
      prisma.transaction.aggregate({
        where: {
          merchantId,
          type: 'CHARGE',
          status: { in: ['CAPTURED', 'SETTLED'] },
        },
        _sum: { netAmount: true },
      }),
      // Already paid out
      prisma.payout.aggregate({
        where: {
          merchantId,
          status: { in: ['COMPLETED', 'SUBMITTED', 'PROCESSING'] },
        },
        _sum: { amount: true },
      }),
      // Pending payouts
      prisma.payout.aggregate({
        where: { merchantId, status: 'PENDING' },
        _sum: { amount: true },
      }),
    ]);

    // Subtract refunds
    const refunds = await prisma.transaction.aggregate({
      where: {
        merchantId,
        type: 'REFUND',
        status: { not: 'FAILED' },
      },
      _sum: { amount: true },
    });

    const totalSettled = Number(settled._sum.netAmount || 0);
    const totalPaidOut = Number(paidOut._sum.amount || 0);
    const totalPending = Number(pending._sum.amount || 0);
    const totalRefunds = Number(refunds._sum.amount || 0);

    const available = totalSettled - totalPaidOut - totalPending - totalRefunds;

    return {
      settled: totalSettled,
      paidOut: totalPaidOut,
      pending: totalPending,
      refunds: totalRefunds,
      available: Math.max(0, available),
    };
  }

  /**
   * Create a payout to a merchant's bank account.
   */
  static async create(merchantId: string, input?: { amount?: number; bankAccountId?: string }) {
    // Get merchant
    const merchant = await prisma.merchant.findUniqueOrThrow({ where: { id: merchantId } });

    if (merchant.status !== 'ACTIVE') {
      throw new AppError(400, 'merchant_inactive', 'Cannot create payout for inactive merchant');
    }

    // Get bank account
    let bankAccountId = input?.bankAccountId;
    if (!bankAccountId) {
      const primaryAccount = await prisma.merchantBankAccount.findFirst({
        where: { merchantId, isPrimary: true, verified: true },
      });
      if (!primaryAccount) {
        throw new AppError(400, 'no_bank_account', 'No verified primary bank account');
      }
      bankAccountId = primaryAccount.id;
    }

    const bankAccount = await prisma.merchantBankAccount.findUniqueOrThrow({
      where: { id: bankAccountId },
    });

    if (!bankAccount.verified) {
      throw new AppError(400, 'unverified_account', 'Bank account not verified');
    }

    // Calculate amount
    const balance = await this.getAvailableBalance(merchantId);
    const payoutAmount = input?.amount || balance.available;

    if (payoutAmount <= 0) {
      throw new AppError(400, 'no_balance', 'No available balance for payout');
    }

    if (payoutAmount > balance.available) {
      throw new AppError(400, 'insufficient_balance', `Available balance is $${balance.available.toFixed(2)}`);
    }

    if (payoutAmount < Number(merchant.payoutMinimum)) {
      throw new AppError(400, 'below_minimum', `Minimum payout is $${merchant.payoutMinimum}`);
    }

    // Calculate period
    const lastPayout = await prisma.payout.findFirst({
      where: { merchantId, status: { in: ['COMPLETED', 'SUBMITTED'] } },
      orderBy: { periodEnd: 'desc' },
    });

    const periodStart = lastPayout?.periodEnd || merchant.createdAt;
    const periodEnd = new Date();

    // Create payout record
    const payout = await prisma.payout.create({
      data: {
        merchantId,
        bankAccountId,
        amount: payoutAmount,
        status: 'PENDING',
        periodStart,
        periodEnd,
      },
    });

    logger.info('Payout created', { payoutId: payout.id, merchantId, amount: payoutAmount });

    return {
      id: payout.externalId,
      amount: payoutAmount,
      status: 'pending',
      periodStart,
      periodEnd,
      createdAt: payout.createdAt,
    };
  }

  /**
   * Process a pending payout via ACH.
   * Called by the payout background job.
   */
  static async process(payoutId: string) {
    const payout = await prisma.payout.findUniqueOrThrow({
      where: { id: payoutId },
      include: { bankAccount: true, merchant: true },
    });

    if (payout.status !== 'PENDING') {
      throw new AppError(400, 'invalid_status', `Payout is ${payout.status}`);
    }

    // Update to processing
    await prisma.payout.update({
      where: { id: payoutId },
      data: { status: 'PROCESSING' },
    });

    try {
      // Decrypt bank details
      const routingNumber = decrypt(payout.bankAccount.routingNumber);
      const accountNumber = decrypt(payout.bankAccount.accountNumber);

      // Send via ACH
      const achProcessor = processors.getAchProcessor();
      const result = await achProcessor.credit({
        amount: Math.round(Number(payout.amount) * 100), // convert to cents
        routingNumber,
        accountNumber,
        accountType: payout.bankAccount.accountType as 'checking' | 'savings',
        accountHolderName: payout.merchant.businessName,
        companyEntryDescription: 'PAYOUT',
        addenda: `PayGate payout ${payout.externalId}`,
      });

      if (result.success) {
        await prisma.payout.update({
          where: { id: payoutId },
          data: {
            status: 'SUBMITTED',
            achBatchId: result.batchId,
            achTraceNumber: result.traceNumber,
            expectedArrival: new Date(Date.now() + 2 * 24 * 60 * 60 * 1000), // T+2
          },
        });

        // Record in ledger
        await Ledger.recordPayout({
          payoutId: payout.id,
          merchantId: payout.merchantId,
          amount: payout.amount,
        });

        // Webhook
        await WebhookService.emit(payout.merchantId, 'payout.submitted', {
          id: payout.externalId,
          amount: Number(payout.amount) * 100,
          status: 'submitted',
          expectedArrival: new Date(Date.now() + 2 * 24 * 60 * 60 * 1000),
        });

        logger.info('Payout submitted via ACH', { payoutId, traceNumber: result.traceNumber });
      } else {
        await prisma.payout.update({
          where: { id: payoutId },
          data: { status: 'FAILED', failureReason: result.responseMessage },
        });

        logger.error('Payout failed', { payoutId, reason: result.responseMessage });
      }
    } catch (error: any) {
      await prisma.payout.update({
        where: { id: payoutId },
        data: { status: 'FAILED', failureReason: error.message },
      });

      logger.error('Payout processing error', { payoutId, error: error.message });
    }
  }

  /**
   * List payouts for a merchant.
   */
  static async list(merchantId: string, params: {
    status?: string;
    page?: number;
    limit?: number;
  }) {
    const { status, page = 1, limit = 20 } = params;
    const skip = (page - 1) * limit;

    const where: any = { merchantId };
    if (status) where.status = status;

    const [payouts, total] = await Promise.all([
      prisma.payout.findMany({
        where,
        skip,
        take: limit,
        orderBy: { createdAt: 'desc' },
        select: {
          externalId: true, amount: true, status: true,
          periodStart: true, periodEnd: true, expectedArrival: true,
          completedAt: true, createdAt: true,
        },
      }),
      prisma.payout.count({ where }),
    ]);

    return { payouts, total, page, limit, pages: Math.ceil(total / limit) };
  }
}
