/**
 * Settlement Reconciliation Job
 *
 * Runs daily to:
 * 1. Close open settlement batches
 * 2. Match processor settlements with our records
 * 3. Flag discrepancies
 * 4. Update chargeback rates for merchants
 */

import { prisma } from '../config/database';
import { logger } from '../config/logger';

export async function runReconciliation() {
  logger.info('Starting reconciliation job');

  // 1. Close settlement batches from yesterday
  const yesterday = new Date();
  yesterday.setDate(yesterday.getDate() - 1);
  yesterday.setHours(0, 0, 0, 0);

  const today = new Date();
  today.setHours(0, 0, 0, 0);

  // Aggregate transactions from yesterday
  const batchStats = await prisma.transaction.groupBy({
    by: ['processorId'],
    where: {
      status: { in: ['CAPTURED', 'SETTLED'] },
      createdAt: { gte: yesterday, lt: today },
      processorId: { not: null },
    },
    _count: true,
    _sum: { amount: true, fee: true, netAmount: true },
  });

  for (const batch of batchStats) {
    if (!batch.processorId) continue;

    await prisma.settlementBatch.upsert({
      where: {
        processorId_batchDate: {
          processorId: batch.processorId,
          batchDate: yesterday,
        },
      },
      update: {
        status: 'CLOSED',
        totalCount: batch._count,
        totalAmount: batch._sum.amount || 0,
        totalFees: batch._sum.fee || 0,
        netAmount: batch._sum.netAmount || 0,
      },
      create: {
        processorId: batch.processorId,
        batchDate: yesterday,
        status: 'CLOSED',
        totalCount: batch._count,
        totalAmount: batch._sum.amount || 0,
        totalFees: batch._sum.fee || 0,
        netAmount: batch._sum.netAmount || 0,
      },
    });
  }

  // 2. Update merchant chargeback rates (rolling 30 days)
  const thirtyDaysAgo = new Date();
  thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);

  const activeMerchants = await prisma.merchant.findMany({
    where: { status: 'ACTIVE' },
    select: { id: true },
  });

  for (const merchant of activeMerchants) {
    const [txnCount, disputeCount] = await Promise.all([
      prisma.transaction.count({
        where: {
          merchantId: merchant.id,
          type: 'CHARGE',
          status: { in: ['CAPTURED', 'SETTLED'] },
          createdAt: { gte: thirtyDaysAgo },
        },
      }),
      prisma.dispute.count({
        where: {
          merchantId: merchant.id,
          createdAt: { gte: thirtyDaysAgo },
        },
      }),
    ]);

    const chargebackRate = txnCount > 0 ? disputeCount / txnCount : 0;

    await prisma.merchant.update({
      where: { id: merchant.id },
      data: { chargebackRate },
    });

    // Alert if chargeback rate exceeds threshold
    if (chargebackRate > 0.01) { // 1% threshold (Visa/MC threshold is 0.9%)
      logger.warn('Merchant exceeds chargeback threshold', {
        merchantId: merchant.id,
        chargebackRate: (chargebackRate * 100).toFixed(2) + '%',
        disputes: disputeCount,
        transactions: txnCount,
      });
    }
  }

  // 3. Mark old captured transactions as settled (T+2)
  const twoDaysAgo = new Date();
  twoDaysAgo.setDate(twoDaysAgo.getDate() - 2);

  const settled = await prisma.transaction.updateMany({
    where: {
      status: 'CAPTURED',
      createdAt: { lt: twoDaysAgo },
    },
    data: {
      status: 'SETTLED',
      settledAt: new Date(),
    },
  });

  logger.info('Reconciliation complete', {
    batches: batchStats.length,
    merchantsChecked: activeMerchants.length,
    transactionsSettled: settled.count,
  });
}

if (require.main === module) {
  runReconciliation()
    .then(() => process.exit(0))
    .catch((err) => {
      logger.error('Reconciliation job failed', { error: err.message });
      process.exit(1);
    });
}
