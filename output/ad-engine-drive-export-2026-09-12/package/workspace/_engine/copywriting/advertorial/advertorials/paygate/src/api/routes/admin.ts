import { Router, Request, Response } from 'express';
import { z } from 'zod';
import bcrypt from 'bcrypt';
import jwt from 'jsonwebtoken';
import { prisma } from '../../config/database';
import { config } from '../../config';
import { adminAuth } from '../middleware/auth';
import { MerchantService } from '../../services/merchant.service';
import { PayoutService } from '../../services/payout.service';
import { Ledger } from '../../core/ledger';
import { AppError } from '../middleware/errorHandler';

const router = Router();

// POST /admin/login — Admin login
const loginSchema = z.object({
  email: z.string().email(),
  password: z.string().min(1),
});

router.post('/login', async (req: Request, res: Response) => {
  const { email, password } = loginSchema.parse(req.body);

  const admin = await prisma.adminUser.findUnique({ where: { email } });
  if (!admin || !admin.active) {
    throw new AppError(401, 'invalid_credentials', 'Invalid email or password');
  }

  const validPassword = await bcrypt.compare(password, admin.password);
  if (!validPassword) {
    throw new AppError(401, 'invalid_credentials', 'Invalid email or password');
  }

  // Update last login
  await prisma.adminUser.update({ where: { id: admin.id }, data: { lastLoginAt: new Date() } });

  const token = jwt.sign(
    { sub: admin.id, email: admin.email, role: admin.role },
    config.jwt.secret,
    { expiresIn: config.jwt.expiresIn }
  );

  res.json({ token, admin: { id: admin.id, email: admin.email, role: admin.role } });
});

// --- Protected admin routes ---

// POST /admin/merchants — Create a new merchant (admin onboarding)
const createMerchantSchema = z.object({
  email: z.string().email(),
  businessName: z.string().min(1),
  businessType: z.string().optional(),
  legalName: z.string().optional(),
  taxId: z.string().optional(),
  website: z.string().optional(),
  phone: z.string().optional(),
  addressLine1: z.string().optional(),
  city: z.string().optional(),
  state: z.string().optional(),
  postalCode: z.string().optional(),
  country: z.string().optional(),
  mcc: z.string().optional(),
  monthlyVolume: z.number().optional(),
  averageTicket: z.number().optional(),
  owners: z.array(z.object({
    firstName: z.string(),
    lastName: z.string(),
    email: z.string().email().optional(),
    dateOfBirth: z.string().optional(),
    ssn: z.string().optional(),
    title: z.string().optional(),
    ownershipPct: z.number().optional(),
  })).optional(),
});

router.post(
  '/merchants',
  adminAuth(['SUPER_ADMIN', 'ADMIN']),
  async (req: Request, res: Response) => {
    const input = createMerchantSchema.parse(req.body);
    const result = await MerchantService.create(input);

    // Audit log
    await prisma.auditLog.create({
      data: {
        adminUserId: req.admin!.id,
        merchantId: result.merchant.id,
        action: 'merchant.created',
        resource: 'merchant',
        resourceId: result.merchant.id,
        ipAddress: req.ip,
      },
    });

    res.status(201).json(result);
  }
);

// GET /admin/merchants — List all merchants
router.get(
  '/merchants',
  adminAuth(),
  async (req: Request, res: Response) => {
    const result = await MerchantService.list({
      status: req.query.status as string,
      search: req.query.search as string,
      page: req.query.page ? parseInt(req.query.page as string) : undefined,
      limit: req.query.limit ? parseInt(req.query.limit as string) : undefined,
    });
    res.json(result);
  }
);

// GET /admin/merchants/:id — Get merchant details
router.get(
  '/merchants/:id',
  adminAuth(),
  async (req: Request, res: Response) => {
    const merchant = await MerchantService.getByExternalId(req.params.id);
    const balance = await PayoutService.getAvailableBalance(merchant.id);
    res.json({ merchant, balance });
  }
);

// POST /admin/merchants/:id/approve — Approve merchant
router.post(
  '/merchants/:id/approve',
  adminAuth(['SUPER_ADMIN', 'ADMIN']),
  async (req: Request, res: Response) => {
    const merchant = await prisma.merchant.findFirst({ where: { externalId: req.params.id } });
    if (!merchant) throw new AppError(404, 'not_found', 'Merchant not found');

    const result = await MerchantService.approve(merchant.id);

    await prisma.auditLog.create({
      data: {
        adminUserId: req.admin!.id,
        merchantId: merchant.id,
        action: 'merchant.approved',
        resource: 'merchant',
        resourceId: merchant.id,
        ipAddress: req.ip,
      },
    });

    res.json({ merchant: result });
  }
);

