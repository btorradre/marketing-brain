import { NextRequest, NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import { authOptions } from "@/lib/auth";
import { prisma } from "@/lib/prisma";
import { calculateVerdict } from "@/lib/utils";

function safeJsonParse(val: string | null | undefined, fallback: any) {
  if (!val) return fallback;
  try { return JSON.parse(val); } catch { return fallback; }
}

export async function GET(req: NextRequest) {
  const session = await getServerSession(authOptions);
  if (!session?.user) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const { searchParams } = new URL(req.url);
  const accountId = searchParams.get("accountId");

  if (!accountId) {
    return NextResponse.json({ error: "accountId required" }, { status: 400 });
  }

  // Get all ads with their data
  const ads = await prisma.ad.findMany({
    where: {
      adSet: {
        campaign: { adAccountId: accountId },
      },
    },
    include: {
      creativeAnalysis: true,
      performanceSnapshots: {
        where: { dateRange: "LIFETIME" },
        take: 1,
        orderBy: { createdAt: "desc" },
      },
      adSet: {
        include: {
          campaign: { select: { name: true, funnelStage: true } },
        },
      },
    },
  });

  // Compute account averages
  let totalSpend = 0;
  let weightedRoas = 0;
  let weightedCtr = 0;
  let totalImps = 0;

  for (const ad of ads) {
    const snap = ad.performanceSnapshots[0];
    if (snap) {
      totalSpend += snap.spend;
      weightedRoas += snap.roas * snap.spend;
      weightedCtr += snap.ctr * snap.impressions;
      totalImps += snap.impressions;
    }
  }

  const avgRoas = totalSpend > 0 ? weightedRoas / totalSpend : 0;
  const avgCtr = totalImps > 0 ? weightedCtr / totalImps : 0;

  // Transform and categorize
  const stages = ["TOF", "MOF", "BOF"] as const;
  const recommendations = stages.map((stage) => {
    const stageAds = ads
      .filter((a) => a.adSet.campaign.funnelStage === stage)
      .map((ad) => {
        const snap = ad.performanceSnapshots[0];
        const spend = snap?.spend || 0;
        const roas = snap?.roas || 0;
        const ctr = snap?.ctr || 0;

        return {
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
          funnelStage: stage,
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
        };
      });

    const killList = stageAds
      .filter((a) => a.verdict === "KILL")
      .sort((a, b) => b.spend - a.spend);
    const scaleList = stageAds
      .filter((a) => a.verdict === "SCALE")
      .sort((a, b) => b.roas - a.roas);
    const iterateList = stageAds
      .filter((a) => a.verdict === "TEST" && a.analysis?.aiIterationIdeas?.length)
      .sort((a, b) => b.spend - a.spend);

    const totalWaste = killList.reduce((sum, ad) => {
      const breakEvenDelta = ad.roas < 1 ? ad.spend * (1 - ad.roas) : 0;
      return sum + breakEvenDelta;
    }, 0);

    // Generate strategic recommendations based on data
    const strategicRecommendations: string[] = [];

    // Find winning asset type for this stage
    const assetTypeCounts: Record<string, { wins: number; total: number }> = {};
    for (const ad of stageAds) {
      const at = ad.analysis?.assetType || "OTHER";
      if (!assetTypeCounts[at]) assetTypeCounts[at] = { wins: 0, total: 0 };
      assetTypeCounts[at].total++;
      if (ad.roas > avgRoas) assetTypeCounts[at].wins++;
    }

    const topAssetType = Object.entries(assetTypeCounts)
      .map(([type, data]) => ({ type, winRate: data.total > 0 ? data.wins / data.total : 0, count: data.total }))
      .sort((a, b) => b.winRate - a.winRate)[0];

    if (topAssetType && topAssetType.count >= 2) {
      strategicRecommendations.push(
        `Your best performing creative type for ${stage} is ${topAssetType.type.replace(/_/g, " ")} with a ${(topAssetType.winRate * 100).toFixed(0)}% win rate. Consider producing more variations of this type.`
      );
    }

    // Find winning messaging angle
    const angleCounts: Record<string, { wins: number; total: number }> = {};
    for (const ad of stageAds) {
      const angle = ad.analysis?.messagingAngle || "FEATURE_BENEFIT";
      if (!angleCounts[angle]) angleCounts[angle] = { wins: 0, total: 0 };
      angleCounts[angle].total++;
      if (ad.roas > avgRoas) angleCounts[angle].wins++;
    }

    const topAngle = Object.entries(angleCounts)
      .map(([angle, data]) => ({ angle, winRate: data.total > 0 ? data.wins / data.total : 0, count: data.total }))
      .sort((a, b) => b.winRate - a.winRate)[0];

    if (topAngle && topAngle.count >= 2) {
      strategicRecommendations.push(
        `${topAngle.angle.replace(/_/g, " ")} messaging is driving the best results in ${stage}. Test new creative angles that combine this with your top-performing visual styles.`
      );
    }

    if (killList.length > 3) {
      strategicRecommendations.push(
        `You have ${killList.length} underperforming ads in ${stage} wasting $${totalWaste.toFixed(0)}. Reallocating this budget to your top performers could significantly improve overall ROAS.`
      );
    }

    return {
      funnelStage: stage,
      killList,
      scaleList,
      iterateList,
      totalWaste,
      strategicRecommendations,
    };
  });

  return NextResponse.json(recommendations);
}
