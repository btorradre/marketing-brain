import { prisma } from '../config/database';
import { AppError } from '../api/middleware/errorHandler';
import { processors } from '../core/processors';
import { FraudEngine } from '../core/fraud';
import { Ledger } from '../core/ledger';
import { WebhookService } from './webhook.service';
import { encrypt } from '../utils/encryption';
import { logger } from '../config/logger';
import { Prisma, TransactionStatus } from '@prisma/client';
import crypto from 'crypto';

export interface ChargeInput {
  amount: number;       // in cents
  currency?: string;
  card?: {
    number: string;
    expMonth: number;
    expYear: number;
    cvv: string;
    billingAddress?: {
      line1: string;
      line2?: string;
      city: string;
      state: string;
      postalCode: string;
      country: string;
    };
  };
  token?: string;        // previously tokenized card
  customerEmail?: string;
  customerId?: string;
  orderId?: string;
  description?: string;
  metadata?: Record<string, any>;
  ipAddress?: string;
  userAgent?: string;
}

export class TransactionService {
  /**
   * Process a card charge (authorize + capture in one step).
   */
  static async charge(merchantId: string, input: ChargeInput) {
    // Validate
    if (input.amount <= 0) throw new AppError(400, 'invalid_amount', 'Amount must be positive');
    if (input.amount > 99999999) throw new AppError(400, 'amount_too_large', 'Amount exceeds maximum');
    if (!input.card && !input.token) throw new AppError(400, 'missing_payment', 'Card or token required');

    // Get merchant config
    const merchant = await prisma.merchant.findUniqueOrThrow({ where: { id: merchantId } });

    // Calculate fee
    const feeBps = merchant.cardRateBps; // e.g., 250 = 2.50%
    const feeFixed = merchant.cardFixedCents; // e.g., 25 = $0.25
    const feeAmount = Math.round((input.amount * feeBps) / 10000) + feeFixed;
    const netAmount = input.amount - feeAmount;

    // Card fingerprint for fraud checks
    let cardFingerprint: string | undefined;
    let cardBin: string | undefined;
    if (input.card) {
      const num = input.card.number.replace(/\D/g, '');
      cardFingerprint = crypto.createHash('sha256').update(num).digest('hex').slice(0, 16);
      cardBin = num.slice(0, 6);
    }

    // Fraud check
    const fraudResult = await FraudEngine.check({
      merchantId,
      amount: input.amount,
      cardFingerprint,
      cardBin,
      customerEmail: input.customerEmail,
      ipAddress: input.ipAddress,
      userAgent: input.userAgent,
    });

    if (fraudResult.action === 'block') {
      // Create a declined transaction record
      const txn = await prisma.transaction.create({
        data: {
          merchantId,
          type: 'CHARGE',
          status: 'DECLINED',
          paymentMethod: 'CARD',
          amount: input.amount / 100,
          currency: input.currency || 'USD',
          fee: feeAmount / 100,
          netAmount: netAmount / 100,
          cardLast4: input.card ? input.card.number.slice(-4) : undefined,
          cardBrand: input.card ? processors.getCardProcessor().detectBrand(input.card.number) : undefined,
          cardFingerprint,
          fraudScore: fraudResult.score,
          fraudFlags: fraudResult.flags,
          ipAddress: input.ipAddress,
          userAgent: input.userAgent,
          customerEmail: input.customerEmail,
          customerId: input.customerId,
          orderId: input.orderId,
          description: input.description,
          metadata: input.metadata,
          processorMsg: 'Declined by fraud detection',
        },
      });

      logger.warn('Transaction blocked by fraud engine', { txnId: txn.id, score: fraudResult.score });

      return {
        id: txn.externalId,
        status: 'declined',
        declineReason: 'Transaction flagged for fraud',
        fraudScore: fraudResult.score,
      };
    }

    // Process with card processor
    const processor = processors.getCardProcessor();
    const processorResult = await processor.charge({
      amount: input.amount,
      currency: input.currency || 'USD',
      card: input.card,
      token: input.token,
      orderId: input.orderId,
      customerEmail: input.customerEmail,
      ipAddress: input.ipAddress,
    });

    // Determine status
    let status: TransactionStatus = processorResult.success ? 'CAPTURED' : 'DECLINED';

    // Create transaction record
    const txn = await prisma.transaction.create({
      data: {
        merchantId,
        type: 'CHARGE',
        status,
        paymentMethod: 'CARD',
        amount: input.amount / 100,
        currency: input.currency || 'USD',
        fee: feeAmount / 100,
        netAmount: netAmount / 100,
        cardBrand: input.card ? processor.detectBrand(input.card.number) : undefined,
        cardLast4: input.card ? input.card.number.slice(-4) : undefined,
        cardExpMonth: input.card?.expMonth,
        cardExpYear: input.card?.expYear,
        cardToken: input.token,
        cardFingerprint,
        processorId: processor.id,
        processorTxnId: processorResult.transactionId,
        processorCode: processorResult.responseCode,
        processorMsg: processorResult.responseMessage,
        authCode: processorResult.authCode,
        avsResult: processorResult.avsResult,
        cvvResult: processorResult.cvvResult,
        fraudScore: fraudResult.score,
        fraudFlags: fraudResult.flags,
        ipAddress: input.ipAddress,
        userAgent: input.userAgent,
        customerEmail: input.customerEmail,
        customerId: input.customerId,
        orderId: input.orderId,
        description: input.description,
        metadata: input.metadata,
      },
    });

    // If successful, record in ledger
    if (processorResult.success) {
      await Ledger.recordCharge({
        transactionId: txn.id,
        merchantId,
        amount: new Prisma.Decimal(input.amount / 100),
        fee: new Prisma.Decimal(feeAmount / 100),
      });

      // Fire webhook
      await WebhookService.emit(merchantId, 'transaction.completed', {
        id: txn.externalId,
        type: 'charge',
        status: 'captured',
        amount: input.amount,
        currency: input.currency || 'USD',
        cardBrand: txn.cardBrand,
        cardLast4: txn.cardLast4,
        createdAt: txn.createdAt,
      }, txn.id);
    }

    logger.info('Transaction processed', {
      txnId: txn.id,
      status,
      amount: input.amount / 100,
      processorId: processor.id,
    });

    return {
      id: txn.externalId,
      status: status.toLowerCase(),
      amount: input.amount,
      currency: input.currency || 'USD',
      fee: feeAmount,
      netAmount,
      cardBrand: txn.cardBrand,
      cardLast4: txn.cardLast4,
      authCode: processorResult.authCode,
      processorResponse: processorResult.responseMessage,
      fraudScore: fraudResult.action === 'review' ? fraudResult.score : undefined,
      createdAt: txn.createdAt,
    };
  }

