"use client";

import { useEffect, useState, useCallback } from "react";
import { useSession } from "next-auth/react";
import { Header } from "@/components/layout/header";
import { KPICards } from "@/components/dashboard/kpi-cards";
import { WinRateSection } from "@/components/dashboard/win-rate-section";
import { CreativeTable } from "@/components/dashboard/creative-table";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import type { KPIData, WinRateData, AdWithAnalysis } from "@/types";

export default function DashboardPage() {
  const { data: session } = useSession();
  const [accounts, setAccounts] = useState<Array<{ id: string; metaAccountName: string }>>([]);
  const [accountId, setAccountId] = useState<string>("");
  const [dateRange, setDateRange] = useState("30D");
  const [funnelStage, setFunnelStage] = useState("ALL");
  const [kpis, setKpis] = useState<KPIData[]>([]);
  const [winRates, setWinRates] = useState<Record<string, WinRateData[]>>({});
  const [ads, setAds] = useState<AdWithAnalysis[]>([]);
  const [loading, setLoading] = useState(true);
  const [isRefreshing, setIsRefreshing] = useState(false);

  // Load accounts
  useEffect(() => {
    async function loadAccounts() {
      try {
        const res = await fetch("/api/accounts");
        const data = await res.json();
        setAccounts(data);
        if (data.length > 0 && !accountId) {
          setAccountId(data[0].id);
        }
      } catch {
        console.error("Failed to load accounts");
      }
    }
    if (session) loadAccounts();
  }, [session]);

  // Load dashboard data
  const loadData = useCallback(async () => {
    if (!accountId) {
      setLoading(false);
      return;
    }

    setLoading(true);
    try {
      const [summaryRes, winRateRes, adsRes] = await Promise.all([
        fetch(`/api/insights/summary?accountId=${accountId}&dateRange=${dateRange}&funnelStage=${funnelStage}`),
        fetch(`/api/insights/winrates?accountId=${accountId}&dateRange=${dateRange}&funnelStage=${funnelStage}`),
        fetch(`/api/ads?accountId=${accountId}&dateRange=${dateRange}&funnelStage=${funnelStage}`),
      ]);

      const [summaryData, winRateData, adsData] = await Promise.all([
        summaryRes.json(),
        winRateRes.json(),
        adsRes.json(),
      ]);

      setKpis(summaryData.kpis || []);
      setWinRates(winRateData || {});
      setAds(adsData.ads || []);
    } catch (err) {
      console.error("Failed to load dashboard data:", err);
    } finally {
      setLoading(false);
    }
  }, [accountId, dateRange, funnelStage]);

  useEffect(() => {
    loadData();
  }, [loadData]);

  async function handleRefresh() {
    setIsRefreshing(true);
    // In production, this would trigger a sync job
    await loadData();
    setIsRefreshing(false);
  }

  if (loading && ads.length === 0) {
    return (
      <div>
        <Header
          accountId={accountId}
          accounts={accounts}
          onAccountChange={setAccountId}
          dateRange={dateRange}
          onDateRangeChange={setDateRange}
          funnelStage={funnelStage}
          onFunnelStageChange={setFunnelStage}
        />
        <div className="flex h-[80vh] items-center justify-center">
          <div className="text-center">
            <div className="mx-auto mb-4 h-8 w-8 animate-spin rounded-full border-2 border-primary border-t-transparent" />
            <p className="text-muted-foreground">Loading dashboard...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div>
      <Header
        accountId={accountId}
        accounts={accounts}
        onAccountChange={setAccountId}
        dateRange={dateRange}
        onDateRangeChange={setDateRange}
        funnelStage={funnelStage}
        onFunnelStageChange={setFunnelStage}
        onRefresh={handleRefresh}
        isRefreshing={isRefreshing}
      />

      <div className="space-y-6 p-6">
        {/* KPI Cards */}
        {kpis.length > 0 && <KPICards data={kpis} />}

        {/* Win Rate Breakdown */}
        <WinRateSection winRates={winRates} />

        {/* Creative Performance Table */}
        <Card>
          <CardHeader>
            <CardTitle>Creative Performance</CardTitle>
          </CardHeader>
          <CardContent>
            <CreativeTable ads={ads} />
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
