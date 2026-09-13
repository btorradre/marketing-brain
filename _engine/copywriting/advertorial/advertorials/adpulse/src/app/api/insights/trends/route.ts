import { NextRequest, NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import { authOptions } from "@/lib/auth";
import { prisma } from "@/lib/prisma";

export async function GET(req: NextRequest) {
  const session = await getServerSession(authOptions);
  if (!session?.user) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const { searchParams } = new URL(req.url);
  const accountId = searchParams.get("accountId");
  const dimension = searchParams.get("dimension") || "assetType";

  if (!accountId) {
    return NextResponse.json({ error: "accountId required" }, { status: 400 });
  }

  // Get win rate caches with computed dates
  const caches = await prisma.winRateCache.findMany({
    where: {
      adAccountId: accountId,
      dimension,
    },
    orderBy: { computedAt: "asc" },
  });

  // Group by dimensionValue for trend lines
  const winRateTrends: Record<string, Array<{ date: string; winRate: number }>> = {};
  for (const cache of caches) {
    const key = cache.dimensionValue;
    if (!winRateTrends[key]) winRateTrends[key] = [];
    winRateTrends[key].push({
      date: cache.computedAt.toISOString().split("T")[0],
      winRate: cache.winRate,
    });
  }

  // Fatigue detection: find ads where recent ROAS < older ROAS
  const ads = await prisma.ad.findMany({
    where: {
      adSet: { campaign: { adAccountId: accountId } },
    },
    include: {
      performanceSnapshots: {
        orderBy: { createdAt: "desc" },
        take: 2,
      },
    },
  });

  const fatigueAlerts: Array<{ adId: string; adName: string; roasDecline: number; spend: number }> = [];
  const risingStars: Array<{ adId: string; adName: string; roasIncrease: number; spend: number }> = [];

  for (const ad of ads) {
    if (ad.performanceSnapshots.length < 2) continue;
    const recent = ad.performanceSnapshots[0];
    const older = ad.performanceSnapshots[1];

    if (older.roas > 0 && recent.spend > 50) {
      const change = (recent.roas - older.roas) / older.roas;
      if (change < -0.2) {
        fatigueAlerts.push({
          adId: ad.id,
          adName: ad.name,
          roasDecline: Math.abs(change),
          spend: recent.spend,
        });
      } else if (change > 0.2) {
        risingStars.push({
          adId: ad.id,
          adName: ad.name,
          roasIncrease: change,
          spend: recent.spend,
        });
      }
    }
  }

  // Sort fatigue by decline severity and rising stars by improvement
  fatigueAlerts.sort((a, b) => b.roasDecline - a.roasDecline);
  risingStars.sort((a, b) => b.roasIncrease - a.roasIncrease);

  // Creative velocity
  const sevenDaysAgo = new Date();
  sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7);

  const newAds = await prisma.ad.count({
    where: {
      adSet: { campaign: { adAccountId: accountId } },
      createdAt: { gte: sevenDaysAgo },
    },
  });

  return NextResponse.json({
    winRateTrends,
    fatigueAlerts: fatigueAlerts.slice(0, 10),
    risingStars: risingStars.slice(0, 10),
    velocity: {
      newAds,
      killedAds: fatigueAlerts.length,
      period: "7 days",
    },
  });
}
