import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatCurrency(value: number): string {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    minimumFractionDigits: 0,
    maximumFractionDigits: 2,
  }).format(value);
}

export function formatPercent(value: number): string {
  return `${(value * 100).toFixed(1)}%`;
}

export function formatNumber(value: number): string {
  if (value >= 1_000_000) return `${(value / 1_000_000).toFixed(1)}M`;
  if (value >= 1_000) return `${(value / 1_000).toFixed(1)}K`;
  return value.toFixed(value % 1 === 0 ? 0 : 2);
}

export function formatRoas(value: number): string {
  return `${value.toFixed(2)}x`;
}

export function getVerdictColor(verdict: string): string {
  switch (verdict) {
    case "SCALE":
      return "text-green-400";
    case "TEST":
      return "text-amber-400";
    case "KILL":
      return "text-red-400";
    default:
      return "text-muted-foreground";
  }
}

export function getVerdictEmoji(verdict: string): string {
  switch (verdict) {
    case "SCALE":
      return "🟢";
    case "TEST":
      return "🟡";
    case "KILL":
      return "🔴";
    default:
      return "⚪";
  }
}

export function calculateVerdict(
  adRoas: number,
  accountAvgRoas: number,
  adCtr: number,
  accountAvgCtr: number,
  spend: number
): "SCALE" | "TEST" | "KILL" {
  const roasRatio = accountAvgRoas > 0 ? adRoas / accountAvgRoas : 0;
  const minSpendThreshold = 50;

  if (spend < minSpendThreshold) return "TEST";

  if (roasRatio >= 1.3 && spend >= 100) return "SCALE";
  if (roasRatio >= 1.5) return "SCALE";

  if (roasRatio < 0.5 && spend >= 100) return "KILL";
  if (roasRatio < 0.7 && spend >= 200) return "KILL";
  if (adRoas < 1.0 && spend >= 150) return "KILL";

  return "TEST";
}

export function detectFunnelStage(
  objective: string | null,
  campaignName: string
): "TOF" | "MOF" | "BOF" {
  const name = campaignName.toLowerCase();
  const obj = (objective || "").toUpperCase();

  // BOF detection
  if (
    ["CONVERSIONS", "CATALOG_SALES", "STORE_TRAFFIC", "OUTCOME_SALES"].includes(obj) ||
    /\b(bof|bottom|purchase|conversion|dpa|catalog|hot)\b/.test(name)
  ) {
    return "BOF";
  }

  // MOF detection
  if (
    ["ENGAGEMENT", "LEAD_GENERATION", "OUTCOME_ENGAGEMENT", "OUTCOME_LEADS"].includes(obj) ||
    /\b(mof|middle|retarget|engaged|warm)\b/.test(name)
  ) {
    return "MOF";
  }

  // Default to TOF
  return "TOF";
}

export function slugify(text: string): string {
  return text
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "_")
    .replace(/^_|_$/g, "");
}
