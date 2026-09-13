"use client";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";
import type { WinRateData } from "@/types";
import { formatCurrency, formatPercent } from "@/lib/utils";

interface WinRateChartProps {
  data: WinRateData[];
  onBarClick?: (dimensionValue: string) => void;
}

function CustomTooltip({ active, payload }: any) {
  if (!active || !payload?.length) return null;

  const d = payload[0].payload as WinRateData;
  return (
    <div className="rounded-lg border border-border bg-card p-3 shadow-lg">
      <p className="mb-2 font-semibold text-foreground">{d.displayName}</p>
      <div className="space-y-1 text-sm">
        <div className="flex justify-between gap-6">
          <span className="text-muted-foreground">Win Rate</span>
          <span className="font-medium text-foreground">
            {(d.winRate * 100).toFixed(0)}%
          </span>
        </div>
        <div className="flex justify-between gap-6">
          <span className="text-muted-foreground">Avg ROAS</span>
          <span className="font-medium text-foreground">
            {d.avgRoas.toFixed(2)}x
          </span>
        </div>
        <div className="flex justify-between gap-6">
          <span className="text-muted-foreground">Ads</span>
          <span className="font-medium text-foreground">{d.adCount}</span>
        </div>
        <div className="flex justify-between gap-6">
          <span className="text-muted-foreground">Total Spend</span>
          <span className="font-medium text-foreground">
            {formatCurrency(d.totalSpend)}
          </span>
        </div>
        <div className="flex justify-between gap-6">
          <span className="text-muted-foreground">Avg CTR</span>
          <span className="font-medium text-foreground">
            {formatPercent(d.avgCtr)}
          </span>
        </div>
      </div>
    </div>
  );
}

function getBarColor(winRate: number): string {
  if (winRate >= 0.6) return "hsl(142, 71%, 45%)"; // green
  if (winRate >= 0.4) return "hsl(38, 92%, 50%)"; // amber
  return "hsl(0, 63%, 51%)"; // red
}

export function WinRateChart({ data, onBarClick }: WinRateChartProps) {
  const sortedData = [...data].sort((a, b) => b.winRate - a.winRate);

  return (
    <ResponsiveContainer width="100%" height={Math.max(300, sortedData.length * 44)}>
      <BarChart
        data={sortedData}
        layout="vertical"
        margin={{ top: 0, right: 20, bottom: 0, left: 0 }}
      >
        <CartesianGrid
          strokeDasharray="3 3"
          horizontal={false}
          stroke="hsl(217, 33%, 17%)"
        />
        <XAxis
          type="number"
          domain={[0, 1]}
          tickFormatter={(v) => `${(v * 100).toFixed(0)}%`}
          stroke="hsl(215, 20%, 55%)"
          fontSize={12}
        />
        <YAxis
          type="category"
          dataKey="displayName"
          width={180}
          stroke="hsl(215, 20%, 55%)"
          fontSize={12}
          tick={{ fill: "hsl(210, 40%, 98%)" }}
        />
        <Tooltip content={<CustomTooltip />} />
        <Bar
          dataKey="winRate"
          radius={[0, 4, 4, 0]}
          cursor="pointer"
          onClick={(data) => onBarClick?.(data.dimensionValue)}
        >
          {sortedData.map((entry, index) => (
            <Cell key={index} fill={getBarColor(entry.winRate)} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}
