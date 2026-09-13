"use client";

import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { WinRateChart } from "@/components/charts/win-rate-chart";
import type { WinRateData } from "@/types";

interface WinRateSectionProps {
  winRates: Record<string, WinRateData[]>;
}

const dimensionLabels: Record<string, string> = {
  assetType: "Asset Type",
  messagingAngle: "Messaging Angle",
  hookTactic: "Hook Tactic",
  visualStyle: "Visual Style",
  emotionalTone: "Emotional Tone",
  productPresentation: "Product Presentation",
};

export function WinRateSection({ winRates }: WinRateSectionProps) {
  const dimensions = Object.keys(winRates);

  if (dimensions.length === 0) {
    return (
      <Card>
        <CardContent className="flex h-48 items-center justify-center">
          <p className="text-muted-foreground">No win rate data available yet. Run an analysis to see results.</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Win Rate Breakdown</CardTitle>
      </CardHeader>
      <CardContent>
        <Tabs defaultValue={dimensions[0]}>
          <TabsList className="mb-4 flex-wrap">
            {dimensions.map((dim) => (
              <TabsTrigger key={dim} value={dim} className="text-xs">
                {dimensionLabels[dim] || dim}
              </TabsTrigger>
            ))}
          </TabsList>
          {dimensions.map((dim) => (
            <TabsContent key={dim} value={dim}>
              <WinRateChart data={winRates[dim]} />
            </TabsContent>
          ))}
        </Tabs>
      </CardContent>
    </Card>
  );
}
