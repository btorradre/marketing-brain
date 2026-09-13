import { Router, Request, Response } from 'express';
import { z } from 'zod';
import { merchantAuth } from '../middleware/auth';
import { WebhookService } from '../../services/webhook.service';

const router = Router();

const VALID_EVENTS = [
  'transaction.completed',
  'transaction.declined',
  'transaction.refunded',
  'transaction.disputed',
  'payout.submitted',
  'payout.completed',
  'payout.failed',
  'dispute.opened',
  'dispute.won',
  'dispute.lost',
];

// POST /webhooks/endpoints — Create webhook endpoint
const createEndpointSchema = z.object({
  url: z.string().url(),
  events: z.array(z.enum(VALID_EVENTS as [string, ...string[]])).min(1),
});

router.post(
  '/endpoints',
  merchantAuth('webhooks.manage'),
  async (req: Request, res: Response) => {
    const input = createEndpointSchema.parse(req.body);
    const endpoint = await WebhookService.createEndpoint(req.merchant!.id, input);
    res.status(201).json({ endpoint });
  }
);

// GET /webhooks/endpoints — List webhook endpoints
router.get(
  '/endpoints',
  merchantAuth('webhooks.manage'),
  async (req: Request, res: Response) => {
    const endpoints = await WebhookService.listEndpoints(req.merchant!.id);
    res.json({ endpoints });
  }
);

// GET /webhooks/endpoints/:id/events — List recent events for an endpoint
router.get(
  '/endpoints/:id/events',
  merchantAuth('webhooks.manage'),
  async (req: Request, res: Response) => {
    const events = await WebhookService.listEvents(req.params.id);
    res.json({ events });
  }
);

export default router;
