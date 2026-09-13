import { Router, Request, Response } from 'express';
import { z } from 'zod';
import { merchantAuth } from '../middleware/auth';
import { TransactionService } from '../../services/transaction.service';

const router = Router();

// POST /transactions/charge — Create a card charge
const chargeSchema = z.object({
  amount: z.number().int().positive(), // in cents
  currency: z.string().length(3).optional(),
  card: z.object({
    number: z.string().min(13).max(19),
    expMonth: z.number().int().min(1).max(12),
    expYear: z.number().int().min(2024),
    cvv: z.string().min(3).max(4),
    billingAddress: z.object({
      line1: z.string(),
      line2: z.string().optional(),
      city: z.string(),
      state: z.string(),
      postalCode: z.string(),
      country: z.string().length(2),
    }).optional(),
  }).optional(),
  token: z.string().optional(),
  customerEmail: z.string().email().optional(),
  customerId: z.string().optional(),
  orderId: z.string().optional(),
  description: z.string().optional(),
  metadata: z.record(z.any()).optional(),
});

router.post(
  '/charge',
  merchantAuth('transactions.create'),
  async (req: Request, res: Response) => {
    const input = chargeSchema.parse(req.body);
    const result = await TransactionService.charge(req.merchant!.id, {
      ...input,
      ipAddress: req.ip,
      userAgent: req.headers['user-agent'],
    });
    res.status(201).json(result);
  }
);

// POST /transactions/:id/refund — Refund a transaction
const refundSchema = z.object({
  amount: z.number().int().positive().optional(),
  reason: z.string().optional(),
});

router.post(
  '/:id/refund',
  merchantAuth('refunds.create'),
  async (req: Request, res: Response) => {
    const input = refundSchema.parse(req.body);
    const result = await TransactionService.refund(req.merchant!.id, req.params.id, input);
    res.status(201).json(result);
  }
);

// GET /transactions/:id — Get a transaction
router.get(
  '/:id',
  merchantAuth('transactions.read'),
  async (req: Request, res: Response) => {
    const txn = await TransactionService.getByExternalId(req.merchant!.id, req.params.id);
    res.json({ transaction: txn });
  }
);

// GET /transactions — List transactions
router.get(
  '/',
  merchantAuth('transactions.read'),
  async (req: Request, res: Response) => {
    const result = await TransactionService.list(req.merchant!.id, {
      status: req.query.status as string,
      type: req.query.type as string,
      startDate: req.query.start_date ? new Date(req.query.start_date as string) : undefined,
      endDate: req.query.end_date ? new Date(req.query.end_date as string) : undefined,
      page: req.query.page ? parseInt(req.query.page as string) : undefined,
      limit: req.query.limit ? parseInt(req.query.limit as string) : undefined,
    });
    res.json(result);
  }
);

export default router;
