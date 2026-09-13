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

  if (!accountId) {
    return NextResponse.json({ error: "accountId required" }, { status: 400 });
  }

  // Get all ads with snapshots for KPI computation
  const ads = await prisma.ad.findMany({
    where: {
      adSet: {
        campaign: { adAccountId: accountId },
      },
    },
    include: {
      performanceSnapshots: {
        where: { dateRange: "LIFETIME" },
        take: 1,
        orderBy: { createdAt: "desc" },
      },
    },
  });

  let totalSpend = 0;
  let totalImpressions = 0;
  let totalClicks = 0;
  let totalPurchases = 0;
  let totalPurchaseValue = 0;
  let totalVideoViews = 0;
  let totalThruPlays = 0;
  let weightedRoas = 0;
  let weightedCtr = 0;
  let weightedCpc = 0;
  let weightedHookRate = 0;
  let weightedHoldRate = 0;

  for (const ad of ads) {
    const snap = ad.performanceSnapshots[0];
    if (!snap) continue;

    totalSpend += snap.spend;
    totalImpressions += snap.impressions;
    totalClicks += snap.clicks;
    totalPurchases += snap.purchases;
    totalPurchaseValue += snap.purchaseValue;
    totalVideoViews += snap.videoViews;
    totalThruPlays += snap.thruPlays;
    weightedRoas += snap.roas * snap.spend;
    weightedCtr += snap.ctr * snap.impressions;
    weightedCpc += snap.cpc * snap.clicks;
    weightedHookRate += snap.hookRate * snap.impressions;
    weightedHoldRate += snap.holdRate * snap.videoViews;
  }

  const avgRoas = totalSpend > 0 ? weightedRoas / totalSpend : 0;
  const avgCtr = totalImpressions > 0 ? weightedCtr / totalImpressions : 0;
  const avgCpc = totalClicks > 0 ? weightedCpc / totalClicks : 0;
  const avgHookRate = totalImpressions > 0 ? weightedHookRate / totalImpressions : 0;
  const avgHoldRate = totalVideoViews > 0 ? weightedHoldRate / totalVideoViews : 0;
  const costPerPurchase = totalPurchases > 0 ? totalSpend / totalPurchases : 0;

  // Simple previous period comparison (mock for now — in production, query previous period)
  const changeFactor = () => (Math.random() * 0.4 - 0.15);

  const kpis = [
    { label: "Total Spend", value: totalSpend, previousValue: totalSpend * (1 - changeFactor()), format: "currency", change: changeFactor() },
    { label: "Avg ROAS", value: avgRoas, previousValue: avgRoas * (1 - changeFactor()), format: "roas", change: changeFactor() },
    { label: "Avg CTR", value: avgCtr, previousValue: avgCtr * (1 - changeFactor()), format: "percent", change: changeFactor() },
    { label: "Avg CPC", value: avgCpc, previousValue: avgCpc * (1 + changeFactor()), format: "currency", change: -changeFactor() },
    { label: "Hook Rate", value: avgHookRate, previousValue: avgHookRate * (1 - changeFactor()), format: "percent", change: changeFactor() },
    { label: "Hold Rate", value: avgHoldRate, previousValue: avgHoldRate * (1 - changeFactor()), format: "percent", change: changeFactor() },
    { label: "Purchases", value: totalPurchases, previousValue: totalPurchases * (1 - changeFactor()), format: "number", change: changeFactor() },
    { label: "Cost/Purchase", value: costPerPurchase, previousValue: costPerPurchase * (1 + changeFactor()), format: "currency", change: -changeFactor() },
  ];

  return NextResponse.json({ kpis });
}
