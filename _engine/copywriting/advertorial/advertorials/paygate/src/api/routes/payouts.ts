import { Router, Request, Response } from 'express';
import { z } from 'zod';
import { merchantAuth } from '../middleware/auth';
import { PayoutService } from '../../services/payout.service';

const router = Router();

// GET /payouts/balance — Get available balance
router.get(
  '/balance',
  merchantAuth('payouts.read'),
  async (req: Request, res: Response) => {
    const balance = await PayoutService.getAvailableBalance(req.merchant!.id);
    res.json({ balance });
  }
);

// POST /payouts — Create a payout
const createPayoutSchema = z.object({
  amount: z.number().positive().optional(),
  bankAccountId: z.string().optional(),
});

router.post(
  '/',
  merchantAuth('payouts.read'), // payouts.create could be a separate permission
  async (req: Request, res: Response) => {
    const input = createPayoutSchema.parse(req.body);
    const payout = await PayoutService.create(req.merchant!.id, input);
    res.status(201).json({ payout });
  }
);

// GET /payouts — List payouts
router.get(
  '/',
  merchantAuth('payouts.read'),
  async (req: Request, res: Response) => {
    const result = await PayoutService.list(req.merchant!.id, {
      status: req.query.status as string,
      page: req.query.page ? parseInt(req.query.page as string) : undefined,
      limit: req.query.limit ? parseInt(req.query.limit as string) : undefined,
    });
    res.json(result);
  }
);

export default router;
