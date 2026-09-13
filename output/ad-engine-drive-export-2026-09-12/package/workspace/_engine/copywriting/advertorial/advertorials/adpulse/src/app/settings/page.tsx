"use client";

import { useEffect, useState } from "react";
import { useSession } from "next-auth/react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ExternalLink, Unplug, Plus, Users, CreditCard, Key } from "lucide-react";
import toast from "react-hot-toast";

interface ConnectedAccount {
  id: string;
  metaAccountId: string;
  metaAccountName: string;
  status: string;
  lastSyncAt: string | null;
}

export default function SettingsPage() {
  const { data: session } = useSession();
  const [accounts, setAccounts] = useState<ConnectedAccount[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadAccounts() {
      try {
        const res = await fetch("/api/accounts");
        const data = await res.json();
        setAccounts(data);
      } catch {
        console.error("Failed to load accounts");
      } finally {
        setLoading(false);
      }
    }
    if (session) loadAccounts();
  }, [session]);

  function handleConnectMeta() {
    window.location.href = "/api/meta/oauth";
  }

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-2xl font-bold">Settings</h1>
        <p className="text-sm text-muted-foreground">
          Manage your account, connections, and preferences.
        </p>
      </div>

      <div className="max-w-3xl space-y-6">
        {/* Connected Ad Accounts */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle>Connected Ad Accounts</CardTitle>
                <CardDescription>
                  Manage your Meta ad account connections.
                </CardDescription>
              </div>
              <Button onClick={handleConnectMeta} size="sm">
                <Plus className="mr-2 h-4 w-4" />
                Connect Account
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            {loading ? (
              <div className="flex h-20 items-center justify-center">
                <div className="h-6 w-6 animate-spin rounded-full border-2 border-primary border-t-transparent" />
              </div>
            ) : accounts.length > 0 ? (
              <div className="space-y-3">
                {accounts.map((account) => (
                  <div
                    key={account.id}
                    className="flex items-center justify-between rounded-lg border border-border p-4"
                  >
                    <div>
                      <p className="font-medium">{account.metaAccountName}</p>
                      <p className="text-xs text-muted-foreground">
                        ID: {account.metaAccountId}
                        {account.lastSyncAt &&
                          ` · Last sync: ${new Date(account.lastSyncAt).toLocaleDateString()}`}
                      </p>
                    </div>
                    <div className="flex items-center gap-2">
                      <Badge
                        variant={
                          account.status === "CONNECTED"
                            ? "success"
                            : account.status === "ERROR"
                              ? "danger"
                              : "secondary"
                        }
                      >
                        {account.status}
                      </Badge>
                      <Button variant="ghost" size="sm">
                        <Unplug className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="rounded-lg border border-dashed border-border p-8 text-center">
                <p className="text-muted-foreground">
                  No ad accounts connected yet.
                </p>
                <Button onClick={handleConnectMeta} variant="outline" size="sm" className="mt-3">
                  Connect your first account
                </Button>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Funnel Stage Rules */}
        <Card>
          <CardHeader>
            <CardTitle>Funnel Stage Rules</CardTitle>
            <CardDescription>
              Customize how campaigns are classified as TOF, MOF, or BOF.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4 text-sm text-muted-foreground">
              <div className="rounded-lg border border-border p-3">
                <p className="mb-1 font-medium text-foreground">TOF (Top of Funnel)</p>
                <p>Objectives: AWARENESS, REACH, VIDEO_VIEWS, TRAFFIC</p>
                <p>Keywords: prospecting, cold, tof, top, acquisition, broad</p>
              </div>
              <div className="rounded-lg border border-border p-3">
                <p className="mb-1 font-medium text-foreground">MOF (Middle of Funnel)</p>
                <p>Objectives: ENGAGEMENT, LEAD_GENERATION</p>
                <p>Keywords: mof, middle, retarget, engaged, warm</p>
              </div>
              <div className="rounded-lg border border-border p-3">
                <p className="mb-1 font-medium text-foreground">BOF (Bottom of Funnel)</p>
                <p>Objectives: CONVERSIONS, CATALOG_SALES, STORE_TRAFFIC</p>
                <p>Keywords: bof, bottom, purchase, conversion, dpa, catalog, hot</p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Placeholder sections */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Users className="h-5 w-5" /> Team Members
            </CardTitle>
            <CardDescription>Coming soon — invite team members to collaborate.</CardDescription>
          </CardHeader>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Key className="h-5 w-5" /> API Keys
            </CardTitle>
            <CardDescription>Coming soon — API access for integrations.</CardDescription>
          </CardHeader>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <CreditCard className="h-5 w-5" /> Billing
            </CardTitle>
            <CardDescription>Coming soon — manage your subscription.</CardDescription>
          </CardHeader>
        </Card>
      </div>
    </div>
  );
}
