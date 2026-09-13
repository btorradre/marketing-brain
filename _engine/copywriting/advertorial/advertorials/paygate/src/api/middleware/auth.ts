/**
 * API Key Authentication Middleware
 *
 * Merchants authenticate via API key in the Authorization header:
 *   Authorization: Bearer pg_live_xxxxx
 *
 * Admin users authenticate via JWT token:
 *   Authorization: Bearer eyJhbG...
 */

import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';
import { prisma } from '../../config/database';
import { config } from '../../config';
import { hashValue } from '../../utils/encryption';

// Extend Express Request to include auth context
declare global {
  namespace Express {
    interface Request {
      merchant?: {
        id: string;
        externalId: string;
        businessName: string;
        status: string;
        environment: string;
      };
      admin?: {
        id: string;
        email: string;
        role: string;
      };
    }
  }
}

/**
 * Authenticate merchant API requests.
 * Expects: Authorization: Bearer pg_[test|live]_xxxxx
 */
export function merchantAuth(requiredPermission?: string) {
  return async (req: Request, res: Response, next: NextFunction) => {
    try {
      const authHeader = req.headers.authorization;
      if (!authHeader?.startsWith('Bearer ')) {
        return res.status(401).json({ error: 'Missing API key', code: 'auth_required' });
      }

      const apiKey = authHeader.slice(7);

      // Validate key format
      if (!apiKey.startsWith('pg_')) {
        return res.status(401).json({ error: 'Invalid API key format', code: 'invalid_key' });
      }

      // Hash the key to look it up
      const keyHash = hashValue(apiKey);
      const prefix = apiKey.slice(0, 12);

      const keyRecord = await prisma.apiKey.findFirst({
        where: {
          AND: [
            { OR: [{ keyHash }, { prefix }] },
            { revokedAt: null },
            { OR: [{ expiresAt: null }, { expiresAt: { gt: new Date() } }] },
          ],
        },
        include: {
          merchant: {
            select: { id: true, externalId: true, businessName: true, status: true },
          },
        },
      });

      if (!keyRecord) {
        return res.status(401).json({ error: 'Invalid API key', code: 'invalid_key' });
      }

      // Check merchant status
      if (keyRecord.merchant.status !== 'ACTIVE') {
        return res.status(403).json({
          error: `Merchant account is ${keyRecord.merchant.status.toLowerCase()}`,
          code: 'merchant_inactive',
        });
      }

      // Check permission
      if (requiredPermission && !keyRecord.permissions.includes(requiredPermission)) {
        return res.status(403).json({
          error: `API key lacks permission: ${requiredPermission}`,
          code: 'insufficient_permissions',
        });
      }

      // Update last used
      await prisma.apiKey.update({
        where: { id: keyRecord.id },
        data: { lastUsedAt: new Date() },
      });

      // Attach merchant to request
      req.merchant = {
        id: keyRecord.merchant.id,
        externalId: keyRecord.merchant.externalId,
        businessName: keyRecord.merchant.businessName,
        status: keyRecord.merchant.status,
        environment: keyRecord.environment,
      };

      next();
    } catch (error) {
      next(error);
    }
  };
}

/**
 * Authenticate admin JWT requests.
 * Expects: Authorization: Bearer eyJhbG...
 */
export function adminAuth(requiredRole?: string[]) {
  return async (req: Request, res: Response, next: NextFunction) => {
    try {
      const authHeader = req.headers.authorization;
      if (!authHeader?.startsWith('Bearer ')) {
        return res.status(401).json({ error: 'Missing token', code: 'auth_required' });
      }

      const token = authHeader.slice(7);

      // Don't confuse API keys with JWTs
      if (token.startsWith('pg_')) {
        return res.status(401).json({ error: 'Expected admin JWT, got API key', code: 'wrong_auth_type' });
      }

      const payload = jwt.verify(token, config.jwt.secret) as {
        sub: string;
        email: string;
        role: string;
      };

      // Verify admin still exists and is active
      const admin = await prisma.adminUser.findUnique({
        where: { id: payload.sub },
        select: { id: true, email: true, role: true, active: true },
      });

      if (!admin || !admin.active) {
        return res.status(401).json({ error: 'Admin account inactive', code: 'admin_inactive' });
      }

      // Check role
      if (requiredRole && !requiredRole.includes(admin.role)) {
        return res.status(403).json({ error: 'Insufficient role', code: 'insufficient_role' });
      }

      req.admin = { id: admin.id, email: admin.email, role: admin.role };
      next();
    } catch (error) {
      if (error instanceof jwt.JsonWebTokenError) {
        return res.status(401).json({ error: 'Invalid token', code: 'invalid_token' });
      }
      next(error);
    }
  };
}
