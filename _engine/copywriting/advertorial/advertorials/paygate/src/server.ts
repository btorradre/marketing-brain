import app from './app';
import { config } from './config';
import { prisma } from './config/database';
import { redis } from './config/redis';
import { processors } from './core/processors';
import { logger } from './config/logger';
import cron from 'node-cron';
import { processPayouts } from './jobs/payouts';
import { deliverWebhooks } from './jobs/webhooks';
import { runReconciliation } from './jobs/reconciliation';

async function main() {
  // Initialize processor connections
  processors.initialize();

  // Verify database connection
  await prisma.$connect();
  logger.info('Connected to PostgreSQL');

  // Schedule background jobs
  // Process payouts at 6 AM daily
  cron.schedule('0 6 * * *', async () => {
    try {
      await processPayouts();
    } catch (err: any) {
      logger.error('Scheduled payout job failed', { error: err.message });
    }
  });

  // Run reconciliation at 2 AM daily
  cron.schedule('0 2 * * *', async () => {
    try {
      await runReconciliation();
    } catch (err: any) {
      logger.error('Scheduled reconciliation job failed', { error: err.message });
    }
  });

  // Deliver webhooks every 10 seconds
  setInterval(async () => {
    try {
      await deliverWebhooks();
    } catch (err: any) {
      logger.error('Webhook delivery error', { error: err.message });
    }
  }, 10_000);

  // Start server
  app.listen(config.port, () => {
    logger.info(`PayGate server running on port ${config.port}`);
    logger.info(`Environment: ${config.nodeEnv}`);
    logger.info(`API: http://localhost:${config.port}/api/${config.apiVersion}`);

    const procs = processors.listProcessors();
    logger.info(`Card processors: ${procs.card.length > 0 ? procs.card.join(', ') : 'NONE'}`);
    logger.info(`ACH processor: ${procs.ach ? 'Active' : 'NONE'}`);
  });
}

// Graceful shutdown
process.on('SIGTERM', async () => {
  logger.info('SIGTERM received, shutting down...');
  await prisma.$disconnect();
  redis.disconnect();
  process.exit(0);
});

process.on('SIGINT', async () => {
  logger.info('SIGINT received, shutting down...');
  await prisma.$disconnect();
  redis.disconnect();
  process.exit(0);
});

main().catch((err) => {
  logger.error('Failed to start server', { error: err.message, stack: err.stack });
  process.exit(1);
});
