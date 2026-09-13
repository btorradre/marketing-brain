/**
 * NMI (Network Merchants Inc.) Processor Integration
 *
 * NMI is a popular payment gateway that connects to major acquiring banks.
 * Lower barrier to entry than TSYS/Fiserv — good for starting out as an ISO.
 * Uses a simple POST-based API (not ISO 8583 directly — NMI translates).
 *
 * Docs: https://secure.nmi.com/merchants/resources/integration/integration_portal.php
 */

import { config } from '../../config';
import { logger } from '../../config/logger';
import {
  BaseProcessor,
  CardData,
  TokenizedCard,
  ProcessorResponse,
  AuthorizeRequest,
  CaptureRequest,
  RefundRequest,
  VoidRequest,
} from './base';
import crypto from 'crypto';

export class NmiProcessor extends BaseProcessor {
  readonly id = 'nmi';
  readonly name = 'NMI';

  private baseUrl = 'https://secure.nmi.com/api/transact.php';
  private securityKey: string;

  constructor() {
    super();
    this.securityKey = config.processors.nmi.securityKey;
  }

  private async post(params: Record<string, string>): Promise<Record<string, string>> {
    params.security_key = this.securityKey;

    const body = new URLSearchParams(params).toString();

    const response = await fetch(this.baseUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body,
    });

    const text = await response.text();
    const result: Record<string, string> = {};
    for (const pair of text.split('&')) {
      const [key, value] = pair.split('=');
      result[decodeURIComponent(key)] = decodeURIComponent(value || '');
    }

    logger.debug('NMI response', { response_code: result.response, response_text: result.responsetext });
    return result;
  }

  private parseResponse(res: Record<string, string>): ProcessorResponse {
    return {
      success: res.response === '1',
      transactionId: res.transactionid || '',
      authCode: res.authcode,
      responseCode: res.response_code || res.response || '',
      responseMessage: res.responsetext || '',
      avsResult: res.avsresponse,
      cvvResult: res.cvvresponse,
    };
  }

  async tokenize(card: CardData): Promise<TokenizedCard> {
    const res = await this.post({
      type: 'validate',
      ccnumber: card.number,
      ccexp: `${String(card.expMonth).padStart(2, '0')}${String(card.expYear).slice(-2)}`,
      cvv: card.cvv,
      customer_vault: 'add_customer',
    });

    if (res.response !== '1') {
      throw new Error(`Tokenization failed: ${res.responsetext}`);
    }

    const num = card.number.replace(/\D/g, '');

    return {
      token: res.customer_vault_id,
      brand: this.detectBrand(num),
      last4: num.slice(-4),
      expMonth: card.expMonth,
      expYear: card.expYear,
      fingerprint: crypto.createHash('sha256').update(num).digest('hex').slice(0, 16),
    };
  }

  async authorize(req: AuthorizeRequest): Promise<ProcessorResponse> {
    const params: Record<string, string> = {
      type: 'auth',
      amount: (req.amount / 100).toFixed(2),
      currency: req.currency || 'USD',
    };

    if (req.token) {
      params.customer_vault_id = req.token;
    } else if (req.card) {
      params.ccnumber = req.card.number;
      params.ccexp = `${String(req.card.expMonth).padStart(2, '0')}${String(req.card.expYear).slice(-2)}`;
      params.cvv = req.card.cvv;

      if (req.card.billingAddress) {
        params.address1 = req.card.billingAddress.line1;
        params.city = req.card.billingAddress.city;
        params.state = req.card.billingAddress.state;
        params.zip = req.card.billingAddress.postalCode;
        params.country = req.card.billingAddress.country;
      }
    }

    if (req.orderId) params.orderid = req.orderId;
    if (req.customerEmail) params.email = req.customerEmail;
    if (req.ipAddress) params.ip_address = req.ipAddress;

    const res = await this.post(params);
    return this.parseResponse(res);
  }

  async capture(req: CaptureRequest): Promise<ProcessorResponse> {
    const res = await this.post({
      type: 'capture',
      transactionid: req.transactionId,
      amount: (req.amount / 100).toFixed(2),
    });
    return this.parseResponse(res);
  }

  async charge(req: AuthorizeRequest): Promise<ProcessorResponse> {
    const params: Record<string, string> = {
      type: 'sale',
      amount: (req.amount / 100).toFixed(2),
      currency: req.currency || 'USD',
    };

    if (req.token) {
      params.customer_vault_id = req.token;
    } else if (req.card) {
      params.ccnumber = req.card.number;
      params.ccexp = `${String(req.card.expMonth).padStart(2, '0')}${String(req.card.expYear).slice(-2)}`;
      params.cvv = req.card.cvv;

      if (req.card.billingAddress) {
        params.address1 = req.card.billingAddress.line1;
        params.city = req.card.billingAddress.city;
        params.state = req.card.billingAddress.state;
        params.zip = req.card.billingAddress.postalCode;
        params.country = req.card.billingAddress.country;
      }
    }

    if (req.orderId) params.orderid = req.orderId;
    if (req.customerEmail) params.email = req.customerEmail;
    if (req.ipAddress) params.ip_address = req.ipAddress;

    const res = await this.post(params);
    return this.parseResponse(res);
  }

  async refund(req: RefundRequest): Promise<ProcessorResponse> {
    const res = await this.post({
      type: 'refund',
      transactionid: req.transactionId,
      amount: (req.amount / 100).toFixed(2),
    });
    return this.parseResponse(res);
  }

  async void(req: VoidRequest): Promise<ProcessorResponse> {
    const res = await this.post({
      type: 'void',
      transactionid: req.transactionId,
    });
    return this.parseResponse(res);
  }
}
