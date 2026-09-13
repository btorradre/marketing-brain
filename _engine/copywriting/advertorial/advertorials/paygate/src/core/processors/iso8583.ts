/**
 * ISO 8583 Message Builder
 *
 * ISO 8583 is THE protocol that card networks (Visa, Mastercard) use.
 * When you swipe/tap a card, the terminal sends an ISO 8583 message
 * through the acquiring bank to the card network to the issuing bank.
 *
 * Message structure:
 * 1. MTI (Message Type Indicator) — 4 digits
 * 2. Bitmap — indicates which data elements are present
 * 3. Data Elements — the actual fields (up to 128)
 *
 * Most processors (TSYS, Fiserv) accept ISO 8583 over TCP/IP.
 * NMI abstracts this away, but for direct connections you need this.
 *
 * MTI format: XXXX
 *   Position 1: Version (0=1987, 1=1993, 2=2003)
 *   Position 2: Message Class (1=auth, 2=financial, 4=reversal, 8=admin)
 *   Position 3: Message Function (0=request, 1=response, 2=advice)
 *   Position 4: Transaction Origin (0=acquirer, 1=repeat)
 *
 * Common MTIs:
 *   0100 = Authorization Request
 *   0110 = Authorization Response
 *   0200 = Financial Transaction Request (sale)
 *   0210 = Financial Transaction Response
 *   0400 = Reversal Request
 *   0410 = Reversal Response
 *   0800 = Network Management Request (echo test)
 *   0810 = Network Management Response
 */

export interface Iso8583Message {
  mti: string;
  fields: Map<number, string>;
}

// Field definitions with max lengths and types
const FIELD_DEFS: Record<number, { maxLen: number; type: 'n' | 'an' | 'ans' | 'b'; fixed?: boolean }> = {
  2: { maxLen: 19, type: 'n' },          // Primary Account Number (PAN)
  3: { maxLen: 6, type: 'n', fixed: true },   // Processing Code
  4: { maxLen: 12, type: 'n', fixed: true },  // Transaction Amount
  7: { maxLen: 10, type: 'n', fixed: true },  // Transmission Date & Time
  11: { maxLen: 6, type: 'n', fixed: true },  // System Trace Audit Number (STAN)
  12: { maxLen: 6, type: 'n', fixed: true },  // Local Transaction Time
  13: { maxLen: 4, type: 'n', fixed: true },  // Local Transaction Date
  14: { maxLen: 4, type: 'n', fixed: true },  // Expiration Date
  18: { maxLen: 4, type: 'n', fixed: true },  // Merchant Category Code (MCC)
  22: { maxLen: 3, type: 'n', fixed: true },  // POS Entry Mode
  23: { maxLen: 3, type: 'n', fixed: true },  // Card Sequence Number
  25: { maxLen: 2, type: 'n', fixed: true },  // POS Condition Code
  26: { maxLen: 2, type: 'n', fixed: true },  // POS PIN Capture Code
  32: { maxLen: 11, type: 'n' },         // Acquiring Institution ID
  35: { maxLen: 37, type: 'ans' },       // Track 2 Data
  37: { maxLen: 12, type: 'an', fixed: true }, // Retrieval Reference Number
  38: { maxLen: 6, type: 'an', fixed: true },  // Authorization ID Response
  39: { maxLen: 2, type: 'an', fixed: true },  // Response Code
  41: { maxLen: 8, type: 'ans', fixed: true }, // Card Acceptor Terminal ID
  42: { maxLen: 15, type: 'ans', fixed: true },// Card Acceptor Merchant ID
  43: { maxLen: 40, type: 'ans', fixed: true },// Card Acceptor Name/Location
  44: { maxLen: 25, type: 'ans' },       // Additional Response Data
  48: { maxLen: 999, type: 'ans' },      // Additional Data
  49: { maxLen: 3, type: 'n', fixed: true },   // Currency Code
  52: { maxLen: 16, type: 'b', fixed: true },  // PIN Data
  54: { maxLen: 120, type: 'ans' },      // Additional Amounts
  55: { maxLen: 999, type: 'ans' },      // EMV Data (ICC)
  60: { maxLen: 60, type: 'ans' },       // Reserved (Private)
  63: { maxLen: 999, type: 'ans' },      // Reserved (Private)
  70: { maxLen: 3, type: 'n', fixed: true },   // Network Management Info Code
  90: { maxLen: 42, type: 'n', fixed: true },  // Original Data Elements
  95: { maxLen: 42, type: 'an', fixed: true }, // Replacement Amounts
  100: { maxLen: 11, type: 'n' },        // Receiving Institution ID
  102: { maxLen: 28, type: 'ans' },      // Account ID 1
  103: { maxLen: 28, type: 'ans' },      // Account ID 2
  123: { maxLen: 999, type: 'ans' },     // POS Data Code
  126: { maxLen: 999, type: 'ans' },     // Private Data
  127: { maxLen: 999, type: 'ans' },     // Private Data
};

