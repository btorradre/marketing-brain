/**
 * ACH Processor — NACHA File Generation
 *
 * This is the real deal. NACHA (National Automated Clearing House Association)
 * files are how money actually moves between banks in the US.
 *
 * Flow:
 * 1. We generate a NACHA-formatted file with batch entries
 * 2. Upload the file to our ODFI (sponsor bank) via SFTP
 * 3. ODFI submits to Federal Reserve or EPN
 * 4. Receiving bank credits/debits the account
 * 5. We get return files back (for failures) via SFTP
 *
 * NACHA file format:
 * - File Header Record (1 record)
 * - Batch Header Record (1 per batch)
 * - Entry Detail Records (1 per transaction)
 * - Addenda Records (optional, 1 per entry)
 * - Batch Control Record (1 per batch)
 * - File Control Record (1 record)
 *
 * All records are exactly 94 characters.
 */

import { config } from '../../config';
import { logger } from '../../config/logger';
import { BaseAchProcessor, AchDebitRequest, AchCreditRequest, AchResponse, NachaEntry } from './base';

// NACHA transaction codes
const TX_CODES = {
  CHECKING_CREDIT: '22',
  CHECKING_DEBIT: '27',
  CHECKING_PRENOTE_CREDIT: '23',
  CHECKING_PRENOTE_DEBIT: '28',
  SAVINGS_CREDIT: '32',
  SAVINGS_DEBIT: '37',
  SAVINGS_PRENOTE_CREDIT: '33',
  SAVINGS_PRENOTE_DEBIT: '38',
} as const;

export class AchProcessor extends BaseAchProcessor {
  readonly id = 'ach_direct';
  readonly name = 'Direct ACH/NACHA';

  private odfiRouting: string;
  private odfiName: string;
  private companyId: string;
  private companyName: string;
  private traceSequence = 0;
  private batchNumber = 0;

  constructor() {
    super();
    this.odfiRouting = config.ach.odfiRouting;
    this.odfiName = config.ach.odfiName;
    this.companyId = config.ach.companyId;
    this.companyName = config.ach.companyName;
  }

  /** Generate a unique trace number for an ACH entry */
  private generateTraceNumber(): string {
    this.traceSequence++;
    const odfi = this.odfiRouting.slice(0, 8);
    const seq = String(this.traceSequence).padStart(7, '0');
    return `${odfi}${seq}`;
  }

  /** Get next batch number */
  private nextBatchNumber(): number {
    this.batchNumber++;
    return this.batchNumber;
  }

  /** Pad/truncate string to fixed width */
  private pad(str: string, len: number, fill = ' ', right = true): string {
    const s = str.slice(0, len);
    return right ? s.padEnd(len, fill) : s.padStart(len, fill);
  }

  /** Format amount in cents to NACHA format (10 digits, zero-padded) */
  private formatAmount(cents: number): string {
    return String(Math.abs(Math.round(cents))).padStart(10, '0');
  }

  /** Get current date in YYMMDD format */
  private dateYYMMDD(): string {
    const d = new Date();
    return `${String(d.getFullYear()).slice(-2)}${String(d.getMonth() + 1).padStart(2, '0')}${String(d.getDate()).padStart(2, '0')}`;
  }

  /** Get current time in HHMM format */
  private timeHHMM(): string {
    const d = new Date();
    return `${String(d.getHours()).padStart(2, '0')}${String(d.getMinutes()).padStart(2, '0')}`;
  }

  /**
   * Generate File Header Record (Record Type 1)
   * Exactly 94 characters.
   */
  private fileHeader(fileIdModifier = 'A'): string {
    const fields = [
      '1',                                          // Record Type Code (1)
      '01',                                         // Priority Code (2)
      ' ' + this.pad(this.odfiRouting, 9),           // Immediate Destination (10) — space + 9-digit routing
      this.pad(this.companyId, 10),                  // Immediate Origin (10) — company EIN
      this.dateYYMMDD(),                             // File Creation Date (6)
      this.timeHHMM(),                               // File Creation Time (4)
      fileIdModifier,                                // File ID Modifier (1)
      '094',                                         // Record Size (3)
      '10',                                          // Blocking Factor (2)
      '1',                                           // Format Code (1)
      this.pad(this.odfiName, 23),                   // Immediate Destination Name (23)
      this.pad(this.companyName, 23),                // Immediate Origin Name (23)
      this.pad('', 8),                               // Reference Code (8)
    ];
    return fields.join('');
  }

