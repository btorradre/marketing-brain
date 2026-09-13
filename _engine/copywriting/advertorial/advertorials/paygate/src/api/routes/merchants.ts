import { Router, Request, Response } from 'express';
import { z } from 'zod';
import { merchantAuth } from '../middleware/auth';
import { MerchantService } from '../../services/merchant.service';

const router = Router();

// All routes require merchant auth
router.use(merchantAuth());

// GET /merchants/me — Get current merchant info
router.get('/me', async (req: Request, res: Response) => {
  const merchant = await MerchantService.getByExternalId(req.merchant!.externalId);
  res.json({ merchant });
});

// GET /merchants/me/dashboard — Get dashboard stats
router.get('/me/dashboard', async (req: Request, res: Response) => {
  const stats = await MerchantService.getDashboardStats(req.merchant!.id);
  res.json(stats);
});

// POST /merchants/me/bank-accounts — Add bank account
const addBankAccountSchema = z.object({
  accountName: z.string().min(1),
  routingNumber: z.string().length(9),
  accountNumber: z.string().min(4).max(17),
  accountType: z.enum(['checking', 'savings']).optional(),
});

router.post('/me/bank-accounts', async (req: Request, res: Response) => {
  const input = addBankAccountSchema.parse(req.body);
  const account = await MerchantService.addBankAccount(req.merchant!.id, input);
  res.status(201).json({ bankAccount: account });
});

export default router;
