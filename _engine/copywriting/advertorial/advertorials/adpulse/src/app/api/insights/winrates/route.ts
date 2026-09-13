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
  const funnelStage = searchParams.get("funnelStage") || "ALL";
  const dateRange = searchParams.get("dateRange") || "30D";

  if (!accountId) {
    return NextResponse.json({ error: "accountId required" }, { status: 400 });
  }

  const caches = await prisma.winRateCache.findMany({
    where: {
      adAccountId: accountId,
      funnelStage: funnelStage as any,
      dateRange,
    },
    orderBy: { winRate: "desc" },
  });

  // Group by dimension
  const grouped: Record<string, any[]> = {};
  for (const cache of caches) {
    if (!grouped[cache.dimension]) grouped[cache.dimension] = [];
    grouped[cache.dimension].push({
      dimension: cache.dimension,
      dimensionValue: cache.dimensionValue,
      displayName: cache.dimensionValue.replace(/_/g, " "),
      adCount: cache.adCount,
      totalSpend: cache.totalSpend,
      avgRoas: cache.avgRoas,
      avgCtr: cache.avgCtr,
      avgCpc: cache.avgCpc,
      avgHookRate: cache.avgHookRate,
      avgHoldRate: cache.avgHoldRate,
      winRate: cache.winRate,
    });
  }

  return NextResponse.json(grouped);
}
