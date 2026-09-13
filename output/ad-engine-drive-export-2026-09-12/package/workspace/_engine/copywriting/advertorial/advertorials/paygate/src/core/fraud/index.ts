/**
 * Fraud Detection Engine
 *
 * Rule-based fraud scoring system. Each transaction gets a score
 * from 0-100. Higher score = more suspicious.
 *
 * Scores above thresholds trigger actions:
 * - 0-30:   Pass (process normally)
 * - 31-60:  Review (process but flag for manual review)
 * - 61-80:  Challenge (require 3DS or additional verification)
 * - 81-100: Block (decline the transaction)
 */

import { prisma } from '../../config/database';
import { redis } from '../../config/redis';
import { logger } from '../../config/logger';

export interface FraudCheckInput {
  merchantId: string;
  amount: number;          // in cents
  cardFingerprint?: string;
  cardBin?: string;        // first 6-8 digits
  customerEmail?: string;
  ipAddress?: string;
  userAgent?: string;
  billingCountry?: string;
  shippingCountry?: string;
}

export interface FraudCheckResult {
  score: number;
  flags: string[];
  action: 'pass' | 'review' | 'challenge' | 'block';
}

export class FraudEngine {
  private static readonly VELOCITY_WINDOW = 3600; // 1 hour in seconds
  private static readonly DAILY_WINDOW = 86400;   // 24 hours

  /**
   * Run all fraud checks on a transaction.
   */
  static async check(input: FraudCheckInput): Promise<FraudCheckResult> {
    const flags: string[] = [];
    let score = 0;

    // Run all checks in parallel
    const results = await Promise.allSettled([
      this.checkVelocity(input),
      this.checkAmount(input),
      this.checkGeo(input),
      this.checkCardReputation(input),
      this.checkEmailReputation(input),
      this.checkMerchantRisk(input),
    ]);

    for (const result of results) {
      if (result.status === 'fulfilled') {
        score += result.value.score;
        flags.push(...result.value.flags);
      }
    }

    // Cap at 100
    score = Math.min(score, 100);

    // Determine action
    let action: FraudCheckResult['action'];
    if (score <= 30) action = 'pass';
    else if (score <= 60) action = 'review';
    else if (score <= 80) action = 'challenge';
    else action = 'block';

    logger.info('Fraud check completed', {
      merchantId: input.merchantId,
      score,
      action,
      flags,
    });

    return { score, flags, action };
  }

  /**
   * Velocity checks — how many transactions in a time window.
   * Rapid-fire transactions from the same card/email/IP are suspicious.
   */
  private static async checkVelocity(input: FraudCheckInput): Promise<{ score: number; flags: string[] }> {
    let score = 0;
    const flags: string[] = [];

    // Card velocity (same card, last hour)
    if (input.cardFingerprint) {
      const key = `fraud:velocity:card:${input.cardFingerprint}`;
      const count = await redis.incr(key);
      if (count === 1) await redis.expire(key, this.VELOCITY_WINDOW);

      if (count > 10) {
        score += 40;
        flags.push('high_card_velocity');
      } else if (count > 5) {
        score += 20;
        flags.push('elevated_card_velocity');
      }
    }

    // IP velocity (same IP, last hour)
    if (input.ipAddress) {
      const key = `fraud:velocity:ip:${input.ipAddress}`;
      const count = await redis.incr(key);
      if (count === 1) await redis.expire(key, this.VELOCITY_WINDOW);

      if (count > 20) {
        score += 30;
        flags.push('high_ip_velocity');
      } else if (count > 10) {
        score += 15;
        flags.push('elevated_ip_velocity');
      }
    }

    // Email velocity (same email, last 24h)
    if (input.customerEmail) {
      const key = `fraud:velocity:email:${input.customerEmail.toLowerCase()}`;
      const count = await redis.incr(key);
      if (count === 1) await redis.expire(key, this.DAILY_WINDOW);

      if (count > 15) {
        score += 25;
        flags.push('high_email_velocity');
      }
    }

    return { score, flags };
  }

  /**
   * Amount checks — unusually large or suspicious amounts.
   */
  private static async checkAmount(input: FraudCheckInput): Promise<{ score: number; flags: string[] }> {
    let score = 0;
    const flags: string[] = [];
    const amountDollars = input.amount / 100;

    // Check against merchant's average ticket
    const merchant = await prisma.merchant.findUnique({
      where: { id: input.merchantId },
      select: { averageTicket: true, monthlyVolume: true },
    });

    if (merchant?.averageTicket) {
      const avg = Number(merchant.averageTicket);
      if (avg > 0 && amountDollars > avg * 5) {
        score += 25;
        flags.push('amount_5x_average');
      } else if (avg > 0 && amountDollars > avg * 3) {
        score += 10;
        flags.push('amount_3x_average');
      }
    }

    // Round dollar amounts are slightly more suspicious
    if (amountDollars >= 100 && amountDollars % 100 === 0) {
      score += 5;
      flags.push('round_amount');
    }

    // Very high amounts
    if (amountDollars > 10000) {
      score += 15;
      flags.push('high_amount');
    }

    return { score, flags };
  }

