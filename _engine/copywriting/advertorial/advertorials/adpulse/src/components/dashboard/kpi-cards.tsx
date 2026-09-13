"use client";

import { Card, CardContent } from "@/components/ui/card";
import { formatCurrency, formatPercent, formatNumber, formatRoas } from "@/lib/utils";
import { TrendingUp, TrendingDown, Minus } from "lucide-react";
import type { KPIData } from "@/types";

interface KPICardsProps {
  data: KPIData[];
}

function formatValue(value: number, format: string): string {
  switch (format) {
    case "currency":
      return formatCurrency(value);
    case "percent":
      return formatPercent(value);
    case "roas":
      return formatRoas(value);
    case "number":
      return formatNumber(value);
    default:
      return value.toString();
  }
}

export function KPICards({ data }: KPICardsProps) {
  return (
    <div className="grid grid-cols-2 gap-4 md:grid-cols-4 lg:grid-cols-8">
      {data.map((kpi) => {
        const isPositive = kpi.change > 0;
        const isNeutral = kpi.change === 0;

        return (
          <Card key={kpi.label} className="bg-card">
            <CardContent className="p-4">
              <p className="text-xs font-medium text-muted-foreground">
                {kpi.label}
              </p>
              <p className="mt-1 text-xl font-bold">
                {formatValue(kpi.value, kpi.format)}
              </p>
              <div className="mt-1 flex items-center gap-1">
                {isNeutral ? (
                  <Minus className="h-3 w-3 text-muted-foreground" />
                ) : isPositive ? (
                  <TrendingUp className="h-3 w-3 text-green-400" />
                ) : (
                  <TrendingDown className="h-3 w-3 text-red-400" />
                )}
                <span
                  className={`text-xs font-medium ${
                    isNeutral
                      ? "text-muted-foreground"
                      : isPositive
                        ? "text-green-400"
                        : "text-red-400"
                  }`}
                >
                  {isPositive ? "+" : ""}
                  {(kpi.change * 100).toFixed(1)}%
                </span>
              </div>
            </CardContent>
          </Card>
        );
      })}
    </div>
  );
}