export class Iso8583Builder {
  private fields: Map<number, string> = new Map();
  private mti: string = '';

  /** Set the Message Type Indicator */
  setMti(mti: string): this {
    if (mti.length !== 4) throw new Error('MTI must be 4 digits');
    this.mti = mti;
    return this;
  }

  /** Set a data element field */
  setField(num: number, value: string): this {
    const def = FIELD_DEFS[num];
    if (def && value.length > def.maxLen) {
      throw new Error(`Field ${num} exceeds max length ${def.maxLen}`);
    }
    this.fields.set(num, value);
    return this;
  }

  /** Generate the primary bitmap (fields 1-64) and secondary bitmap (65-128) */
  private buildBitmap(): Buffer {
    const hasSecondary = Array.from(this.fields.keys()).some((k) => k > 64);
    const bitmapLen = hasSecondary ? 16 : 8; // 64 or 128 bits
    const bitmap = Buffer.alloc(bitmapLen, 0);

    if (hasSecondary) {
      // Set bit 1 to indicate secondary bitmap present
      bitmap[0] |= 0x80;
    }

    for (const fieldNum of this.fields.keys()) {
      const bitPos = fieldNum - 1; // 0-indexed
      const byteIdx = Math.floor(bitPos / 8);
      const bitIdx = 7 - (bitPos % 8);
      bitmap[byteIdx] |= 1 << bitIdx;
    }

    return bitmap;
  }

  /** Build the complete ISO 8583 message as a buffer */
  build(): Buffer {
    if (!this.mti) throw new Error('MTI not set');

    const parts: Buffer[] = [];

    // MTI
    parts.push(Buffer.from(this.mti, 'ascii'));

    // Bitmap
    parts.push(this.buildBitmap());

    // Data elements in order
    const sortedFields = Array.from(this.fields.entries()).sort(([a], [b]) => a - b);

    for (const [num, value] of sortedFields) {
      const def = FIELD_DEFS[num];

      if (def?.fixed) {
        // Fixed-length: just pad
        const padded = def.type === 'n'
          ? value.padStart(def.maxLen, '0')
          : value.padEnd(def.maxLen, ' ');
        parts.push(Buffer.from(padded, 'ascii'));
      } else {
        // Variable-length: add length prefix
        const lenDigits = (def?.maxLen || 999) > 99 ? 3 : 2;
        const lenPrefix = String(value.length).padStart(lenDigits, '0');
        parts.push(Buffer.from(lenPrefix + value, 'ascii'));
      }
    }

    return Buffer.concat(parts);
  }