  /**
   * Geographic checks — mismatched countries, high-risk regions.
   */
  private static async checkGeo(input: FraudCheckInput): Promise<{ score: number; flags: string[] }> {
    let score = 0;
    const flags: string[] = [];

    // Billing/shipping country mismatch
    if (input.billingCountry && input.shippingCountry &&
        input.billingCountry !== input.shippingCountry) {
      score += 15;
      flags.push('country_mismatch');
    }

    // High-risk countries (common sources of card fraud)
    const highRiskCountries = new Set([
      'NG', 'GH', 'CM', 'CI', 'SN',  // West Africa
      'RO', 'BG', 'UA', 'RU',         // Eastern Europe
      'ID', 'MY', 'PH', 'VN',         // Southeast Asia
      'BR', 'MX', 'CO',               // Latin America
    ]);

    if (input.billingCountry && highRiskCountries.has(input.billingCountry)) {
      score += 20;
      flags.push('high_risk_country');
    }

    return { score, flags };
  }

  /**
   * Card reputation — has this card been involved in disputes/fraud before?
   */
  private static async checkCardReputation(input: FraudCheckInput): Promise<{ score: number; flags: string[] }> {
    let score = 0;
    const flags: string[] = [];

    if (!input.cardFingerprint) return { score, flags };

    // Check for previous disputes with this card
    const disputeCount = await prisma.dispute.count({
      where: {
        transaction: { cardFingerprint: input.cardFingerprint },
        status: { in: ['LOST', 'OPEN'] },
      },
    });

    if (disputeCount > 0) {
      score += 40;
      flags.push('card_has_disputes');
    }

    // Check for previous declines
    const declineCount = await prisma.transaction.count({
      where: {
        cardFingerprint: input.cardFingerprint,
        status: 'DECLINED',
        createdAt: { gte: new Date(Date.now() - this.DAILY_WINDOW * 1000) },
      },
    });

    if (declineCount >= 3) {
      score += 30;
      flags.push('multiple_declines');
    }

    // BIN check — prepaid cards are higher risk
    if (input.cardBin) {
      const key = `fraud:bin:${input.cardBin}`;
      const binData = await redis.get(key);
      if (binData) {
        const data = JSON.parse(binData);
        if (data.prepaid) {
          score += 10;
          flags.push('prepaid_card');
        }
      }
    }

    return { score, flags };
  }

  /**
   * Email reputation checks.
   */
  private static async checkEmailReputation(input: FraudCheckInput): Promise<{ score: number; flags: string[] }> {
    let score = 0;
    const flags: string[] = [];

    if (!input.customerEmail) return { score, flags };

    const email = input.customerEmail.toLowerCase();

    // Disposable email domains
    const disposableDomains = new Set([
      'mailinator.com', 'guerrillamail.com', 'tempmail.com', 'throwaway.email',
      'yopmail.com', 'sharklasers.com', 'guerrillamailblock.com', 'grr.la',
      'dispostable.com', 'trashmail.com', '10minutemail.com', 'temp-mail.org',
    ]);

    const domain = email.split('@')[1];
    if (domain && disposableDomains.has(domain)) {
      score += 25;
      flags.push('disposable_email');
    }

    // Previous disputes from this email
    const disputeCount = await prisma.dispute.count({
      where: {
        transaction: { customerEmail: email },
        status: { in: ['LOST', 'OPEN'] },
      },
    });

    if (disputeCount > 0) {
      score += 20;
      flags.push('email_has_disputes');
    }

    return { score, flags };
  }

  /**
   * Merchant risk — check if the merchant itself is high-risk.
   */
  private static async checkMerchantRisk(input: FraudCheckInput): Promise<{ score: number; flags: string[] }> {
    let score = 0;
    const flags: string[] = [];

    const merchant = await prisma.merchant.findUnique({
      where: { id: input.merchantId },
      select: { riskScore: true, chargebackRate: true, status: true },
    });

    if (!merchant) return { score, flags };

    // High chargeback rate
    if (Number(merchant.chargebackRate) > 0.01) {
      score += 15;
      flags.push('merchant_high_chargeback_rate');
    }

    // Merchant risk score
    if (merchant.riskScore > 70) {
      score += 10;
      flags.push('merchant_high_risk');
    }

    return { score, flags };
  }
}
