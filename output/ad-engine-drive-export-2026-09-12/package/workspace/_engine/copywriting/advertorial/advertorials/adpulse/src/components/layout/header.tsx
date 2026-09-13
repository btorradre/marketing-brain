"use client";

import React from "react";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Button } from "@/components/ui/button";
import { RefreshCw, LogOut } from "lucide-react";
import { signOut } from "next-auth/react";
import { cn } from "@/lib/utils";

interface HeaderProps {
  accountId?: string;
  accounts?: Array<{ id: string; metaAccountName: string }>;
  onAccountChange?: (id: string) => void;
  dateRange: string;
  onDateRangeChange: (range: string) => void;
  funnelStage: string;
  onFunnelStageChange: (stage: string) => void;
  onRefresh?: () => void;
  isRefreshing?: boolean;
}

export function Header({
  accountId,
  accounts = [],
  onAccountChange,
  dateRange,
  onDateRangeChange,
  funnelStage,
  onFunnelStageChange,
  onRefresh,
  isRefreshing = false,
}: HeaderProps) {
  return (
    <header className="sticky top-0 z-30 flex h-16 items-center justify-between border-b border-border bg-background/95 px-6 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="flex items-center gap-4">
        {/* Ad Account Selector */}
        {accounts.length > 0 && (
          <Select value={accountId} onValueChange={onAccountChange}>
            <SelectTrigger className="w-[220px]">
              <SelectValue placeholder="Select account" />
            </SelectTrigger>
            <SelectContent>
              {accounts.map((account) => (
                <SelectItem key={account.id} value={account.id}>
                  {account.metaAccountName}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        )}

        {/* Date Range Selector */}
        <Select value={dateRange} onValueChange={onDateRangeChange}>
          <SelectTrigger className="w-[140px]">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="7D">Last 7 Days</SelectItem>
            <SelectItem value="14D">Last 14 Days</SelectItem>
            <SelectItem value="30D">Last 30 Days</SelectItem>
            <SelectItem value="90D">Last 90 Days</SelectItem>
            <SelectItem value="ALL">All Time</SelectItem>
          </SelectContent>
        </Select>

        {/* Funnel Stage Filter */}
        <Select value={funnelStage} onValueChange={onFunnelStageChange}>
          <SelectTrigger className="w-[120px]">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="ALL">All Funnel</SelectItem>
            <SelectItem value="TOF">TOF</SelectItem>
            <SelectItem value="MOF">MOF</SelectItem>
            <SelectItem value="BOF">BOF</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <div className="flex items-center gap-2">
        {onRefresh && (
          <Button
            variant="outline"
            size="sm"
            onClick={onRefresh}
            disabled={isRefreshing}
          >
            <RefreshCw
              className={cn("mr-2 h-4 w-4", isRefreshing && "animate-spin")}
            />
            {isRefreshing ? "Syncing..." : "Refresh"}
          </Button>
        )}
        <Button
          variant="ghost"
          size="sm"
          onClick={() => signOut({ callbackUrl: "/login" })}
        >
          <LogOut className="mr-2 h-4 w-4" />
          Sign Out
        </Button>
      </div>
    </header>
  );
}