  /**
   * Refund a transaction (full or partial).
   */
  static async refund(merchantId: string, transactionExternalId: string, input: {
    amount?: number; // cents, omit for full refund
    reason?: string;
  }) {
    const original = await prisma.transaction.findFirst({
      where: { externalId: transactionExternalId, merchantId },
    });

    if (!original) throw new AppError(404, 'not_found', 'Transaction not found');
    if (!['CAPTURED', 'SETTLED'].includes(original.status)) {
      throw new AppError(400, 'invalid_status', `Cannot refund a ${original.status.toLowerCase()} transaction`);
    }

    const refundAmountCents = input.amount || Math.round(Number(original.amount) * 100);
    const originalAmountCents = Math.round(Number(original.amount) * 100);

    // Check for over-refund
    const existingRefunds = await prisma.transaction.aggregate({
      where: { parentTxnId: original.id, type: 'REFUND', status: { not: 'FAILED' } },
      _sum: { amount: true },
    });
    const totalRefunded = Math.round(Number(existingRefunds._sum.amount || 0) * 100);

    if (totalRefunded + refundAmountCents > originalAmountCents) {
      throw new AppError(400, 'over_refund', 'Refund amount exceeds original transaction');
    }

    // Process refund with processor
    const processor = processors.getCardProcessor(original.processorId || undefined);
    const result = await processor.refund({
      transactionId: original.processorTxnId!,
      amount: refundAmountCents,
      reason: input.reason,
    });

    const status: TransactionStatus = result.success ? 'REFUNDED' : 'FAILED';

    const refundTxn = await prisma.transaction.create({
      data: {
        merchantId,
        type: 'REFUND',
        status,
        paymentMethod: original.paymentMethod,
        amount: refundAmountCents / 100,
        currency: original.currency,
        fee: 0,
        netAmount: refundAmountCents / 100,
        cardBrand: original.cardBrand,
        cardLast4: original.cardLast4,
        cardFingerprint: original.cardFingerprint,
        processorId: original.processorId,
        processorTxnId: result.transactionId,
        processorCode: result.responseCode,
        processorMsg: result.responseMessage,
        parentTxnId: original.id,
        description: input.reason || 'Refund',
        customerEmail: original.customerEmail,
      },
    });

    // Update original transaction status
    if (result.success) {
      const newTotalRefunded = totalRefunded + refundAmountCents;
      const newStatus: TransactionStatus = newTotalRefunded >= originalAmountCents
        ? 'REFUNDED'
        : 'PARTIALLY_REFUNDED';

      await prisma.transaction.update({
        where: { id: original.id },
        data: { status: newStatus },
      });

      // Record in ledger
      await Ledger.recordRefund({
        transactionId: refundTxn.id,
        merchantId,
        amount: new Prisma.Decimal(refundAmountCents / 100),
        refundFee: false,
        originalFee: original.fee,
      });

      // Webhook
      await WebhookService.emit(merchantId, 'transaction.refunded', {
        id: refundTxn.externalId,
        originalTransactionId: original.externalId,
        amount: refundAmountCents,
        reason: input.reason,
      }, refundTxn.id);
    }

    return {
      id: refundTxn.externalId,
      originalTransactionId: original.externalId,
      status: status.toLowerCase(),
      amount: refundAmountCents,
      createdAt: refundTxn.createdAt,
    };
  }