// POST /admin/merchants/:id/suspend — Suspend merchant
router.post(
  '/merchants/:id/suspend',
  adminAuth(['SUPER_ADMIN', 'ADMIN']),
  async (req: Request, res: Response) => {
    const { reason } = z.object({ reason: z.string().min(1) }).parse(req.body);
    const merchant = await prisma.merchant.findFirst({ where: { externalId: req.params.id } });
    if (!merchant) throw new AppError(404, 'not_found', 'Merchant not found');

    const result = await MerchantService.suspend(merchant.id, reason);

    await prisma.auditLog.create({
      data: {
        adminUserId: req.admin!.id,
        merchantId: merchant.id,
        action: 'merchant.suspended',
        resource: 'merchant',
        resourceId: merchant.id,
        details: { reason },
        ipAddress: req.ip,
      },
    });

    res.json({ merchant: result });
  }
);

// GET /admin/ledger/balances — Get ledger balances
router.get(
  '/ledger/balances',
  adminAuth(),
  async (req: Request, res: Response) => {
    const balances = await Ledger.getBalances();
    const verification = await Ledger.verify();
    res.json({ accounts: balances, verification });
  }
);

// GET /admin/stats — Platform-wide stats
router.get(
  '/stats',
  adminAuth(),
  async (req: Request, res: Response) => {
    const now = new Date();
    const startOfMonth = new Date(now.getFullYear(), now.getMonth(), 1);
    const startOfDay = new Date(now.getFullYear(), now.getMonth(), now.getDate());

    const [
      totalMerchants,
      activeMerchants,
      monthlyVolume,
      dailyVolume,
      openDisputes,
      pendingPayouts,
    ] = await Promise.all([
      prisma.merchant.count(),
      prisma.merchant.count({ where: { status: 'ACTIVE' } }),
      prisma.transaction.aggregate({
        where: { status: { in: ['CAPTURED', 'SETTLED'] }, createdAt: { gte: startOfMonth } },
        _sum: { amount: true, fee: true },
        _count: true,
      }),
      prisma.transaction.aggregate({
        where: { status: { in: ['CAPTURED', 'SETTLED'] }, createdAt: { gte: startOfDay } },
        _sum: { amount: true, fee: true },
        _count: true,
      }),
      prisma.dispute.count({ where: { status: { in: ['OPEN', 'EVIDENCE_NEEDED'] } } }),
      prisma.payout.aggregate({
        where: { status: 'PENDING' },
        _sum: { amount: true },
        _count: true,
      }),
    ]);

    res.json({
      merchants: { total: totalMerchants, active: activeMerchants },
      monthlyVolume: {
        grossVolume: monthlyVolume._sum.amount || 0,
        revenue: monthlyVolume._sum.fee || 0,
        transactionCount: monthlyVolume._count,
      },
      dailyVolume: {
        grossVolume: dailyVolume._sum.amount || 0,
        revenue: dailyVolume._sum.fee || 0,
        transactionCount: dailyVolume._count,
      },
      openDisputes,
      pendingPayouts: {
        amount: pendingPayouts._sum.amount || 0,
        count: pendingPayouts._count,
      },
    });
  }
);

// POST /admin/setup — Initial admin setup (only works if no admins exist)
const setupSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
  firstName: z.string().min(1),
  lastName: z.string().min(1),
});

router.post('/setup', async (req: Request, res: Response) => {
  const existing = await prisma.adminUser.count();
  if (existing > 0) {
    throw new AppError(403, 'already_setup', 'Admin already exists. Use login instead.');
  }

  const input = setupSchema.parse(req.body);
  const hashedPassword = await bcrypt.hash(input.password, 12);

  const admin = await prisma.adminUser.create({
    data: {
      email: input.email,
      password: hashedPassword,
      firstName: input.firstName,
      lastName: input.lastName,
      role: 'SUPER_ADMIN',
    },
  });

  // Initialize ledger accounts
  await Ledger.initializeAccounts();

  const token = jwt.sign(
    { sub: admin.id, email: admin.email, role: admin.role },
    config.jwt.secret,
    { expiresIn: config.jwt.expiresIn }
  );

  res.status(201).json({
    message: 'Admin account created and ledger initialized',
    token,
    admin: { id: admin.id, email: admin.email, role: admin.role },
  });
});

export default router;
