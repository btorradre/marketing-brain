"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { useSession } from "next-auth/react";
import Link from "next/link";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  ArrowLeft,
  CheckCircle2,
  XCircle,
  Lightbulb,
  BarChart3,
  Play,
} from "lucide-react";
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from "recharts";
import type { AdWithAnalysis } from "@/types";

export default function CreativeDetailPage() {
  const params = useParams();
  const router = useRouter();
  const { data: session } = useSession();
  const [ad, setAd] = useState<AdWithAnalysis | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadAd() {
      try {
        const res = await fetch(`/api/ads/${params.id}`);
        if (!res.ok) throw new Error("Failed to load");
        const data = await res.json();
        setAd(data);
      } catch {
        console.error("Failed to load creative");
      } finally {
        setLoading(false);
      }
    }
    if (session && params.id) loadAd();
  }, [session, params.id]);

  if (loading) {
    return (
      <div className="flex h-[80vh] items-center justify-center">
        <div className="h-8 w-8 animate-spin rounded-full border-2 border-primary border-t-transparent" />
      </div>
    );
  }

  if (!ad) {
    return (
      <div className="flex h-[80vh] flex-col items-center justify-center gap-4">
        <p className="text-muted-foreground">Creative not found</p>
        <Button variant="outline" onClick={() => router.push("/dashboard")}>
          Back to Dashboard
        </Button>
      </div>
    );
  }

  const analysis = ad.analysis;

  return (
    <div className="min-h-screen p-6">
      {/* Back button */}
      <Button
        variant="ghost"
        size="sm"
        className="mb-6"
        onClick={() => router.back()}
      >
        <ArrowLeft className="mr-2 h-4 w-4" />
        Back
      </Button>

      <div className="grid gap-6 lg:grid-cols-2">
        {/* Left: Creative Preview */}
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="text-lg">{ad.name}</CardTitle>
                <div className="flex items-center gap-2">
                  <Badge
                    variant={
                      ad.verdict === "SCALE"
                        ? "success"
                        : ad.verdict === "KILL"
                          ? "danger"
                          : "warning"
                    }
                  >
                    {ad.verdict === "SCALE"
                      ? "🟢 SCALE"
                      : ad.verdict === "KILL"
                        ? "🔴 KILL"
                        : "🟡 TEST"}
                  </Badge>
                  <Badge variant="secondary">{ad.creativeType}</Badge>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              {/* Creative Preview */}
              <div className="relative aspect-video w-full overflow-hidden rounded-lg bg-muted">
                {ad.videoUrl ? (
                  <div className="flex h-full items-center justify-center">
                    <div className="text-center">
                      <Play className="mx-auto mb-2 h-12 w-12 text-muted-foreground" />
                      <p className="text-sm text-muted-foreground">
                        Video Preview
                      </p>
                    </div>
                  </div>
                ) : ad.imageUrl || ad.thumbnailUrl ? (
                  <img
                    src={ad.imageUrl || ad.thumbnailUrl || ""}
                    alt={ad.name}
                    className="h-full w-full object-cover"
                  />
                ) : (
                  <div className="flex h-full items-center justify-center bg-gradient-to-br from-primary/20 to-primary/5">
                    <p className="text-lg font-semibold text-muted-foreground">
                      {ad.creativeType}
                    </p>
                  </div>
                )}
              </div>

              {/* Ad Copy */}
              {ad.adCopy && (
                <div className="mt-4 rounded-lg border border-border p-4">
                  <p className="mb-1 text-xs font-medium text-muted-foreground">
                    Primary Text
                  </p>
                  <p className="text-sm">{ad.adCopy}</p>
                </div>
              )}

              {(ad.headline || ad.callToAction) && (
                <div className="mt-2 flex gap-4">
                  {ad.headline && (
                    <div className="flex-1 rounded-lg border border-border p-3">
                      <p className="mb-1 text-xs font-medium text-muted-foreground">
                        Headline
                      </p>
                      <p className="text-sm font-medium">{ad.headline}</p>
                    </div>
                  )}
                  {ad.callToAction && (
                    <div className="rounded-lg border border-border p-3">
                      <p className="mb-1 text-xs font-medium text-muted-foreground">
                        CTA
                      </p>
                      <p className="text-sm font-medium">{ad.callToAction}</p>
                    </div>
                  )}
                </div>
              )}
            </CardContent>
          </Card>

          {/* Performance Metrics */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-lg">
                <BarChart3 className="h-5 w-5" /> Performance Metrics
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
                {[
                  { label: "Spend", value: `$${ad.spend.toFixed(2)}` },
                  { label: "ROAS", value: `${ad.roas.toFixed(2)}x` },
                  { label: "CTR", value: `${(ad.ctr * 100).toFixed(2)}%` },
                  { label: "CPC", value: `$${ad.cpc.toFixed(2)}` },
                  { label: "Hook Rate", value: ad.creativeType === "VIDEO" ? `${(ad.hookRate * 100).toFixed(1)}%` : "N/A" },
                  { label: "Hold Rate", value: ad.creativeType === "VIDEO" ? `${(ad.holdRate * 100).toFixed(1)}%` : "N/A" },
                  { label: "Purchases", value: ad.purchases.toString() },
                  { label: "Impressions", value: ad.impressions.toLocaleString() },
                ].map((m) => (
                  <div key={m.label} className="rounded-lg border border-border p-3">
                    <p className="text-xs text-muted-foreground">{m.label}</p>
                    <p className="mt-1 text-lg font-bold">{m.value}</p>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Right: AI Analysis */}
        <div className="space-y-6">
          {analysis ? (
            <>
              {/* Classification Badges */}
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">AI Classification</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="flex flex-wrap gap-2">
                    {[
                      { label: "Asset Type", value: analysis.assetType },
                      { label: "Messaging", value: analysis.messagingAngle },
                      { label: "Hook", value: analysis.hookTactic },
                      { label: "Visual", value: analysis.visualStyle },
                      { label: "CTA Style", value: analysis.ctaStyle },
                      { label: "Tone", value: analysis.emotionalTone },
                      { label: "Product", value: analysis.productPresentation },
                    ].map((badge) => (
                      <div key={badge.label}>
                        <span className="mr-1 text-xs text-muted-foreground">
                          {badge.label}:
                        </span>
                        <Badge variant="secondary">
                          {badge.value.replace(/_/g, " ")}
                        </Badge>
                      </div>
                    ))}
                  </div>
                  <div className="mt-4 flex items-center gap-2">
                    <span className="text-xs text-muted-foreground">
                      Confidence:
                    </span>
                    <div className="flex-1 rounded-full bg-muted">
                      <div
                        className="h-2 rounded-full bg-primary"
                        style={{ width: `${analysis.confidenceScore}%` }}
                      />
                    </div>
                    <span className="text-xs font-medium">
                      {analysis.confidenceScore}%
                    </span>
                  </div>
                </CardContent>
              </Card>

              {/* AI Summary */}
              {analysis.aiSummary && (
                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg">AI Summary</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm leading-relaxed text-muted-foreground">
                      {analysis.aiSummary}
                    </p>
                  </CardContent>
                </Card>
              )}

              {/* Strengths & Weaknesses */}
              <div className="grid gap-4 md:grid-cols-2">
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2 text-lg text-green-400">
                      <CheckCircle2 className="h-5 w-5" /> Strengths
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <ul className="space-y-2">
                      {analysis.aiStrengths.map((s, i) => (
                        <li
                          key={i}
                          className="flex items-start gap-2 text-sm text-muted-foreground"
                        >
                          <span className="mt-1 h-1.5 w-1.5 flex-shrink-0 rounded-full bg-green-400" />
                          {s}
                        </li>
                      ))}
                    </ul>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2 text-lg text-red-400">
                      <XCircle className="h-5 w-5" /> Weaknesses
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <ul className="space-y-2">
                      {analysis.aiWeaknesses.map((w, i) => (
                        <li
                          key={i}
                          className="flex items-start gap-2 text-sm text-muted-foreground"
                        >
                          <span className="mt-1 h-1.5 w-1.5 flex-shrink-0 rounded-full bg-red-400" />
                          {w}
                        </li>
                      ))}
                    </ul>
                  </CardContent>
                </Card>
              </div>

              {/* Iteration Recommendations */}
              {analysis.aiIterationIdeas.length > 0 && (
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2 text-lg">
                      <Lightbulb className="h-5 w-5 text-amber-400" />
                      Iteration Recommendations
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {analysis.aiIterationIdeas.map((idea, i) => (
                        <div
                          key={i}
                          className="rounded-lg border border-border p-4"
                        >
                          <div className="mb-2 flex items-center justify-between">
                            <h4 className="font-medium">{idea.idea}</h4>
                            <Badge
                              variant={
                                idea.priority === "HIGH"
                                  ? "destructive"
                                  : idea.priority === "MEDIUM"
                                    ? "warning"
                                    : "secondary"
                              }
                            >
                              {idea.priority}
                            </Badge>
                          </div>
                          <p className="mb-2 text-sm text-muted-foreground">
                            {idea.reasoning}
                          </p>
                          <p className="text-xs text-primary">
                            Expected impact: {idea.estimatedImpact}
                          </p>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              )}
            </>
          ) : (
            <Card>
              <CardContent className="flex h-48 items-center justify-center">
                <div className="text-center">
                  <p className="text-muted-foreground">
                    AI analysis not yet available for this creative.
                  </p>
                  <Button variant="outline" size="sm" className="mt-4">
                    Run Analysis
                  </Button>
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}
