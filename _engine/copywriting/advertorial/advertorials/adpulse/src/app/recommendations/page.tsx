"use client";

import { useEffect, useState } from "react";
import { useSession } from "next-auth/react";
import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  AlertTriangle,
  TrendingUp,
  RefreshCw,
  DollarSign,
  Lightbulb,
} from "lucide-react";
import { formatCurrency } from "@/lib/utils";
import type { RecommendationGroup, AdWithAnalysis } from "@/types";

function AdRow({ ad, showReason }: { ad: AdWithAnalysis; showReason?: boolean }) {
  return (
    <Link href={`/creative/${ad.id}`}>
      <div className="flex items-center gap-4 rounded-lg border border-border p-3 transition-colors hover:bg-muted/30">
        <div className="h-12 w-12 flex-shrink-0 overflow-hidden rounded bg-muted">
          {ad.thumbnailUrl || ad.imageUrl ? (
            <img
              src={ad.thumbnailUrl || ad.imageUrl || ""}
              alt=""
              className="h-full w-full object-cover"
            />
          ) : (
            <div className="flex h-full w-full items-center justify-center text-xs text-muted-foreground">
              {ad.creativeType === "VIDEO" ? "VID" : "IMG"}
            </div>
          )}
        </div>
        <div className="flex-1 min-w-0">
          <p className="truncate text-sm font-medium">{ad.name}</p>
          {showReason && ad.analysis?.aiSummary && (
            <p className="mt-0.5 truncate text-xs text-muted-foreground">
              {ad.analysis.aiSummary}
            </p>
          )}
        </div>
        <div className="flex items-center gap-4 text-right">
          <div>
            <p className="text-xs text-muted-foreground">Spend</p>
            <p className="text-sm font-mono font-medium">
              {formatCurrency(ad.spend)}
            </p>
          </div>
          <div>
            <p className="text-xs text-muted-foreground">ROAS</p>
            <p
              className={`text-sm font-mono font-medium ${
                ad.roas >= 2 ? "text-green-400" : ad.roas < 1 ? "text-red-400" : "text-amber-400"
              }`}
            >
              {ad.roas.toFixed(2)}x
            </p>
          </div>
        </div>
      </div>
    </Link>
  );
}

function FunnelSection({ group }: { group: RecommendationGroup }) {
  return (
    <div className="space-y-6">
      {/* Kill List */}
      <Card className="border-red-500/20">
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="flex items-center gap-2 text-red-400">
              <AlertTriangle className="h-5 w-5" />
              Kill List ({group.killList.length})
            </CardTitle>
            {group.totalWaste > 0 && (
              <Badge variant="danger" className="flex items-center gap-1">
                <DollarSign className="h-3 w-3" />
                {formatCurrency(group.totalWaste)} wasted
              </Badge>
            )}
          </div>
        </CardHeader>
        <CardContent>
          {group.killList.length > 0 ? (
            <div className="space-y-2">
              {group.killList.map((ad) => (
                <AdRow key={ad.id} ad={ad} showReason />
              ))}
            </div>
          ) : (
            <p className="text-sm text-muted-foreground">
              No ads to kill. Your {group.funnelStage} ads are performing well.
            </p>
          )}
        </CardContent>
      </Card>

      {/* Scale List */}
      <Card className="border-green-500/20">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-green-400">
            <TrendingUp className="h-5 w-5" />
            Scale List ({group.scaleList.length})
          </CardTitle>
        </CardHeader>
        <CardContent>
          {group.scaleList.length > 0 ? (
            <div className="space-y-2">
              {group.scaleList.map((ad) => (
                <AdRow key={ad.id} ad={ad} />
              ))}
            </div>
          ) : (
            <p className="text-sm text-muted-foreground">
              No clear scale candidates yet. More data needed.
            </p>
          )}
        </CardContent>
      </Card>

      {/* Iterate List */}
      <Card className="border-amber-500/20">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-amber-400">
            <RefreshCw className="h-5 w-5" />
            Iterate List ({group.iterateList.length})
          </CardTitle>
        </CardHeader>
        <CardContent>
          {group.iterateList.length > 0 ? (
            <div className="space-y-2">
              {group.iterateList.map((ad) => (
                <AdRow key={ad.id} ad={ad} showReason />
              ))}
            </div>
          ) : (
            <p className="text-sm text-muted-foreground">
              No iteration candidates identified.
            </p>
          )}
        </CardContent>
      </Card>

      {/* Strategic Recommendations */}
      {group.strategicRecommendations.length > 0 && (
        <Card className="border-primary/20">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-primary">
              <Lightbulb className="h-5 w-5" />
              Strategic Recommendations
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {group.strategicRecommendations.map((rec, i) => (
                <div
                  key={i}
                  className="rounded-lg border border-border bg-muted/30 p-3"
                >
                  <p className="text-sm text-muted-foreground">{rec}</p>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}

export default function RecommendationsPage() {
  const { data: session } = useSession();
  const [groups, setGroups] = useState<RecommendationGroup[]>([]);
  const [loading, setLoading] = useState(true);
  const [accountId, setAccountId] = useState("");

  useEffect(() => {
    async function loadAccount() {
      const res = await fetch("/api/accounts");
      const accounts = await res.json();
      if (accounts.length > 0) setAccountId(accounts[0].id);
    }
    if (session) loadAccount();
  }, [session]);

  useEffect(() => {
    async function loadRecs() {
      if (!accountId) return;
      setLoading(true);
      try {
        const res = await fetch(
          `/api/insights/recommendations?accountId=${accountId}`
        );
        const data = await res.json();
        setGroups(data);
      } catch {
        console.error("Failed to load recommendations");
      } finally {
        setLoading(false);
      }
    }
    loadRecs();
  }, [accountId]);

  if (loading) {
    return (
      <div className="flex h-[80vh] items-center justify-center">
        <div className="h-8 w-8 animate-spin rounded-full border-2 border-primary border-t-transparent" />
      </div>
    );
  }

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-2xl font-bold">Recommendations</h1>
        <p className="text-sm text-muted-foreground">
          AI-powered kill, scale, and iterate recommendations by funnel stage.
        </p>
      </div>

      <Tabs defaultValue="TOF">
        <TabsList className="mb-6">
          <TabsTrigger value="TOF">
            TOF ({groups.find((g) => g.funnelStage === "TOF")?.killList.length ?? 0} kill / {groups.find((g) => g.funnelStage === "TOF")?.scaleList.length ?? 0} scale)
          </TabsTrigger>
          <TabsTrigger value="MOF">
            MOF ({groups.find((g) => g.funnelStage === "MOF")?.killList.length ?? 0} kill / {groups.find((g) => g.funnelStage === "MOF")?.scaleList.length ?? 0} scale)
          </TabsTrigger>
          <TabsTrigger value="BOF">
            BOF ({groups.find((g) => g.funnelStage === "BOF")?.killList.length ?? 0} kill / {groups.find((g) => g.funnelStage === "BOF")?.scaleList.length ?? 0} scale)
          </TabsTrigger>
        </TabsList>
        {["TOF", "MOF", "BOF"].map((stage) => {
          const group = groups.find((g) => g.funnelStage === stage);
          return (
            <TabsContent key={stage} value={stage}>
              {group ? (
                <FunnelSection group={group} />
              ) : (
                <p className="text-muted-foreground">No data for {stage}.</p>
              )}
            </TabsContent>
          );
        })}
      </Tabs>
    </div>
  );
}