  /** Parse an ISO 8583 response buffer back into fields */
  static parse(buffer: Buffer): Iso8583Message {
    let offset = 0;

    // MTI (4 bytes)
    const mti = buffer.subarray(offset, offset + 4).toString('ascii');
    offset += 4;

    // Primary bitmap (8 bytes)
    const primaryBitmap = buffer.subarray(offset, offset + 8);
    offset += 8;

    // Check for secondary bitmap (bit 1 of primary)
    const hasSecondary = (primaryBitmap[0] & 0x80) !== 0;
    let secondaryBitmap: Buffer | null = null;
    if (hasSecondary) {
      secondaryBitmap = buffer.subarray(offset, offset + 8);
      offset += 8;
    }

    const fields = new Map<number, string>();
    const maxField = hasSecondary ? 128 : 64;

    for (let fieldNum = 2; fieldNum <= maxField; fieldNum++) {
      const bitPos = fieldNum - 1;
      const byteIdx = Math.floor(bitPos / 8);
      const bitIdx = 7 - (bitPos % 8);

      const bitmapByte = byteIdx < 8
        ? primaryBitmap[byteIdx]
        : secondaryBitmap ? secondaryBitmap[byteIdx - 8] : 0;

      if (!(bitmapByte & (1 << bitIdx))) continue;

      const def = FIELD_DEFS[fieldNum];
      if (!def) {
        // Unknown field, skip
        continue;
      }

      let value: string;
      if (def.fixed) {
        value = buffer.subarray(offset, offset + def.maxLen).toString('ascii');
        offset += def.maxLen;
      } else {
        const lenDigits = def.maxLen > 99 ? 3 : 2;
        const len = parseInt(buffer.subarray(offset, offset + lenDigits).toString('ascii'), 10);
        offset += lenDigits;
        value = buffer.subarray(offset, offset + len).toString('ascii');
        offset += len;
      }

      fields.set(fieldNum, value.trim());
    }

    return { mti, fields };
  }
}

/**
 * Helper to build common ISO 8583 messages.
 * Use these with a direct TCP connection to a processor.
 */
export class Iso8583Messages {
  private stan = 0;

  private nextStan(): string {
    this.stan = (this.stan + 1) % 1000000;
    return String(this.stan).padStart(6, '0');
  }

  private nowDateTime(): { date: string; time: string; full: string } {
    const d = new Date();
    const MM = String(d.getMonth() + 1).padStart(2, '0');
    const DD = String(d.getDate()).padStart(2, '0');
    const hh = String(d.getHours()).padStart(2, '0');
    const mm = String(d.getMinutes()).padStart(2, '0');
    const ss = String(d.getSeconds()).padStart(2, '0');
    return {
      date: `${MM}${DD}`,
      time: `${hh}${mm}${ss}`,
      full: `${MM}${DD}${hh}${mm}${ss}`,
    };
  }

  /** Build Authorization Request (0100) */
  authorizationRequest(params: {
    pan: string;
    amount: number; // cents
    expDate: string; // YYMM
    cvv?: string;
    mcc: string;
    terminalId: string;
    merchantId: string;
    merchantName: string;
    currencyCode?: string;
  }): Buffer {
    const dt = this.nowDateTime();

    const builder = new Iso8583Builder()
      .setMti('0100')
      .setField(2, params.pan)
      .setField(3, '000000')                    // Processing code: purchase
      .setField(4, String(params.amount).padStart(12, '0'))
      .setField(7, dt.full)
      .setField(11, this.nextStan())
      .setField(12, dt.time)
      .setField(13, dt.date)
      .setField(14, params.expDate)
      .setField(18, params.mcc)
      .setField(22, '051')                      // POS entry: e-commerce
      .setField(25, '59')                        // POS condition: e-commerce
      .setField(41, params.terminalId)
      .setField(42, params.merchantId)
      .setField(43, params.merchantName)
      .setField(49, params.currencyCode || '840'); // 840 = USD

    return builder.build();
  }

