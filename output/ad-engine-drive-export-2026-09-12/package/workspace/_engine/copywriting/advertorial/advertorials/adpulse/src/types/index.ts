export type FunnelStage = "TOF" | "MOF" | "BOF" | "ALL";
export type DateRangeOption = "7D" | "14D" | "30D" | "90D" | "ALL";
export type Verdict = "SCALE" | "TEST" | "KILL";

export interface KPIData {
  label: string;
  value: number;
  previousValue: number;
  format: "currency" | "percent" | "number" | "roas";
  change: number;
}

export interface WinRateData {
  dimension: string;
  dimensionValue: string;
  displayName: string;
  adCount: number;
  totalSpend: number;
  avgRoas: number;
  avgCtr: number;
  avgCpc: number;
  avgHookRate: number;
  avgHoldRate: number;
  winRate: number;
}

export interface AdWithAnalysis {
  id: string;
  name: string;
  status: string;
  creativeType: string;
  thumbnailUrl: string | null;
  imageUrl: string | null;
  videoUrl: string | null;
  adCopy: string | null;
  headline: string | null;
  callToAction: string | null;
  funnelStage: string;
  campaignName: string;
  spend: number;
  roas: number;
  ctr: number;
  cpc: number;
  hookRate: number;
  holdRate: number;
  purchases: number;
  impressions: number;
  verdict: Verdict;
  analysis: {
    assetType: string;
    messagingAngle: string;
    hookTactic: string;
    visualStyle: string;
    ctaStyle: string;
    emotionalTone: string;
    productPresentation: string;
    aiSummary: string | null;
    aiStrengths: string[];
    aiWeaknesses: string[];
    aiIterationIdeas: Array<{
      idea: string;
      reasoning: string;
      priority: string;
      estimatedImpact: string;
    }>;
    confidenceScore: number;
    copyAnalysis: any;
  } | null;
}

export interface RecommendationGroup {
  funnelStage: FunnelStage;
  killList: AdWithAnalysis[];
  scaleList: AdWithAnalysis[];
  iterateList: AdWithAnalysis[];
  totalWaste: number;
  strategicRecommendations: string[];
}

export interface TrendDataPoint {
  date: string;
  value: number;
}

export interface TrendSeries {
  dimensionValue: string;
  displayName: string;
  data: TrendDataPoint[];
}
