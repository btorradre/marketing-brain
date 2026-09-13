"use client";

import { useEffect, useState } from "react";
import { useSession } from "next-auth/react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { TrendingUp, TrendingDown, AlertTriangle, Star } from "lucide-react";
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Legend,
} from "recharts";

const COLORS = [
  "hsl(217, 91%, 60%)",
  "hsl(142, 71%, 45%)",
  "hsl(38, 92%, 50%)",
  "hsl(0, 63%, 51%)",
  "hsl(280, 65%, 60%)",
  "hsl(190, 80%, 50%)",
  "hsl(330, 80%, 60%)",
];

interface TrendData {
  fatigueAlerts: Array<{ adId: string; adName: string; roasDecline: number; spend: number }>;
  risingStars: Array<{ adId: string; adName: string; roasIncrease: number; spend: number }>;
  winRateTrends: Record<string, Array<{ date: string; winRate: number }>>;
  velocity: { newAds: number; killedAds: number; period: string };
}

export default function TrendsPage() {
  const { data: session } = useSession();
  const [loading, setLoading] = useState(true);
  const [accountId, setAccountId] = useState("");
  const [dimension, setDimension] = useState("assetType");
  const [data, setData] = useState<TrendData | null>(null);

  useEffect(() => {
    async function loadAccount() {
      const res = await fetch("/api/accounts");
      const accounts = await res.json();
      if (accounts.length > 0) setAccountId(accounts[0].id);
    }
    if (session) loadAccount();
  }, [session]);

  useEffect(() => {
    async function loadTrends() {
      if (!accountId) return;
      setLoading(true);
      try {
        const res = await fetch(
          `/api/insights/trends?accountId=${accountId}&dimension=${dimension}`
        );
        const result = await res.json();
        setData(result);
      } catch {
        console.error("Failed to load trends");
      } finally {
        setLoading(false);
      }
    }
    loadTrends();
  }, [accountId, dimension]);

  if (loading) {
    return (
      <div className="flex h-[80vh] items-center justify-center">
        <div className="h-8 w-8 animate-spin rounded-full border-2 border-primary border-t-transparent" />
      </div>
    );
  }

  // Build chart data from winRateTrends
  const trendKeys = data?.winRateTrends ? Object.keys(data.winRateTrends) : [];
  const chartData: Array<Record<string, any>> = [];

  if (data?.winRateTrends && trendKeys.length > 0) {
    const allDates = new Set<string>();
    for (const key of trendKeys) {
      for (const point of data.winRateTrends[key]) {
        allDates.add(point.date);
      }
    }
    const sortedDates = [...allDates].sort();
    for (const date of sortedDates) {
      const entry: Record<string, any> = { date };
      for (const key of trendKeys) {
        const point = data.winRateTrends[key].find((p) => p.date === date);
        entry[key] = point ? point.winRate : null;
      }
      chartData.push(entry);
    }
  }

  return (
    <div className="p-6">
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Trends</h1>
          <p className="text-sm text-muted-foreground">
            Track creative performance trends and detect fatigue.
          </p>
        </div>
        <Select value={dimension} onValueChange={setDimension}>
          <SelectTrigger className="w-[200px]">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="assetType">Asset Type</SelectItem>
            <SelectItem value="messagingAngle">Messaging Angle</SelectItem>
            <SelectItem value="hookTactic">Hook Tactic</SelectItem>
            <SelectItem value="visualStyle">Visual Style</SelectItem>
            <SelectItem value="emotionalTone">Emotional Tone</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        {/* Win Rate Trends Chart */}
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle>Win Rate Over Time by {dimension.replace(/([A-Z])/g, " $1").trim()}</CardTitle>
          </CardHeader>
          <CardContent>
            {chartData.length > 0 ? (
              <ResponsiveContainer width="100%" height={400}>
                <LineChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="hsl(217, 33%, 17%)" />
                  <XAxis dataKey="date" stroke="hsl(215, 20%, 55%)" fontSize={12} />
                  <YAxis
                    tickFormatter={(v) => `${(v * 100).toFixed(0)}%`}
                    stroke="hsl(215, 20%, 55%)"
                    fontSize={12}
                  />
                  <Tooltip
                    contentStyle={{
                      background: "hsl(222, 47%, 8%)",
                      border: "1px solid hsl(217, 33%, 17%)",
                      borderRadius: "8px",
                    }}
                    formatter={(value: number) => [`${(value * 100).toFixed(1)}%`, ""]}
                  />
                  <Legend />
                  {trendKeys.map((key, i) => (
                    <Line
                      key={key}
                      type="monotone"
                      dataKey={key}
                      name={key.replace(/_/g, " ")}
                      stroke={COLORS[i % COLORS.length]}
                      strokeWidth={2}
                      dot={false}
                      connectNulls
                    />
                  ))}
                </LineChart>
              </ResponsiveContainer>
            ) : (
              <div className="flex h-48 items-center justify-center">
                <p className="text-muted-foreground">No trend data available yet.</p>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Creative Fatigue Alerts */}
        <Card className="border-amber-500/20">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-amber-400">
              <AlertTriangle className="h-5 w-5" />
              Creative Fatigue
            </CardTitle>
          </CardHeader>
          <CardContent>
            {data?.fatigueAlerts && data.fatigueAlerts.length > 0 ? (
              <div className="space-y-3">
                {data.fatigueAlerts.map((alert) => (
                  <div
                    key={alert.adId}
                    className="flex items-center justify-between rounded-lg border border-border p-3"
                  >
                    <div>
                      <p className="text-sm font-medium">{alert.adName}</p>
                      <p className="text-xs text-muted-foreground">
                        ${alert.spend.toFixed(0)} spend
                      </p>
                    </div>
                    <Badge variant="warning">
                      <TrendingDown className="mr-1 h-3 w-3" />
                      {(alert.roasDecline * 100).toFixed(0)}% decline
                    </Badge>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-sm text-muted-foreground">
                No fatigue signals detected.
              </p>
            )}
          </CardContent>
        </Card>

        {/* Rising Stars */}
        <Card className="border-green-500/20">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-green-400">
              <Star className="h-5 w-5" />
              Rising Stars
            </CardTitle>
          </CardHeader>
          <CardContent>
            {data?.risingStars && data.risingStars.length > 0 ? (
              <div className="space-y-3">
                {data.risingStars.map((star) => (
                  <div
                    key={star.adId}
                    className="flex items-center justify-between rounded-lg border border-border p-3"
                  >
                    <div>
                      <p className="text-sm font-medium">{star.adName}</p>
                      <p className="text-xs text-muted-foreground">
                        ${star.spend.toFixed(0)} spend
                      </p>
                    </div>
                    <Badge variant="success">
                      <TrendingUp className="mr-1 h-3 w-3" />
                      +{(star.roasIncrease * 100).toFixed(0)}% ROAS
                    </Badge>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-sm text-muted-foreground">
                No rising stars detected yet.
              </p>
            )}
          </CardContent>
        </Card>

        {/* Creative Velocity */}
        {data?.velocity && (
          <Card className="lg:col-span-2">
            <CardHeader>
              <CardTitle>Creative Velocity (Last {data.velocity.period})</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 gap-4">
                <div className="rounded-lg border border-border p-4 text-center">
                  <p className="text-3xl font-bold text-green-400">
                    {data.velocity.newAds}
                  </p>
                  <p className="text-sm text-muted-foreground">
                    New Ads Launched
                  </p>
                </div>
                <div className="rounded-lg border border-border p-4 text-center">
                  <p className="text-3xl font-bold text-red-400">
                    {data.velocity.killedAds}
                  </p>
                  <p className="text-sm text-muted-foreground">Ads Killed</p>
                </div>
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}
