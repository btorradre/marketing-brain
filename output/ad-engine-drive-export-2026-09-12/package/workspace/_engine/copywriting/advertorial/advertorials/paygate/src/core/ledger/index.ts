/**
 * Double-Entry Ledger System
 *
 * Every dollar that moves through PayGate is tracked with double-entry
 * bookkeeping. Every transaction creates TWO ledger entries: a debit
 * and a credit, which must always balance.
 *
 * Chart of Accounts:
 * ─────────────────────────────────────────────
 * 1000  Cash (Settlement)      ASSET      Money held from processors
 * 1001  ACH Receivable         ASSET      Pending ACH debits
 * 1002  Processor Receivable   ASSET      Money owed by processor
 * 2000  Merchant Payable       LIABILITY  Money owed to merchants
 * 2001  Refund Payable         LIABILITY  Pending refunds
 * 2002  Dispute Reserve        LIABILITY  Held for disputes
 * 3000  Processing Revenue     REVENUE    Our processing fees
 * 3001  Monthly Fees           REVENUE    Monthly subscription fees
 * 4000  Processor Costs        EXPENSE    Fees we pay to processors
 * 4001  Chargeback Losses      EXPENSE    Lost chargebacks
 */

import { prisma } from '../../config/database';
import { logger } from '../../config/logger';
import { Prisma } from '@prisma/client';

// Standard account codes
export const ACCOUNTS = {
  CASH: '1000',
  ACH_RECEIVABLE: '1001',
  PROCESSOR_RECEIVABLE: '1002',
  MERCHANT_PAYABLE: '2000',
  REFUND_PAYABLE: '2001',
  DISPUTE_RESERVE: '2002',
  PROCESSING_REVENUE: '3000',
  MONTHLY_FEES: '3001',
  PROCESSOR_COSTS: '4000',
  CHARGEBACK_LOSSES: '4001',
} as const;

export class Ledger {
  /**
   * Initialize the chart of accounts.
   * Run this once on first setup.
   */
  static async initializeAccounts() {
    const accounts = [
      { code: '1000', name: 'Cash (Settlement)', type: 'ASSET' as const },
      { code: '1001', name: 'ACH Receivable', type: 'ASSET' as const },
      { code: '1002', name: 'Processor Receivable', type: 'ASSET' as const },
      { code: '2000', name: 'Merchant Payable', type: 'LIABILITY' as const },
      { code: '2001', name: 'Refund Payable', type: 'LIABILITY' as const },
      { code: '2002', name: 'Dispute Reserve', type: 'LIABILITY' as const },
      { code: '3000', name: 'Processing Revenue', type: 'REVENUE' as const },
      { code: '3001', name: 'Monthly Fees Revenue', type: 'REVENUE' as const },
      { code: '4000', name: 'Processor Costs', type: 'EXPENSE' as const },
      { code: '4001', name: 'Chargeback Losses', type: 'EXPENSE' as const },
    ];

    for (const acct of accounts) {
      await prisma.ledgerAccount.upsert({
        where: { code: acct.code },
        update: {},
        create: acct,
      });
    }

    logger.info('Ledger accounts initialized');
  }

