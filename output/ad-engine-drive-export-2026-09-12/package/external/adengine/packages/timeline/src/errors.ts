export type OpErrorCode =
  | 'NOT_FOUND'
  | 'DUPLICATE_ID'
  | 'OVERLAP'
  | 'INVALID_RANGE'
  | 'SOURCE_BOUNDS'
  | 'LOCKED'
  | 'INVALID_OP'
  | 'NOT_ADJACENT'
  | 'KIND_MISMATCH'
  | 'REFERENCED'
  | 'UNJOINABLE'
  | 'UNDO_CONFLICT'
  | 'NOTHING_TO_UNDO'
  | 'INVALID_DOCUMENT';

export class OpError extends Error {
  readonly code: OpErrorCode;
  readonly opId: string | undefined;
  readonly details: Record<string, unknown> | undefined;

  constructor(code: OpErrorCode, message: string, opts?: { opId?: string; details?: Record<string, unknown> }) {
    super(`${code}: ${message}`);
    this.name = 'OpError';
    this.code = code;
    this.opId = opts?.opId;
    this.details = opts?.details;
  }
}

export function isOpError(e: unknown): e is OpError {
  return e instanceof OpError;
}
