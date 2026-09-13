"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useSession } from "next-auth/react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Activity, CheckCircle2, ExternalLink, Loader2 } from "lucide-react";

export default function OnboardingPage() {
  const router = useRouter();
  const { data: session } = useSession();
  const [step, setStep] = useState(1);
  const [connecting, setConnecting] = useState(false);
  const [syncing, setSyncing] = useState(false);
  const [syncProgress, setSyncProgress] = useState(0);

  async function handleConnectMeta() {
    setConnecting(true);
    // Redirect to Meta OAuth
    window.location.href = "/api/meta/oauth";
  }

  async function handleStartSync() {
    setSyncing(true);
    // Simulate sync progress for demo
    for (let i = 0; i <= 100; i += 5) {
      await new Promise((r) => setTimeout(r, 200));
      setSyncProgress(i);
    }
    setSyncing(false);
    setStep(4);
  }

  function handleUseDemoData() {
    router.push("/dashboard");
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-background px-4">
      <div className="w-full max-w-lg">
        {/* Header */}
        <div className="mb-8 text-center">
          <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-primary">
            <Activity className="h-7 w-7 text-primary-foreground" />
          </div>
          <h1 className="text-2xl font-bold">Set up AdPulse</h1>
          <p className="mt-1 text-sm text-muted-foreground">
            Connect your Meta ad account to get started.
          </p>
        </div>

        {/* Progress Steps */}
        <div className="mb-8 flex items-center justify-center gap-2">
          {[1, 2, 3, 4].map((s) => (
            <div
              key={s}
              className={`h-2 w-12 rounded-full ${
                s <= step ? "bg-primary" : "bg-muted"
              }`}
            />
          ))}
        </div>

        {/* Step 1: Connect Meta */}
        {step === 1 && (
          <Card>
            <CardHeader>
              <CardTitle>Connect Meta Ads</CardTitle>
              <CardDescription>
                Link your Meta Business account to start analyzing your ad
                creatives.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <Button
                onClick={handleConnectMeta}
                className="w-full"
                disabled={connecting}
              >
                {connecting ? (
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                ) : (
                  <ExternalLink className="mr-2 h-4 w-4" />
                )}
                Connect with Meta
              </Button>
              <div className="relative">
                <div className="absolute inset-0 flex items-center">
                  <div className="w-full border-t border-border" />
                </div>
                <div className="relative flex justify-center text-xs uppercase">
                  <span className="bg-card px-2 text-muted-foreground">Or</span>
                </div>
              </div>
              <Button
                variant="outline"
                className="w-full"
                onClick={handleUseDemoData}
              >
                Use Demo Data Instead
              </Button>
            </CardContent>
          </Card>
        )}

        {/* Step 2: Select Account */}
        {step === 2 && (
          <Card>
            <CardHeader>
              <CardTitle>Select Ad Account</CardTitle>
              <CardDescription>
                Choose which ad account(s) to analyze.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="rounded-lg border border-primary/50 bg-primary/5 p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium">Demo Skincare Brand</p>
                    <p className="text-xs text-muted-foreground">
                      act_123456789
                    </p>
                  </div>
                  <CheckCircle2 className="h-5 w-5 text-primary" />
                </div>
              </div>
              <Button className="w-full" onClick={() => setStep(3)}>
                Continue
              </Button>
            </CardContent>
          </Card>
        )}

        {/* Step 3: Sync */}
        {step === 3 && (
          <Card>
            <CardHeader>
              <CardTitle>Sync Your Data</CardTitle>
              <CardDescription>
                We&apos;ll pull your campaign data and start AI analysis.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {syncing ? (
                <div>
                  <div className="mb-2 flex items-center justify-between text-sm">
                    <span className="text-muted-foreground">
                      Syncing campaigns & analyzing creatives...
                    </span>
                    <span className="font-mono">{syncProgress}%</span>
                  </div>
                  <Progress value={syncProgress} className="h-2" />
                </div>
              ) : (
                <Button className="w-full" onClick={handleStartSync}>
                  Start Sync (Last 30 Days)
                </Button>
              )}
            </CardContent>
          </Card>
        )}

        {/* Step 4: Done */}
        {step === 4 && (
          <Card>
            <CardHeader className="text-center">
              <div className="mx-auto mb-2 flex h-12 w-12 items-center justify-center rounded-full bg-green-500/10">
                <CheckCircle2 className="h-7 w-7 text-green-400" />
              </div>
              <CardTitle>You&apos;re all set!</CardTitle>
              <CardDescription>
                Your data has been synced and analyzed. Head to the dashboard to
                see your creative insights.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Button
                className="w-full"
                onClick={() => router.push("/dashboard")}
              >
                Go to Dashboard
              </Button>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}