  /**
   * Record a card charge.
   *
   * When a merchant charges a customer's card:
   *   Debit  1002 Processor Receivable  (money coming from processor)
   *   Credit 2000 Merchant Payable      (we owe merchant the net amount)
   *   Credit 3000 Processing Revenue    (our fee)
   */
  static async recordCharge(params: {
    transactionId: string;
    merchantId: string;
    amount: Prisma.Decimal;
    fee: Prisma.Decimal;
  }) {
    const { transactionId, merchantId, amount, fee } = params;
    const netAmount = amount.sub(fee);

    const [receivableAcct, payableAcct, revenueAcct] = await Promise.all([
      prisma.ledgerAccount.findUniqueOrThrow({ where: { code: ACCOUNTS.PROCESSOR_RECEIVABLE } }),
      prisma.ledgerAccount.findUniqueOrThrow({ where: { code: ACCOUNTS.MERCHANT_PAYABLE } }),
      prisma.ledgerAccount.findUniqueOrThrow({ where: { code: ACCOUNTS.PROCESSING_REVENUE } }),
    ]);

    await prisma.$transaction([
      // Gross amount: processor owes us
      prisma.ledgerEntry.create({
        data: {
          transactionId,
          merchantId,
          debitAccountId: receivableAcct.id,
          creditAccountId: payableAcct.id,
          amount: netAmount,
          description: `Charge - merchant net`,
        },
      }),
      // Fee: our revenue
      prisma.ledgerEntry.create({
        data: {
          transactionId,
          merchantId,
          debitAccountId: receivableAcct.id,
          creditAccountId: revenueAcct.id,
          amount: fee,
          description: `Processing fee`,
        },
      }),
      // Update account balances
      prisma.ledgerAccount.update({
        where: { code: ACCOUNTS.PROCESSOR_RECEIVABLE },
        data: { balance: { increment: amount } },
      }),
      prisma.ledgerAccount.update({
        where: { code: ACCOUNTS.MERCHANT_PAYABLE },
        data: { balance: { increment: netAmount } },
      }),
      prisma.ledgerAccount.update({
        where: { code: ACCOUNTS.PROCESSING_REVENUE },
        data: { balance: { increment: fee } },
      }),
    ]);

    logger.debug('Ledger: recorded charge', { transactionId, amount: amount.toString(), fee: fee.toString() });
  }

  /**
   * Record a refund.
   *
   *   Debit  2000 Merchant Payable      (reduce what we owe merchant)
   *   Credit 1002 Processor Receivable  (reduce what processor owes us)
   *
   * Note: We typically don't refund our fee, but can be configured.
   */
  static async recordRefund(params: {
    transactionId: string;
    merchantId: string;
    amount: Prisma.Decimal;
    refundFee: boolean;
    originalFee: Prisma.Decimal;
  }) {
    const { transactionId, merchantId, amount, refundFee, originalFee } = params;

    const [payableAcct, receivableAcct, revenueAcct] = await Promise.all([
      prisma.ledgerAccount.findUniqueOrThrow({ where: { code: ACCOUNTS.MERCHANT_PAYABLE } }),
      prisma.ledgerAccount.findUniqueOrThrow({ where: { code: ACCOUNTS.PROCESSOR_RECEIVABLE } }),
      prisma.ledgerAccount.findUniqueOrThrow({ where: { code: ACCOUNTS.PROCESSING_REVENUE } }),
    ]);

    const entries: any[] = [
      // Reverse the net amount from merchant payable
      prisma.ledgerEntry.create({
        data: {
          transactionId,
          merchantId,
          debitAccountId: payableAcct.id,
          creditAccountId: receivableAcct.id,
          amount,
          description: `Refund`,
        },
      }),
      prisma.ledgerAccount.update({
        where: { code: ACCOUNTS.MERCHANT_PAYABLE },
        data: { balance: { decrement: amount } },
      }),
      prisma.ledgerAccount.update({
        where: { code: ACCOUNTS.PROCESSOR_RECEIVABLE },
        data: { balance: { decrement: amount } },
      }),
    ];

    if (refundFee) {
      entries.push(
        prisma.ledgerEntry.create({
          data: {
            transactionId,
            merchantId,
            debitAccountId: revenueAcct.id,
            creditAccountId: receivableAcct.id,
            amount: originalFee,
            description: `Fee refund`,
          },
        }),
        prisma.ledgerAccount.update({
          where: { code: ACCOUNTS.PROCESSING_REVENUE },
          data: { balance: { decrement: originalFee } },
        })
      );
    }

    await prisma.$transaction(entries);

    logger.debug('Ledger: recorded refund', { transactionId, amount: amount.toString() });
  }