  /**
   * Generate Batch Header Record (Record Type 5)
   */
  private batchHeader(
    serviceClassCode: string,    // 200=mixed, 220=credits only, 225=debits only
    companyEntryDescription: string,
    effectiveEntryDate: string,  // YYMMDD
    batchNumber: number,
    standardEntryClass = 'PPD'   // PPD=personal, CCD=corporate, WEB=internet
  ): string {
    const fields = [
      '5',                                                    // Record Type Code
      serviceClassCode,                                        // Service Class Code (3)
      this.pad(this.companyName, 16),                          // Company Name (16)
      this.pad('', 20),                                        // Company Discretionary Data (20)
      this.pad(this.companyId, 10),                            // Company Identification (10)
      standardEntryClass,                                      // Standard Entry Class Code (3)
      this.pad(companyEntryDescription, 10),                   // Company Entry Description (10)
      this.dateYYMMDD(),                                       // Company Descriptive Date (6)
      effectiveEntryDate,                                      // Effective Entry Date (6)
      '   ',                                                   // Settlement Date — filled by ACH operator (3)
      '1',                                                     // Originator Status Code (1)
      this.pad(this.odfiRouting.slice(0, 8), 8),               // Originating DFI Identification (8)
      String(batchNumber).padStart(7, '0'),                    // Batch Number (7)
    ];
    return fields.join('');
  }

  /**
   * Generate Entry Detail Record (Record Type 6)
   */
  private entryDetail(entry: NachaEntry): string {
    const routingCheckDigit = entry.routingNumber.slice(-1);
    const routingTransit = entry.routingNumber.slice(0, 8);

    const fields = [
      '6',                                                    // Record Type Code
      entry.transactionCode,                                   // Transaction Code (2)
      routingTransit,                                          // Receiving DFI Identification (8)
      routingCheckDigit,                                       // Check Digit (1)
      this.pad(entry.accountNumber, 17),                       // DFI Account Number (17)
      this.formatAmount(entry.amount),                         // Amount (10)
      this.pad('', 15),                                        // Individual Identification Number (15)
      this.pad(entry.name, 22),                                // Individual Name (22)
      '  ',                                                    // Discretionary Data (2)
      entry.addenda ? '1' : '0',                               // Addenda Record Indicator (1)
      entry.traceNumber,                                       // Trace Number (15)
    ];
    return fields.join('');
  }

  /**
   * Generate Addenda Record (Record Type 7)
   */
  private addendaRecord(info: string, entrySequence: number): string {
    const fields = [
      '7',                                                    // Record Type Code
      '05',                                                    // Addenda Type Code
      this.pad(info, 80),                                      // Payment Related Information (80)
      String(entrySequence).padStart(4, '0'),                  // Addenda Sequence Number (4)
      String(entrySequence).padStart(7, '0'),                  // Entry Detail Sequence Number (7)
    ];
    return fields.join('');
  }

  /**
   * Generate Batch Control Record (Record Type 8)
   */
  private batchControl(
    serviceClassCode: string,
    entryCount: number,
    entryHash: number,
    totalDebit: number,
    totalCredit: number,
    batchNumber: number
  ): string {
    const fields = [
      '8',                                                    // Record Type Code
      serviceClassCode,                                        // Service Class Code (3)
      String(entryCount).padStart(6, '0'),                     // Entry/Addenda Count (6)
      String(entryHash % 10000000000).padStart(10, '0'),       // Entry Hash (10)
      this.formatAmount(totalDebit).padStart(12, '0'),         // Total Debit (12)
      this.formatAmount(totalCredit).padStart(12, '0'),        // Total Credit (12)
      this.pad(this.companyId, 10),                            // Company Identification (10)
      this.pad('', 19),                                        // Message Authentication Code (19)
      this.pad('', 6),                                         // Reserved (6)
      this.pad(this.odfiRouting.slice(0, 8), 8),               // Originating DFI Identification (8)
      String(batchNumber).padStart(7, '0'),                    // Batch Number (7)
    ];
    return fields.join('');
  }

  /**
   * Generate File Control Record (Record Type 9)
   */
  private fileControl(
    batchCount: number,
    blockCount: number,
    entryCount: number,
    entryHash: number,
    totalDebit: number,
    totalCredit: number
  ): string {
    const fields = [
      '9',                                                    // Record Type Code
      String(batchCount).padStart(6, '0'),                     // Batch Count (6)
      String(blockCount).padStart(6, '0'),                     // Block Count (6)
      String(entryCount).padStart(8, '0'),                     // Entry/Addenda Count (8)
      String(entryHash % 10000000000).padStart(10, '0'),       // Entry Hash (10)
      this.formatAmount(totalDebit).padStart(12, '0'),         // Total Debit (12)
      this.formatAmount(totalCredit).padStart(12, '0'),        // Total Credit (12)
      this.pad('', 39),                                        // Reserved (39)
    ];
    return fields.join('');
  }

