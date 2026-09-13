import { prisma } from '../config/database';
import { AppError } from '../api/middleware/errorHandler';
import { generateApiKey, generateWebhookSecret, encrypt } from '../utils/encryption';
import { Ledger } from '../core/ledger';
import { logger } from '../config/logger';
import { Prisma } from '@prisma/client';

export interface CreateMerchantInput {
  email: string;
  businessName: string;
  businessType?: string;
  legalName?: string;
  taxId?: string;
  website?: string;
  phone?: string;
  addressLine1?: string;
  addressLine2?: string;
  city?: string;
  state?: string;
  postalCode?: string;
  country?: string;
  mcc?: string;
  monthlyVolume?: number;
  averageTicket?: number;
  owners?: {
    firstName: string;
    lastName: string;
    email?: string;
    dateOfBirth?: string;
    ssn?: string;
    title?: string;
    ownershipPct?: number;
  }[];
}

export class MerchantService {
  /**
   * Create a new merchant and generate their first API key.
   */
  static async create(input: CreateMerchantInput) {
    // Check duplicate email
    const existing = await prisma.merchant.findUnique({ where: { email: input.email } });
    if (existing) {
      throw new AppError(409, 'duplicate_merchant', 'A merchant with this email already exists');
    }

    // Generate API keys (test + live)
    const testKey = generateApiKey();
    const liveKey = generateApiKey();

    const merchant = await prisma.merchant.create({
      data: {
        email: input.email,
        businessName: input.businessName,
        businessType: (input.businessType as any) || 'LLC',
        legalName: input.legalName,
        taxId: input.taxId ? encrypt(input.taxId) : undefined,
        website: input.website,
        phone: input.phone,
        addressLine1: input.addressLine1,
        addressLine2: input.addressLine2,
        city: input.city,
        state: input.state,
        postalCode: input.postalCode,
        country: input.country || 'US',
        mcc: input.mcc,
        monthlyVolume: input.monthlyVolume,
        averageTicket: input.averageTicket,
        status: 'PENDING',
        apiKeys: {
          create: [
            {
              keyHash: testKey.hash,
              prefix: testKey.prefix,
              label: 'Default Test Key',
              environment: 'test',
              permissions: [
                'transactions.create', 'transactions.read',
                'refunds.create', 'payouts.read', 'webhooks.manage',
              ],
            },
            {
              keyHash: liveKey.hash,
              prefix: liveKey.prefix,
              label: 'Default Live Key',
              environment: 'live',
              permissions: [
                'transactions.create', 'transactions.read',
                'refunds.create', 'payouts.read', 'webhooks.manage',
              ],
            },
          ],
        },
        owners: input.owners ? {
          create: input.owners.map((o) => ({
            firstName: o.firstName,
            lastName: o.lastName,
            email: o.email,
            dateOfBirth: o.dateOfBirth ? encrypt(o.dateOfBirth) : undefined,
            ssn: o.ssn ? encrypt(o.ssn) : undefined,
            title: o.title,
            ownershipPct: o.ownershipPct,
          })),
        } : undefined,
      },
      include: { owners: true },
    });

    logger.info('Merchant created', { merchantId: merchant.id, email: merchant.email });

    return {
      merchant,
      keys: {
        test: testKey.key,  // Only returned once at creation
        live: liveKey.key,  // Only returned once at creation
      },
    };
  }

  /**
   * Get merchant by ID (public-facing ID).
   */
  static async getByExternalId(externalId: string) {
    const merchant = await prisma.merchant.findUnique({
      where: { externalId },
      include: {
        bankAccounts: { select: { id: true, accountName: true, accountType: true, isPrimary: true, verified: true } },
        owners: { select: { id: true, firstName: true, lastName: true, title: true, kycStatus: true } },
        _count: { select: { transactions: true, payouts: true, disputes: true } },
      },
    });

    if (!merchant) {
      throw new AppError(404, 'not_found', 'Merchant not found');
    }

    return merchant;
  }