  /**
   * Record a payout to merchant.
   *
   *   Debit  2000 Merchant Payable   (reduce what we owe)
   *   Credit 1000 Cash               (money leaving our account)
   */
  static async recordPayout(params: {
    payoutId: string;
    merchantId: string;
    amount: Prisma.Decimal;
  }) {
    const { payoutId, merchantId, amount } = params;

    const [payableAcct, cashAcct] = await Promise.all([
      prisma.ledgerAccount.findUniqueOrThrow({ where: { code: ACCOUNTS.MERCHANT_PAYABLE } }),
      prisma.ledgerAccount.findUniqueOrThrow({ where: { code: ACCOUNTS.CASH } }),
    ]);

    await prisma.$transaction([
      prisma.ledgerEntry.create({
        data: {
          payoutId,
          merchantId,
          debitAccountId: payableAcct.id,
          creditAccountId: cashAcct.id,
          amount,
          description: `Payout to merchant`,
        },
      }),
      prisma.ledgerAccount.update({
        where: { code: ACCOUNTS.MERCHANT_PAYABLE },
        data: { balance: { decrement: amount } },
      }),
      prisma.ledgerAccount.update({
        where: { code: ACCOUNTS.CASH },
        data: { balance: { decrement: amount } },
      }),
    ]);

    logger.debug('Ledger: recorded payout', { payoutId, amount: amount.toString() });
  }

  /**
   * Record settlement from processor (money hitting our bank).
   *
   *   Debit  1000 Cash                   (money arriving)
   *   Credit 1002 Processor Receivable   (processor paid what they owed)
   */
  static async recordSettlement(params: {
    amount: Prisma.Decimal;
    reference: string;
  }) {
    const { amount, reference } = params;

    const [cashAcct, receivableAcct] = await Promise.all([
      prisma.ledgerAccount.findUniqueOrThrow({ where: { code: ACCOUNTS.CASH } }),
      prisma.ledgerAccount.findUniqueOrThrow({ where: { code: ACCOUNTS.PROCESSOR_RECEIVABLE } }),
    ]);

    await prisma.$transaction([
      prisma.ledgerEntry.create({
        data: {
          debitAccountId: cashAcct.id,
          creditAccountId: receivableAcct.id,
          amount,
          description: `Settlement received`,
          reference,
        },
      }),
      prisma.ledgerAccount.update({
        where: { code: ACCOUNTS.CASH },
        data: { balance: { increment: amount } },
      }),
      prisma.ledgerAccount.update({
        where: { code: ACCOUNTS.PROCESSOR_RECEIVABLE },
        data: { balance: { decrement: amount } },
      }),
    ]);

    logger.debug('Ledger: recorded settlement', { amount: amount.toString(), reference });
  }

  /**
   * Get current balances for all accounts.
   */
  static async getBalances() {
    return prisma.ledgerAccount.findMany({
      orderBy: { code: 'asc' },
      select: { code: true, name: true, type: true, balance: true },
    });
  }

  /**
   * Verify the ledger balances (debits must equal credits).
   * Returns true if balanced.
   */
  static async verify(): Promise<{ balanced: boolean; totalDebits: string; totalCredits: string }> {
    const result = await prisma.ledgerEntry.aggregate({
      _sum: { amount: true },
      _count: true,
    });

    // In double-entry, every entry has a debit and credit side,
    // so we check that assets + expenses = liabilities + revenue
    const accounts = await prisma.ledgerAccount.findMany();

    let assetsAndExpenses = new Prisma.Decimal(0);
    let liabilitiesAndRevenue = new Prisma.Decimal(0);

    for (const acct of accounts) {
      if (acct.type === 'ASSET' || acct.type === 'EXPENSE') {
        assetsAndExpenses = assetsAndExpenses.add(acct.balance);
      } else {
        liabilitiesAndRevenue = liabilitiesAndRevenue.add(acct.balance);
      }
    }

    return {
      balanced: assetsAndExpenses.equals(liabilitiesAndRevenue),
      totalDebits: assetsAndExpenses.toString(),
      totalCredits: liabilitiesAndRevenue.toString(),
    };
  }
}
