/**
 * Base processor interface — all payment processors (NMI, TSYS, Fiserv, etc.)
 * implement this interface. This is the abstraction layer between PayGate
 * and the card networks / banking rails.
 */

export interface CardData {
  number: string;
  expMonth: number;
  expYear: number;
  cvv: string;
  cardholderName?: string;
  billingAddress?: {
    line1: string;
    line2?: string;
    city: string;
    state: string;
    postalCode: string;
    country: string;
  };
}

export interface TokenizedCard {
  token: string;
  brand: string;       // visa, mastercard, amex, discover
  last4: string;
  expMonth: number;
  expYear: number;
  fingerprint: string; // unique identifier for the card
}

export interface ProcessorResponse {
  success: boolean;
  transactionId: string;  // processor's ID
  authCode?: string;
  responseCode: string;
  responseMessage: string;
  avsResult?: string;
  cvvResult?: string;
  networkTransactionId?: string;
}

export interface AuthorizeRequest {
  amount: number;         // in cents
  currency: string;
  card?: CardData;
  token?: string;         // use tokenized card
  orderId?: string;
  customerEmail?: string;
  ipAddress?: string;
  description?: string;
  metadata?: Record<string, string>;
}

export interface CaptureRequest {
  transactionId: string;  // processor's auth transaction ID
  amount: number;         // in cents, can be <= auth amount
}

export interface RefundRequest {
  transactionId: string;
  amount: number;         // in cents, partial refund supported
  reason?: string;
}

export interface VoidRequest {
  transactionId: string;
}

export abstract class BaseProcessor {
  abstract readonly id: string;
  abstract readonly name: string;

  /** Tokenize a card for future use */
  abstract tokenize(card: CardData): Promise<TokenizedCard>;

  /** Authorize a charge (hold funds, don't capture) */
  abstract authorize(req: AuthorizeRequest): Promise<ProcessorResponse>;

  /** Capture a previously authorized charge */
  abstract capture(req: CaptureRequest): Promise<ProcessorResponse>;

  /** Authorize and capture in one step */
  abstract charge(req: AuthorizeRequest): Promise<ProcessorResponse>;

  /** Refund a captured/settled transaction */
  abstract refund(req: RefundRequest): Promise<ProcessorResponse>;

  /** Void a transaction before settlement */
  abstract void(req: VoidRequest): Promise<ProcessorResponse>;

  /** Detect card brand from number */
  detectBrand(cardNumber: string): string {
    const num = cardNumber.replace(/\D/g, '');
    if (/^4/.test(num)) return 'visa';
    if (/^5[1-5]/.test(num) || /^2[2-7]/.test(num)) return 'mastercard';
    if (/^3[47]/.test(num)) return 'amex';
    if (/^6(?:011|5)/.test(num)) return 'discover';
    if (/^35/.test(num)) return 'jcb';
    if (/^3(?:0[0-5]|[68])/.test(num)) return 'diners';
    return 'unknown';
  }

  /** Luhn check for card number validation */
  validateCardNumber(cardNumber: string): boolean {
    const num = cardNumber.replace(/\D/g, '');
    if (num.length < 13 || num.length > 19) return false;

    let sum = 0;
    let alternate = false;
    for (let i = num.length - 1; i >= 0; i--) {
      let n = parseInt(num[i], 10);
      if (alternate) {
        n *= 2;
        if (n > 9) n -= 9;
      }
      sum += n;
      alternate = !alternate;
    }
    return sum % 10 === 0;
  }
}

/**
 * ACH processor interface — separate from card processing.
 * Handles bank-to-bank transfers via the ACH network.
 */

export interface AchDebitRequest {
  amount: number;          // in cents
  routingNumber: string;
  accountNumber: string;
  accountType: 'checking' | 'savings';
  accountHolderName: string;
  companyEntryDescription: string;
  orderId?: string;
}

export interface AchCreditRequest {
  amount: number;
  routingNumber: string;
  accountNumber: string;
  accountType: 'checking' | 'savings';
  accountHolderName: string;
  companyEntryDescription: string;
  addenda?: string;
}

export interface AchResponse {
  success: boolean;
  traceNumber: string;    // unique ACH trace number
  batchId: string;
  responseMessage: string;
}

export abstract class BaseAchProcessor {
  abstract readonly id: string;
  abstract readonly name: string;

  /** Pull money from a customer's bank account */
  abstract debit(req: AchDebitRequest): Promise<AchResponse>;

  /** Push money to a bank account (payouts) */
  abstract credit(req: AchCreditRequest): Promise<AchResponse>;

  /** Generate NACHA file for batch submission */
  abstract generateNachaFile(entries: NachaEntry[]): string;

  /** Validate routing number with checksum */
  validateRoutingNumber(routing: string): boolean {
    if (routing.length !== 9) return false;
    const d = routing.split('').map(Number);
    const checksum = (3 * (d[0] + d[3] + d[6]) + 7 * (d[1] + d[4] + d[7]) + (d[2] + d[5] + d[8])) % 10;
    return checksum === 0;
  }
}

export interface NachaEntry {
  transactionCode: string; // 22=checking credit, 27=checking debit, 32=savings credit, 37=savings debit
  routingNumber: string;
  accountNumber: string;
  amount: number;          // in cents
  name: string;            // recipient name
  traceNumber: string;
  addenda?: string;
}
