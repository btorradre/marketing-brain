import Link from "next/link";
import { Activity, BarChart3, Brain, Target, TrendingUp, Zap } from "lucide-react";
import { Button } from "@/components/ui/button";

const features = [
  {
    icon: Brain,
    title: "AI Creative Analysis",
    description:
      "Every ad is analyzed by AI — asset type, messaging angle, hook tactic, visual style, and more. Know exactly what makes each creative tick.",
  },
  {
    icon: BarChart3,
    title: "Win Rate Breakdowns",
    description:
      "See which creative categories are winning across every dimension. UGC vs Studio? Problem-Solution vs Social Proof? Get the data.",
  },
  {
    icon: Target,
    title: "Kill / Scale / Iterate",
    description:
      "Instant recommendations on which ads to kill, scale, or iterate. Stop wasting budget on underperformers.",
  },
  {
    icon: TrendingUp,
    title: "Trend Detection",
    description:
      "Track creative performance trends over time. Spot fatigue early and double down on what's working.",
  },
  {
    icon: Zap,
    title: "Iteration Briefs",
    description:
      "AI-generated creative briefs for each ad — what to change, why it should work, and which metric it'll impact.",
  },
  {
    icon: Activity,
    title: "Funnel Stage Intelligence",
    description:
      "Separate insights for TOF, MOF, and BOF. Different funnels need different creative strategies.",
  },
];

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-background">
      {/* Nav */}
      <nav className="border-b border-border">
        <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-6">
          <div className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary">
              <Activity className="h-5 w-5 text-primary-foreground" />
            </div>
            <span className="text-xl font-bold">AdPulse</span>
          </div>
          <div className="flex items-center gap-4">
            <Link href="/login">
              <Button variant="ghost">Log In</Button>
            </Link>
            <Link href="/signup">
              <Button>Get Started</Button>
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="mx-auto max-w-7xl px-6 py-24 text-center">
        <div className="mx-auto max-w-3xl">
          <div className="mb-6 inline-flex items-center rounded-full border border-primary/30 bg-primary/10 px-4 py-1.5 text-sm text-primary">
            Meta Ads Creative Intelligence
          </div>
          <h1 className="mb-6 text-5xl font-bold tracking-tight md:text-6xl lg:text-7xl">
            Stop Guessing.
            <br />
            <span className="text-primary">Start Knowing.</span>
          </h1>
          <p className="mx-auto mb-10 max-w-2xl text-lg text-muted-foreground">
            Meta tells you WHAT happened. AdPulse tells you WHY. AI-powered
            creative analysis that watches every video, labels every ad, and
            generates actionable recommendations to scale winners and kill
            losers.
          </p>
          <div className="flex items-center justify-center gap-4">
            <Link href="/signup">
              <Button size="lg" className="text-base">
                Start Free Analysis
              </Button>
            </Link>
            <Link href="/login">
              <Button variant="outline" size="lg" className="text-base">
                View Demo
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Stats */}
      <section className="border-y border-border bg-card/50">
        <div className="mx-auto grid max-w-7xl grid-cols-2 gap-8 px-6 py-16 md:grid-cols-4">
          {[
            { value: "10,000+", label: "Ads Analyzed" },
            { value: "23%", label: "Avg ROAS Improvement" },
            { value: "< 2min", label: "Per Creative Analysis" },
            { value: "15+", label: "Creative Dimensions" },
          ].map((stat) => (
            <div key={stat.label} className="text-center">
              <div className="text-3xl font-bold text-primary">
                {stat.value}
              </div>
              <div className="mt-1 text-sm text-muted-foreground">
                {stat.label}
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Features */}
      <section className="mx-auto max-w-7xl px-6 py-24">
        <div className="mb-16 text-center">
          <h2 className="mb-4 text-3xl font-bold">
            Creative Intelligence, Not Just Data
          </h2>
          <p className="mx-auto max-w-2xl text-muted-foreground">
            AdPulse goes beyond metrics. It understands your creatives at a
            strategic level and tells you exactly what to do next.
          </p>
        </div>
        <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
          {features.map((feature) => (
            <div
              key={feature.title}
              className="rounded-xl border border-border bg-card p-6 transition-colors hover:border-primary/30"
            >
              <div className="mb-4 flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10">
                <feature.icon className="h-5 w-5 text-primary" />
              </div>
              <h3 className="mb-2 text-lg font-semibold">{feature.title}</h3>
              <p className="text-sm text-muted-foreground">
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="border-t border-border bg-card/50">
        <div className="mx-auto max-w-7xl px-6 py-24 text-center">
          <h2 className="mb-4 text-3xl font-bold">
            Ready to decode your ad performance?
          </h2>
          <p className="mx-auto mb-8 max-w-xl text-muted-foreground">
            Connect your Meta ad account in minutes. Get your first AI analysis
            in under an hour.
          </p>
          <Link href="/signup">
            <Button size="lg" className="text-base">
              Get Started Free
            </Button>
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-8">
          <div className="flex items-center gap-2">
            <Activity className="h-5 w-5 text-primary" />
            <span className="font-semibold">AdPulse</span>
          </div>
          <p className="text-sm text-muted-foreground">
            Built for DTC brands and media buying agencies.
          </p>
        </div>
      </footer>
    </div>
  );
}