  /**
   * Generate a complete NACHA file from a list of entries.
   * This is the file you upload to your ODFI via SFTP.
   */
  generateNachaFile(entries: NachaEntry[]): string {
    if (entries.length === 0) {
      throw new Error('Cannot generate NACHA file with no entries');
    }

    this.traceSequence = 0;
    const lines: string[] = [];

    // Determine service class
    const hasDebits = entries.some((e) => ['27', '37'].includes(e.transactionCode));
    const hasCredits = entries.some((e) => ['22', '32'].includes(e.transactionCode));
    const serviceClassCode = hasDebits && hasCredits ? '200' : hasCredits ? '220' : '225';

    // Effective entry date = tomorrow (T+1)
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    const effectiveDate = `${String(tomorrow.getFullYear()).slice(-2)}${String(tomorrow.getMonth() + 1).padStart(2, '0')}${String(tomorrow.getDate()).padStart(2, '0')}`;

    const batchNum = this.nextBatchNumber();

    // File Header
    lines.push(this.fileHeader());

    // Batch Header
    lines.push(this.batchHeader(serviceClassCode, 'PAYMENT', effectiveDate, batchNum));

    // Entries
    let entryHash = 0;
    let totalDebit = 0;
    let totalCredit = 0;
    let addendaCount = 0;

    for (const entry of entries) {
      // Assign trace number if not set
      if (!entry.traceNumber) {
        entry.traceNumber = this.generateTraceNumber();
      }

      lines.push(this.entryDetail(entry));

      // Sum routing numbers for hash
      entryHash += parseInt(entry.routingNumber.slice(0, 8), 10);

      // Sum amounts
      if (['27', '37'].includes(entry.transactionCode)) {
        totalDebit += entry.amount;
      } else {
        totalCredit += entry.amount;
      }

      // Addenda
      if (entry.addenda) {
        addendaCount++;
        lines.push(this.addendaRecord(entry.addenda, addendaCount));
      }
    }

    // Batch Control
    lines.push(this.batchControl(serviceClassCode, entries.length + addendaCount, entryHash, totalDebit, totalCredit, batchNum));

    // File Control
    const totalLines = lines.length + 1; // +1 for file control itself
    const blockCount = Math.ceil(totalLines / 10);
    lines.push(this.fileControl(1, blockCount, entries.length + addendaCount, entryHash, totalDebit, totalCredit));

    // Pad to block boundary (each block = 10 lines of 94 chars)
    const totalRecords = lines.length;
    const needed = blockCount * 10 - totalRecords;
    for (let i = 0; i < needed; i++) {
      lines.push('9'.repeat(94));
    }

    logger.info('Generated NACHA file', {
      entries: entries.length,
      totalDebit: totalDebit / 100,
      totalCredit: totalCredit / 100,
      batches: 1,
    });

    return lines.join('\n');
  }

  /** Pull money from a customer's bank (debit) */
  async debit(req: AchDebitRequest): Promise<AchResponse> {
    if (!this.validateRoutingNumber(req.routingNumber)) {
      return { success: false, traceNumber: '', batchId: '', responseMessage: 'Invalid routing number' };
    }

    const txCode = req.accountType === 'savings' ? TX_CODES.SAVINGS_DEBIT : TX_CODES.CHECKING_DEBIT;
    const traceNumber = this.generateTraceNumber();

    const entry: NachaEntry = {
      transactionCode: txCode,
      routingNumber: req.routingNumber,
      accountNumber: req.accountNumber,
      amount: req.amount,
      name: req.accountHolderName,
      traceNumber,
      addenda: req.orderId ? `ORDER:${req.orderId}` : undefined,
    };

    // In production, this entry would be batched and submitted via SFTP
    // For now, we generate the file and return success
    const nachaContent = this.generateNachaFile([entry]);
    const batchId = `ACH-${Date.now()}`;

    logger.info('ACH debit created', { traceNumber, amount: req.amount / 100, batchId });

    // TODO: Upload NACHA file to ODFI via SFTP
    // await this.uploadToOdfi(nachaContent, batchId);

    return {
      success: true,
      traceNumber,
      batchId,
      responseMessage: 'ACH debit entry created',
    };
  }

  /** Push money to a bank account (credit / payout) */
  async credit(req: AchCreditRequest): Promise<AchResponse> {
    if (!this.validateRoutingNumber(req.routingNumber)) {
      return { success: false, traceNumber: '', batchId: '', responseMessage: 'Invalid routing number' };
    }

    const txCode = req.accountType === 'savings' ? TX_CODES.SAVINGS_CREDIT : TX_CODES.CHECKING_CREDIT;
    const traceNumber = this.generateTraceNumber();

    const entry: NachaEntry = {
      transactionCode: txCode,
      routingNumber: req.routingNumber,
      accountNumber: req.accountNumber,
      amount: req.amount,
      name: req.accountHolderName,
      traceNumber,
      addenda: req.addenda,
    };

    const nachaContent = this.generateNachaFile([entry]);
    const batchId = `ACH-${Date.now()}`;

    logger.info('ACH credit created', { traceNumber, amount: req.amount / 100, batchId });

    return {
      success: true,
      traceNumber,
      batchId,
      responseMessage: 'ACH credit entry created',
    };
  }
}
