"use client";

import { useState, useMemo } from "react";
import Link from "next/link";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { formatCurrency, formatPercent, getVerdictEmoji } from "@/lib/utils";
import { ChevronUp, ChevronDown, Search, ChevronLeft, ChevronRight } from "lucide-react";
import type { AdWithAnalysis } from "@/types";

interface CreativeTableProps {
  ads: AdWithAnalysis[];
}

type SortKey = "name" | "spend" | "roas" | "ctr" | "hookRate" | "holdRate" | "verdict";
type SortDir = "asc" | "desc";

const PAGE_SIZE = 20;

export function CreativeTable({ ads }: CreativeTableProps) {
  const [search, setSearch] = useState("");
  const [sortKey, setSortKey] = useState<SortKey>("spend");
  const [sortDir, setSortDir] = useState<SortDir>("desc");
  const [page, setPage] = useState(0);
  const [assetTypeFilter, setAssetTypeFilter] = useState("ALL");
  const [angleFilter, setAngleFilter] = useState("ALL");
  const [verdictFilter, setVerdictFilter] = useState("ALL");

  const filtered = useMemo(() => {
    let result = ads;
    if (search) {
      const s = search.toLowerCase();
      result = result.filter((ad) => ad.name.toLowerCase().includes(s));
    }
    if (assetTypeFilter !== "ALL") {
      result = result.filter((ad) => ad.analysis?.assetType === assetTypeFilter);
    }
    if (angleFilter !== "ALL") {
      result = result.filter((ad) => ad.analysis?.messagingAngle === angleFilter);
    }
    if (verdictFilter !== "ALL") {
      result = result.filter((ad) => ad.verdict === verdictFilter);
    }
    return result;
  }, [ads, search, assetTypeFilter, angleFilter, verdictFilter]);

  const sorted = useMemo(() => {
    return [...filtered].sort((a, b) => {
      let aVal: any, bVal: any;
      switch (sortKey) {
        case "name":
          aVal = a.name;
          bVal = b.name;
          break;
        case "spend":
          aVal = a.spend;
          bVal = b.spend;
          break;
        case "roas":
          aVal = a.roas;
          bVal = b.roas;
          break;
        case "ctr":
          aVal = a.ctr;
          bVal = b.ctr;
          break;
        case "hookRate":
          aVal = a.hookRate;
          bVal = b.hookRate;
          break;
        case "holdRate":
          aVal = a.holdRate;
          bVal = b.holdRate;
          break;
        case "verdict":
          const order = { SCALE: 3, TEST: 2, KILL: 1 };
          aVal = order[a.verdict] || 0;
          bVal = order[b.verdict] || 0;
          break;
        default:
          return 0;
      }
      if (aVal < bVal) return sortDir === "asc" ? -1 : 1;
      if (aVal > bVal) return sortDir === "asc" ? 1 : -1;
      return 0;
    });
  }, [filtered, sortKey, sortDir]);

  const paged = sorted.slice(page * PAGE_SIZE, (page + 1) * PAGE_SIZE);
  const totalPages = Math.ceil(sorted.length / PAGE_SIZE);

  function handleSort(key: SortKey) {
    if (sortKey === key) {
      setSortDir(sortDir === "asc" ? "desc" : "asc");
    } else {
      setSortKey(key);
      setSortDir("desc");
    }
    setPage(0);
  }

  const assetTypes = [...new Set(ads.map((a) => a.analysis?.assetType).filter(Boolean))] as string[];
  const angles = [...new Set(ads.map((a) => a.analysis?.messagingAngle).filter(Boolean))] as string[];

  function SortIcon({ column }: { column: SortKey }) {
    if (sortKey !== column) return null;
    return sortDir === "asc" ? (
      <ChevronUp className="ml-1 inline h-3 w-3" />
    ) : (
      <ChevronDown className="ml-1 inline h-3 w-3" />
    );
  }

  return (
    <div>
      {/* Filters */}
      <div className="mb-4 flex flex-wrap items-center gap-3">
        <div className="relative flex-1 min-w-[200px]">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <Input
            placeholder="Search ads..."
            value={search}
            onChange={(e) => {
              setSearch(e.target.value);
              setPage(0);
            }}
            className="pl-9"
          />
        </div>
        <Select value={assetTypeFilter} onValueChange={(v) => { setAssetTypeFilter(v); setPage(0); }}>
          <SelectTrigger className="w-[180px]">
            <SelectValue placeholder="Asset Type" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="ALL">All Asset Types</SelectItem>
            {assetTypes.map((t) => (
              <SelectItem key={t} value={t}>
                {t.replace(/_/g, " ")}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
        <Select value={angleFilter} onValueChange={(v) => { setAngleFilter(v); setPage(0); }}>
          <SelectTrigger className="w-[180px]">
            <SelectValue placeholder="Messaging Angle" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="ALL">All Angles</SelectItem>
            {angles.map((a) => (
              <SelectItem key={a} value={a}>
                {a.replace(/_/g, " ")}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
        <Select value={verdictFilter} onValueChange={(v) => { setVerdictFilter(v); setPage(0); }}>
          <SelectTrigger className="w-[130px]">
            <SelectValue placeholder="Verdict" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="ALL">All Verdicts</SelectItem>
            <SelectItem value="SCALE">Scale</SelectItem>
            <SelectItem value="TEST">Test</SelectItem>
            <SelectItem value="KILL">Kill</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {/* Table */}
      <div className="overflow-x-auto rounded-lg border border-border">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-border bg-muted/50">
              <th className="px-4 py-3 text-left font-medium text-muted-foreground">
                Creative
              </th>
              <th
                className="cursor-pointer px-4 py-3 text-left font-medium text-muted-foreground hover:text-foreground"
                onClick={() => handleSort("name")}
              >
                Ad Name
                <SortIcon column="name" />
              </th>
              <th className="px-4 py-3 text-left font-medium text-muted-foreground">
                Type
              </th>
              <th className="px-4 py-3 text-left font-medium text-muted-foreground">
                Angle
              </th>
              <th className="px-4 py-3 text-left font-medium text-muted-foreground">
                Stage
              </th>
              <th
                className="cursor-pointer px-4 py-3 text-right font-medium text-muted-foreground hover:text-foreground"
                onClick={() => handleSort("spend")}
              >
                Spend
                <SortIcon column="spend" />
              </th>
              <th
                className="cursor-pointer px-4 py-3 text-right font-medium text-muted-foreground hover:text-foreground"
                onClick={() => handleSort("roas")}
              >
                ROAS
                <SortIcon column="roas" />
              </th>
              <th
                className="cursor-pointer px-4 py-3 text-right font-medium text-muted-foreground hover:text-foreground"
                onClick={() => handleSort("ctr")}
              >
                CTR
                <SortIcon column="ctr" />
              </th>
              <th
                className="cursor-pointer px-4 py-3 text-right font-medium text-muted-foreground hover:text-foreground"
                onClick={() => handleSort("hookRate")}
              >
                Hook Rate
                <SortIcon column="hookRate" />
              </th>
              <th
                className="cursor-pointer px-4 py-3 text-center font-medium text-muted-foreground hover:text-foreground"
                onClick={() => handleSort("verdict")}
              >
                Verdict
                <SortIcon column="verdict" />
              </th>
            </tr>
          </thead>
          <tbody>
            {paged.map((ad) => (
              <tr
                key={ad.id}
                className="border-b border-border transition-colors hover:bg-muted/30"
              >
                <td className="px-4 py-3">
                  <Link href={`/creative/${ad.id}`}>
                    <div className="h-10 w-10 rounded bg-muted flex items-center justify-center overflow-hidden">
                      {ad.thumbnailUrl || ad.imageUrl ? (
                        <img
                          src={ad.thumbnailUrl || ad.imageUrl || ""}
                          alt=""
                          className="h-full w-full object-cover"
                        />
                      ) : (
                        <span className="text-xs text-muted-foreground">
                          {ad.creativeType === "VIDEO" ? "VID" : "IMG"}
                        </span>
                      )}
                    </div>
                  </Link>
                </td>
                <td className="px-4 py-3">
                  <Link
                    href={`/creative/${ad.id}`}
                    className="font-medium text-foreground hover:text-primary"
                  >
                    {ad.name.length > 40 ? ad.name.slice(0, 40) + "..." : ad.name}
                  </Link>
                </td>
                <td className="px-4 py-3">
                  <Badge variant="secondary" className="text-xs">
                    {(ad.analysis?.assetType || "N/A").replace(/_/g, " ")}
                  </Badge>
                </td>
                <td className="px-4 py-3">
                  <Badge variant="outline" className="text-xs">
                    {(ad.analysis?.messagingAngle || "N/A").replace(/_/g, " ")}
                  </Badge>
                </td>
                <td className="px-4 py-3">
                  <Badge
                    variant={
                      ad.funnelStage === "TOF"
                        ? "default"
                        : ad.funnelStage === "MOF"
                          ? "secondary"
                          : "outline"
                    }
                    className="text-xs"
                  >
                    {ad.funnelStage}
                  </Badge>
                </td>
                <td className="px-4 py-3 text-right font-mono">
                  {formatCurrency(ad.spend)}
                </td>
                <td className="px-4 py-3 text-right font-mono">
                  {ad.roas.toFixed(2)}x
                </td>
                <td className="px-4 py-3 text-right font-mono">
                  {formatPercent(ad.ctr)}
                </td>
                <td className="px-4 py-3 text-right font-mono">
                  {ad.creativeType === "VIDEO"
                    ? formatPercent(ad.hookRate)
                    : "—"}
                </td>
                <td className="px-4 py-3 text-center">
                  <span className="text-base">
                    {getVerdictEmoji(ad.verdict)}
                  </span>{" "}
                  <span
                    className={`text-xs font-semibold ${
                      ad.verdict === "SCALE"
                        ? "text-green-400"
                        : ad.verdict === "KILL"
                          ? "text-red-400"
                          : "text-amber-400"
                    }`}
                  >
                    {ad.verdict}
                  </span>
                </td>
              </tr>
            ))}
            {paged.length === 0 && (
              <tr>
                <td colSpan={10} className="px-4 py-12 text-center text-muted-foreground">
                  No ads found matching your filters.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="mt-4 flex items-center justify-between">
          <p className="text-sm text-muted-foreground">
            Showing {page * PAGE_SIZE + 1}-{Math.min((page + 1) * PAGE_SIZE, sorted.length)} of {sorted.length} ads
          </p>
          <div className="flex items-center gap-2">
            <Button
              variant="outline"
              size="sm"
              disabled={page === 0}
              onClick={() => setPage(page - 1)}
            >
              <ChevronLeft className="h-4 w-4" />
            </Button>
            <span className="text-sm text-muted-foreground">
              Page {page + 1} of {totalPages}
            </span>
            <Button
              variant="outline"
              size="sm"
              disabled={page >= totalPages - 1}
              onClick={() => setPage(page + 1)}
            >
              <ChevronRight className="h-4 w-4" />
            </Button>
          </div>
        </div>
      )}
    </div>
  );
}
