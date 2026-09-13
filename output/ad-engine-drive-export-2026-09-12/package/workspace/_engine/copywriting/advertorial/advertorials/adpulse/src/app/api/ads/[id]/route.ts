import { NextRequest, NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import { authOptions } from "@/lib/auth";
import { prisma } from "@/lib/prisma";
import { calculateVerdict } from "@/lib/utils";

function safeJsonParse(val: string | null | undefined, fallback: any) {
  if (!val) return fallback;
  try { return JSON.parse(val); } catch { return fallback; }
}

export async function GET(
  req: NextRequest,
  { params }: { params: { id: string } }
) {
  const session = await getServerSession(authOptions);
  if (!session?.user) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const ad = await prisma.ad.findUnique({
    where: { id: params.id },
    include: {
      creativeAnalysis: true,
      performanceSnapshots: {
        where: { dateRange: "LIFETIME" },
        take: 1,
        orderBy: { createdAt: "desc" },
      },
      adSet: {
        include: {
          campaign: {
            include: {
              adAccount: { select: { userId: true } },
            },
          },
        },
      },
    },
  });

  if (!ad || ad.adSet.campaign.adAccount.userId !== (session.user as any).id) {
    return NextResponse.json({ error: "Not found" }, { status: 404 });
  }

  const snap = ad.performanceSnapshots[0];
  const spend = snap?.spend || 0;
  const roas = snap?.roas || 0;
  const ctr = snap?.ctr || 0;

  // Get account averages for verdict
  const allSnapshots = await prisma.performanceSnapshot.findMany({
    where: {
      dateRange: "LIFETIME",
      ad: {
        adSet: {
          campaign: { adAccountId: ad.adSet.campaign.adAccountId },
        },
      },
    },
    select: { spend: true, roas: true, ctr: true, impressions: true },
  });

  let totalSpend = 0;
  let weightedRoas = 0;
  let weightedCtr = 0;
  let totalImps = 0;

  for (const s of allSnapshots) {
    totalSpend += s.spend;
    weightedRoas += s.roas * s.spend;
    weightedCtr += s.ctr * s.impressions;
    totalImps += s.impressions;
  }

  const avgRoas = totalSpend > 0 ? weightedRoas / totalSpend : 0;
  const avgCtr = totalImps > 0 ? weightedCtr / totalImps : 0;

  return NextResponse.json({
    id: ad.id,
    name: ad.name,
    status: ad.status,
    creativeType: ad.creativeType,
    thumbnailUrl: ad.thumbnailUrl,
    imageUrl: ad.imageUrl,
    videoUrl: ad.videoUrl,
    adCopy: ad.adCopy,
    headline: ad.headline,
    callToAction: ad.callToAction,
    funnelStage: ad.adSet.campaign.funnelStage,
    campaignName: ad.adSet.campaign.name,
    spend,
    roas,
    ctr,
    cpc: snap?.cpc || 0,
    hookRate: snap?.hookRate || 0,
    holdRate: snap?.holdRate || 0,
    purchases: snap?.purchases || 0,
    impressions: snap?.impressions || 0,
    verdict: calculateVerdict(roas, avgRoas, ctr, avgCtr, spend),
    analysis: ad.creativeAnalysis
      ? {
          assetType: ad.creativeAnalysis.assetType,
          messagingAngle: ad.creativeAnalysis.messagingAngle,
          hookTactic: ad.creativeAnalysis.hookTactic,
          visualStyle: ad.creativeAnalysis.visualStyle,
          ctaStyle: ad.creativeAnalysis.ctaStyle,
          emotionalTone: ad.creativeAnalysis.emotionalTone,
          productPresentation: ad.creativeAnalysis.productPresentation,
          aiSummary: ad.creativeAnalysis.aiSummary,
          aiStrengths: safeJsonParse(ad.creativeAnalysis.aiStrengths, []),
          aiWeaknesses: safeJsonParse(ad.creativeAnalysis.aiWeaknesses, []),
          aiIterationIdeas: safeJsonParse(ad.creativeAnalysis.aiIterationIdeas, []),
          confidenceScore: ad.creativeAnalysis.confidenceScore,
          copyAnalysis: safeJsonParse(ad.creativeAnalysis.copyAnalysis, null),
        }
      : null,
  });
}
