import { prisma } from '../config/database';
import { signWebhookPayload, generateWebhookSecret } from '../utils/encryption';
import { logger } from '../config/logger';
import { config } from '../config';

export class WebhookService {
  /**
   * Register a webhook endpoint for a merchant.
   */
  static async createEndpoint(merchantId: string, input: {
    url: string;
    events: string[];
  }) {
    const secret = generateWebhookSecret();

    const endpoint = await prisma.webhookEndpoint.create({
      data: {
        merchantId,
        url: input.url,
        secret,
        events: input.events,
        active: true,
      },
    });

    return {
      id: endpoint.id,
      url: endpoint.url,
      events: endpoint.events,
      secret, // Only returned at creation
      active: endpoint.active,
    };
  }

  /**
   * Emit a webhook event to all matching endpoints for a merchant.
   */
  static async emit(
    merchantId: string,
    eventType: string,
    payload: Record<string, any>,
    transactionId?: string
  ) {
    // Find all active endpoints subscribed to this event
    const endpoints = await prisma.webhookEndpoint.findMany({
      where: {
        merchantId,
        active: true,
        events: { has: eventType },
      },
    });

    if (endpoints.length === 0) return;

    const eventPayload = {
      event: eventType,
      data: payload,
      createdAt: new Date().toISOString(),
    };

    // Create webhook events for each endpoint
    for (const endpoint of endpoints) {
      await prisma.webhookEvent.create({
        data: {
          endpointId: endpoint.id,
          transactionId,
          eventType,
          payload: eventPayload,
          status: 'PENDING',
        },
      });
    }

    logger.debug('Webhook events queued', { merchantId, eventType, endpoints: endpoints.length });
  }

  /**
   * Deliver a single webhook event. Called by the webhook delivery job.
   */
  static async deliver(eventId: string) {
    const event = await prisma.webhookEvent.findUniqueOrThrow({
      where: { id: eventId },
      include: { endpoint: true },
    });

    if (event.status === 'DELIVERED') return;
    if (event.attempts >= event.maxAttempts) {
      await prisma.webhookEvent.update({
        where: { id: eventId },
        data: { status: 'FAILED' },
      });
      return;
    }

    const payloadStr = JSON.stringify(event.payload);
    const signature = signWebhookPayload(payloadStr, event.endpoint.secret);

    try {
      const response = await fetch(event.endpoint.url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-PayGate-Signature': signature,
          'X-PayGate-Event': event.eventType,
          'User-Agent': 'PayGate-Webhook/1.0',
        },
        body: payloadStr,
        signal: AbortSignal.timeout(10000), // 10s timeout
      });

      const httpStatus = response.status;

      if (httpStatus >= 200 && httpStatus < 300) {
        await prisma.webhookEvent.update({
          where: { id: eventId },
          data: {
            status: 'DELIVERED',
            httpStatus,
            attempts: { increment: 1 },
            lastAttemptAt: new Date(),
            deliveredAt: new Date(),
          },
        });
        logger.debug('Webhook delivered', { eventId, url: event.endpoint.url });
      } else {
        throw new Error(`HTTP ${httpStatus}`);
      }
    } catch (error: any) {
      const attempts = event.attempts + 1;
      const retryDelays = config.webhook.retryDelays;
      const nextRetry = attempts < retryDelays.length
        ? new Date(Date.now() + retryDelays[attempts] * 1000)
        : null;

      await prisma.webhookEvent.update({
        where: { id: eventId },
        data: {
          status: nextRetry ? 'RETRYING' : 'FAILED',
          attempts,
          lastAttemptAt: new Date(),
          lastError: error.message,
          nextRetryAt: nextRetry,
        },
      });

      logger.warn('Webhook delivery failed', {
        eventId,
        url: event.endpoint.url,
        error: error.message,
        attempt: attempts,
        nextRetry: nextRetry?.toISOString(),
      });
    }
  }

  /**
   * List webhook endpoints for a merchant.
   */
  static async listEndpoints(merchantId: string) {
    return prisma.webhookEndpoint.findMany({
      where: { merchantId },
      select: {
        id: true, url: true, events: true, active: true, createdAt: true,
        _count: { select: { webhookEvents: true } },
      },
    });
  }

  /**
   * List recent webhook events for a merchant endpoint.
   */
  static async listEvents(endpointId: string, limit = 20) {
    return prisma.webhookEvent.findMany({
      where: { endpointId },
      orderBy: { createdAt: 'desc' },
      take: limit,
      select: {
        id: true, eventType: true, status: true, httpStatus: true,
        attempts: true, lastError: true, createdAt: true, deliveredAt: true,
      },
    });
  }
}
