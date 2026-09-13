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
  const funnelStage = searchParams.get("funnelStage");
  const dateRange = searchParams.get("dateRange") || "30D";

  if (!accountId) {
    return NextResponse.json({ error: "accountId required" }, { status: 400 });
  }

  // Verify account belongs to user
  const account = await prisma.adAccount.findFirst({
    where: {
      id: accountId,
      userId: (session.user as any).id,
    },
  });

  if (!account) {
    return NextResponse.json({ error: "Account not found" }, { status: 404 });
  }

  // Build campaign filter
  const campaignWhere: any = { adAccountId: accountId };
  if (funnelStage && funnelStage !== "ALL") {
    campaignWhere.funnelStage = funnelStage;
  }

  // Fetch ads with relations
  const ads = await prisma.ad.findMany({
    where: {
      adSet: {
        campaign: campaignWhere,
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

  // Compute account averages for verdict calculation
  let totalSpend = 0;
  let totalRoasWeighted = 0;
  let totalCtrWeighted = 0;
  let totalImpressions = 0;

  for (const ad of ads) {
    const snap = ad.performanceSnapshots[0];
    if (snap) {
      totalSpend += snap.spend;
      totalRoasWeighted += snap.roas * snap.spend;
      totalCtrWeighted += snap.ctr * snap.impressions;
      totalImpressions += snap.impressions;
    }
  }

  const accountAvgRoas = totalSpend > 0 ? totalRoasWeighted / totalSpend : 0;
  const accountAvgCtr = totalImpressions > 0 ? totalCtrWeighted / totalImpressions : 0;

  // Transform response
  const result = ads.map((ad) => {
    const snap = ad.performanceSnapshots[0];
    const spend = snap?.spend || 0;
    const roas = snap?.roas || 0;
    const ctr = snap?.ctr || 0;
    const cpc = snap?.cpc || 0;
    const hookRate = snap?.hookRate || 0;
    const holdRate = snap?.holdRate || 0;

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
      funnelStage: ad.adSet.campaign.funnelStage,
      campaignName: ad.adSet.campaign.name,
      spend,
      roas,
      ctr,
      cpc,
      hookRate,
      holdRate,
      purchases: snap?.purchases || 0,
      impressions: snap?.impressions || 0,
      verdict: calculateVerdict(roas, accountAvgRoas, ctr, accountAvgCtr, spend),
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

  return NextResponse.json({
    ads: result,
    accountAvgRoas,
    accountAvgCtr,
    totalAds: result.length,
  });
}