  /** Build Sale Request (0200) — authorize + capture in one */
  saleRequest(params: {
    pan: string;
    amount: number;
    expDate: string;
    mcc: string;
    terminalId: string;
    merchantId: string;
    merchantName: string;
    currencyCode?: string;
  }): Buffer {
    const dt = this.nowDateTime();

    const builder = new Iso8583Builder()
      .setMti('0200')
      .setField(2, params.pan)
      .setField(3, '000000')
      .setField(4, String(params.amount).padStart(12, '0'))
      .setField(7, dt.full)
      .setField(11, this.nextStan())
      .setField(12, dt.time)
      .setField(13, dt.date)
      .setField(14, params.expDate)
      .setField(18, params.mcc)
      .setField(22, '051')
      .setField(25, '59')
      .setField(41, params.terminalId)
      .setField(42, params.merchantId)
      .setField(43, params.merchantName)
      .setField(49, params.currencyCode || '840');

    return builder.build();
  }

  /** Build Reversal Request (0400) — void a previous transaction */
  reversalRequest(params: {
    originalMti: string;
    originalStan: string;
    originalDateTime: string;
    originalAmount: number;
    pan: string;
    terminalId: string;
    merchantId: string;
  }): Buffer {
    const dt = this.nowDateTime();

    const builder = new Iso8583Builder()
      .setMti('0400')
      .setField(2, params.pan)
      .setField(3, '000000')
      .setField(4, String(params.originalAmount).padStart(12, '0'))
      .setField(7, dt.full)
      .setField(11, this.nextStan())
      .setField(12, dt.time)
      .setField(13, dt.date)
      .setField(41, params.terminalId)
      .setField(42, params.merchantId)
      .setField(90, `${params.originalMti}${params.originalStan}${params.originalDateTime}${'0'.repeat(22)}`);

    return builder.build();
  }

  /** Build Echo Test (0800) — network health check */
  echoTest(): Buffer {
    const dt = this.nowDateTime();

    const builder = new Iso8583Builder()
      .setMti('0800')
      .setField(7, dt.full)
      .setField(11, this.nextStan())
      .setField(70, '301'); // Network management info: echo test

    return builder.build();
  }

  /** Parse response code to human-readable message */
  static getResponseMessage(code: string): string {
    const codes: Record<string, string> = {
      '00': 'Approved',
      '01': 'Refer to card issuer',
      '02': 'Refer to card issuer (special)',
      '03': 'Invalid merchant',
      '04': 'Pick up card',
      '05': 'Do not honor',
      '06': 'Error',
      '07': 'Pick up card (special)',
      '08': 'Honor with ID',
      '10': 'Partial approval',
      '12': 'Invalid transaction',
      '13': 'Invalid amount',
      '14': 'Invalid card number',
      '15': 'No such issuer',
      '19': 'Re-enter transaction',
      '21': 'No action taken',
      '25': 'Unable to locate record',
      '28': 'File temporarily not available',
      '30': 'Format error',
      '41': 'Lost card - pick up',
      '43': 'Stolen card - pick up',
      '51': 'Insufficient funds',
      '54': 'Expired card',
      '55': 'Incorrect PIN',
      '57': 'Transaction not permitted',
      '58': 'Transaction not permitted for terminal',
      '59': 'Suspected fraud',
      '61': 'Exceeds withdrawal limit',
      '62': 'Restricted card',
      '63': 'Security violation',
      '65': 'Exceeds withdrawal frequency',
      '75': 'PIN tries exceeded',
      '76': 'Invalid/nonexistent account',
      '77': 'Invalid/nonexistent account',
      '78': 'No account',
      '80': 'Invalid date',
      '81': 'Encryption error',
      '82': 'CVV data not valid',
      '85': 'No reason to decline',
      '86': 'Cannot verify PIN',
      '91': 'Issuer unavailable',
      '92': 'Unable to route',
      '93': 'Cannot complete (violation)',
      '94': 'Duplicate transaction',
      '96': 'System malfunction',
    };
    return codes[code] || `Unknown response code: ${code}`;
  }
}
