/**
 * Payout Processing Job
 *
 * Runs on a schedule (e.g., daily at 6 AM) to process pending payouts.
 * Batches all pending payouts into a single NACHA file for efficiency.
 */

import { prisma } from '../config/database';
import { PayoutService } from '../services/payout.service';
import { logger } from '../config/logger';

export async function processPayouts() {
  logger.info('Starting payout processing job');

  const pendingPayouts = await prisma.payout.findMany({
    where: { status: 'PENDING' },
    orderBy: { createdAt: 'asc' },
    take: 500, // process in batches of 500
  });

  if (pendingPayouts.length === 0) {
    logger.info('No pending payouts to process');
    return;
  }

  logger.info(`Processing ${pendingPayouts.length} payouts`);

  let successCount = 0;
  let failCount = 0;

  for (const payout of pendingPayouts) {
    try {
      await PayoutService.process(payout.id);
      successCount++;
    } catch (error: any) {
      failCount++;
      logger.error('Failed to process payout', { payoutId: payout.id, error: error.message });
    }
  }

  logger.info('Payout processing complete', { total: pendingPayouts.length, success: successCount, failed: failCount });
}

// Run directly if called as a script
if (require.main === module) {
  processPayouts()
    .then(() => process.exit(0))
    .catch((err) => {
      logger.error('Payout job failed', { error: err.message });
      process.exit(1);
    });
}