  /**
   * Add a bank account for payouts.
   */
  static async addBankAccount(merchantId: string, input: {
    accountName: string;
    routingNumber: string;
    accountNumber: string;
    accountType?: string;
  }) {
    // Validate routing number
    const routing = input.routingNumber.replace(/\D/g, '');
    if (routing.length !== 9) {
      throw new AppError(400, 'invalid_routing', 'Routing number must be 9 digits');
    }

    // Check if this is the first account (make it primary)
    const existingCount = await prisma.merchantBankAccount.count({ where: { merchantId } });

    const account = await prisma.merchantBankAccount.create({
      data: {
        merchantId,
        accountName: input.accountName,
        routingNumber: encrypt(routing),
        accountNumber: encrypt(input.accountNumber),
        accountType: input.accountType || 'checking',
        isPrimary: existingCount === 0, // first account is primary
      },
    });

    logger.info('Bank account added', { merchantId, accountId: account.id });

    return {
      id: account.id,
      accountName: account.accountName,
      routingLast4: routing.slice(-4),
      accountLast4: input.accountNumber.slice(-4),
      accountType: account.accountType,
      isPrimary: account.isPrimary,
      verified: account.verified,
    };
  }

  /**
   * Approve a merchant (admin action).
   */
  static async approve(merchantId: string) {
    const merchant = await prisma.merchant.update({
      where: { id: merchantId },
      data: { status: 'ACTIVE' },
    });

    logger.info('Merchant approved', { merchantId });
    return merchant;
  }

  /**
   * Suspend a merchant (admin action).
   */
  static async suspend(merchantId: string, reason: string) {
    const merchant = await prisma.merchant.update({
      where: { id: merchantId },
      data: { status: 'SUSPENDED' },
    });

    logger.warn('Merchant suspended', { merchantId, reason });
    return merchant;
  }

  /**
   * Get merchant dashboard stats.
   */
  static async getDashboardStats(merchantId: string) {
    const now = new Date();
    const startOfMonth = new Date(now.getFullYear(), now.getMonth(), 1);
    const startOfDay = new Date(now.getFullYear(), now.getMonth(), now.getDate());

    const [
      monthlyVolume,
      dailyVolume,
      pendingPayouts,
      openDisputes,
      recentTransactions,
    ] = await Promise.all([
      prisma.transaction.aggregate({
        where: { merchantId, status: { in: ['CAPTURED', 'SETTLED'] }, createdAt: { gte: startOfMonth } },
        _sum: { amount: true },
        _count: true,
      }),
      prisma.transaction.aggregate({
        where: { merchantId, status: { in: ['CAPTURED', 'SETTLED'] }, createdAt: { gte: startOfDay } },
        _sum: { amount: true },
        _count: true,
      }),
      prisma.payout.aggregate({
        where: { merchantId, status: 'PENDING' },
        _sum: { amount: true },
        _count: true,
      }),
      prisma.dispute.count({ where: { merchantId, status: { in: ['OPEN', 'EVIDENCE_NEEDED'] } } }),
      prisma.transaction.findMany({
        where: { merchantId },
        orderBy: { createdAt: 'desc' },
        take: 10,
        select: {
          externalId: true, type: true, status: true, amount: true,
          paymentMethod: true, cardBrand: true, cardLast4: true,
          createdAt: true,
        },
      }),
    ]);

    return {
      monthlyVolume: {
        amount: monthlyVolume._sum.amount || 0,
        count: monthlyVolume._count,
      },
      dailyVolume: {
        amount: dailyVolume._sum.amount || 0,
        count: dailyVolume._count,
      },
      pendingPayouts: {
        amount: pendingPayouts._sum.amount || 0,
        count: pendingPayouts._count,
      },
      openDisputes,
      recentTransactions,
    };
  }

  /**
   * List merchants (admin).
   */
  static async list(params: {
    status?: string;
    search?: string;
    page?: number;
    limit?: number;
  }) {
    const { status, search, page = 1, limit = 20 } = params;
    const skip = (page - 1) * limit;

    const where: any = {};
    if (status) where.status = status;
    if (search) {
      where.OR = [
        { businessName: { contains: search, mode: 'insensitive' } },
        { email: { contains: search, mode: 'insensitive' } },
      ];
    }

    const [merchants, total] = await Promise.all([
      prisma.merchant.findMany({
        where,
        skip,
        take: limit,
        orderBy: { createdAt: 'desc' },
        select: {
          id: true, externalId: true, email: true, businessName: true,
          status: true, createdAt: true, kycStatus: true,
          _count: { select: { transactions: true } },
        },
      }),
      prisma.merchant.count({ where }),
    ]);

    return { merchants, total, page, limit, pages: Math.ceil(total / limit) };
  }
}