  /**
   * Get transaction by external ID.
   */
  static async getByExternalId(merchantId: string, externalId: string) {
    const txn = await prisma.transaction.findFirst({
      where: { externalId, merchantId },
      include: {
        childTxns: {
          select: { externalId: true, type: true, status: true, amount: true, createdAt: true },
        },
        disputes: {
          select: { externalId: true, status: true, reason: true, amount: true },
        },
      },
    });

    if (!txn) throw new AppError(404, 'not_found', 'Transaction not found');
    return txn;
  }

  /**
   * List transactions for a merchant.
   */
  static async list(merchantId: string, params: {
    status?: string;
    type?: string;
    startDate?: Date;
    endDate?: Date;
    page?: number;
    limit?: number;
  }) {
    const { status, type, startDate, endDate, page = 1, limit = 20 } = params;
    const skip = (page - 1) * limit;

    const where: any = { merchantId };
    if (status) where.status = status;
    if (type) where.type = type;
    if (startDate || endDate) {
      where.createdAt = {};
      if (startDate) where.createdAt.gte = startDate;
      if (endDate) where.createdAt.lte = endDate;
    }

    const [transactions, total] = await Promise.all([
      prisma.transaction.findMany({
        where,
        skip,
        take: limit,
        orderBy: { createdAt: 'desc' },
        select: {
          externalId: true, type: true, status: true, paymentMethod: true,
          amount: true, currency: true, fee: true, netAmount: true,
          cardBrand: true, cardLast4: true, customerEmail: true,
          orderId: true, createdAt: true,
        },
      }),
      prisma.transaction.count({ where }),
    ]);

    return { transactions, total, page, limit, pages: Math.ceil(total / limit) };
  }
}
