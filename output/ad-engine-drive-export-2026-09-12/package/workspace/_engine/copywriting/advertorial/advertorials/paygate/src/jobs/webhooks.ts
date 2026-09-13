/**
 * Webhook Delivery Job
 *
 * Processes pending webhook events and retries failed ones.
 * Runs continuously or on a frequent schedule (every 10 seconds).
 */

import { prisma } from '../config/database';
import { WebhookService } from '../services/webhook.service';
import { logger } from '../config/logger';

export async function deliverWebhooks() {
  // Get pending events
  const pendingEvents = await prisma.webhookEvent.findMany({
    where: { status: 'PENDING' },
    orderBy: { createdAt: 'asc' },
    take: 100,
  });

  // Get events due for retry
  const retryEvents = await prisma.webhookEvent.findMany({
    where: {
      status: 'RETRYING',
      nextRetryAt: { lte: new Date() },
    },
    orderBy: { nextRetryAt: 'asc' },
    take: 50,
  });

  const events = [...pendingEvents, ...retryEvents];

  if (events.length === 0) return;

  logger.debug(`Delivering ${events.length} webhook events`);

  // Process in parallel (max 10 concurrent)
  const CONCURRENCY = 10;
  for (let i = 0; i < events.length; i += CONCURRENCY) {
    const batch = events.slice(i, i + CONCURRENCY);
    await Promise.allSettled(
      batch.map((event) => WebhookService.deliver(event.id))
    );
  }
}

// Run as a continuous loop if called directly
if (require.main === module) {
  const INTERVAL = 10_000; // 10 seconds

  async function loop() {
    while (true) {
      try {
        await deliverWebhooks();
      } catch (error: any) {
        logger.error('Webhook delivery error', { error: error.message });
      }
      await new Promise((resolve) => setTimeout(resolve, INTERVAL));
    }
  }

  logger.info('Webhook delivery worker started');
  loop().catch((err) => {
    logger.error('Webhook worker crashed', { error: err.message });
    process.exit(1);
  });
}
