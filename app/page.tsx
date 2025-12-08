"use client";

import React from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { ArrowRight, Sparkles, Layers, Wand2, Timer, BarChart3, Shield, Workflow, PlaySquare, PlugZap } from "lucide-react";

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-background text-foreground">
      {/* Hero */}
      <section className="relative overflow-hidden px-6 py-16 sm:px-10 lg:px-14">
        <div className="absolute inset-0 pointer-events-none opacity-70" aria-hidden>
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_20%_20%,rgba(0,0,0,0.08),transparent_40%),radial-gradient(circle_at_80%_10%,rgba(0,0,0,0.05),transparent_40%),radial-gradient(circle_at_40%_80%,rgba(0,0,0,0.06),transparent_45%)]" />
        </div>
        <div className="mx-auto max-w-6xl grid gap-10 lg:grid-cols-[1.1fr_0.9fr] items-start relative z-10">
          <div className="space-y-6">
            <div className="inline-flex items-center gap-2 rounded-full border border-border/80 bg-card/70 px-3 py-2 text-xs uppercase tracking-[0.14em] text-muted-foreground">
              <Sparkles className="h-4 w-4" /> Human-made monochrome
            </div>
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold leading-tight tracking-tight">
              Turn long YouTube videos into disciplined, ready-to-post Reels.
            </h1>
            <p className="text-lg text-muted-foreground max-w-2xl leading-relaxed">
              GRAVIXAI slices, scores, and formats your footage automatically. No color noise, no fluff—just a focused pipeline that keeps everything inside one calm surface.
            </p>
            <div className="flex flex-col sm:flex-row gap-3">
              <Link href="/add-video">
                <Button size="lg" className="h-12 px-6 flex items-center gap-2">
                  Add a video
                  <ArrowRight className="h-4 w-4" />
                </Button>
              </Link>
              <Link href="/connect-instagram">
                <Button size="lg" variant="outline" className="h-12 px-6 flex items-center gap-2">
                  Connect Instagram
                  <PlugZap className="h-4 w-4" />
                </Button>
              </Link>
            </div>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-2 text-sm">
              {[
                { label: "Cuts scored", value: "+12k" },
                { label: "Avg. prep time", value: "2m 30s" },
                { label: "IG-ready ratio", value: "94%" },
                { label: "Export size", value: "1080x1920" },
              ].map((item) => (
                <div key={item.label} className="rounded-xl border border-border/70 bg-card/70 px-4 py-3">
                  <p className="text-xs text-muted-foreground uppercase tracking-wide">{item.label}</p>
                  <p className="text-xl font-semibold mt-1">{item.value}</p>
                </div>
              ))}
            </div>
          </div>

          <div className="relative">
            <div className="absolute -top-6 -right-6 h-32 w-32 rounded-full border border-border/40" aria-hidden></div>
            <div className="absolute -bottom-8 -left-10 h-28 w-28 rounded-full border border-border/30" aria-hidden></div>
            <div className="relative rounded-2xl border border-border/60 bg-card/80 shadow-organic p-6 space-y-4">
              <div className="rounded-xl border border-border/60 bg-background/60 p-4 flex items-center justify-between">
                <div className="space-y-1">
                  <p className="text-sm text-muted-foreground">Current job</p>
                  <p className="font-semibold">Tech Talk 54: AI vs Video</p>
                </div>
                <div className="rounded-full border border-border px-3 py-1 text-xs">Processing</div>
              </div>
              <div className="rounded-xl border border-border/60 bg-background/60 p-4 space-y-3">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-muted-foreground">Segmenting</span>
                  <span className="font-medium">65%</span>
                </div>
                <div className="h-2 rounded-full bg-border/70 overflow-hidden">
                  <div className="h-full w-2/3 bg-foreground" />
                </div>
                <div className="grid grid-cols-3 gap-2 text-xs text-muted-foreground">
                  <span className="rounded-lg border border-border/60 bg-card/60 px-2 py-2">Captions</span>
                  <span className="rounded-lg border border-border/60 bg-card/60 px-2 py-2">Vertical crop</span>
                  <span className="rounded-lg border border-border/60 bg-card/60 px-2 py-2">Scene score</span>
                </div>
              </div>
              <div className="rounded-xl border border-border/60 bg-background/60 p-4 space-y-2 text-sm">
                <div className="flex items-center justify-between">
                  <span className="text-muted-foreground">Next up</span>
                  <span className="font-medium">Publish to IG</span>
                </div>
                <p className="text-muted-foreground">Auto-post queue keeps reels synced once you approve.</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Proof points */}
      <section className="px-6 sm:px-10 lg:px-14 pb-14">
        <div className="mx-auto max-w-6xl grid gap-4 md:grid-cols-3">
          {[
            {
              icon: Layers,
              title: "Structured output",
              desc: "Every reel comes with clean captions, safe crop, and audio checked. No retries needed.",
            },
            {
              icon: Wand2,
              title: "Monochrome focus",
              desc: "A single aesthetic direction—no random gradients or off-brand color hits anywhere.",
            },
            {
              icon: Timer,
              title: "Under 3 minutes",
              desc: "From paste to ready-to-post in minutes, not hours of timeline work.",
            },
          ].map((item) => {
            const Icon = item.icon;
            return (
              <div key={item.title} className="rounded-2xl border border-border/70 bg-card/70 p-5 space-y-3 shadow-soft">
                <div className="flex items-center gap-2 text-sm text-muted-foreground">
                  <Icon className="h-4 w-4" />
                  <span>{item.title}</span>
                </div>
                <p className="text-base text-muted-foreground leading-relaxed">{item.desc}</p>
              </div>
            );
          })}
        </div>
      </section>

      {/* Workflow */}
      <section className="px-6 sm:px-10 lg:px-14 pb-16">
        <div className="mx-auto max-w-6xl rounded-2xl border border-border/70 bg-card/70 p-6 sm:p-8 shadow-organic">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <p className="text-xs uppercase tracking-[0.14em] text-muted-foreground">Workflow</p>
              <h2 className="text-3xl sm:text-4xl font-bold mt-2">A disciplined four-step lane.</h2>
            </div>
            <Link href="/connect-instagram">
              <Button variant="outline">See connection status</Button>
            </Link>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mt-8">
            {[
              { title: "Paste", desc: "Drop a YouTube link—no uploads needed.", icon: Workflow },
              { title: "Slice", desc: "Scene-score, caption, crop, normalize audio.", icon: PlaySquare },
              { title: "Review", desc: "Skim the best cuts, remove anything you dislike.", icon: Shield },
              { title: "Publish", desc: "Push to Instagram in-line. No app hopping.", icon: PlugZap },
            ].map((step, idx) => {
              const Icon = step.icon;
              return (
                <div key={step.title} className="rounded-xl border border-border/70 bg-background/80 p-4 space-y-3">
                  <div className="flex items-center justify-between text-sm text-muted-foreground">
                    <span className="rounded-full border border-border/70 px-2 py-1 text-xs">0{idx + 1}</span>
                    <Icon className="h-4 w-4" />
                  </div>
                  <h3 className="text-lg font-semibold">{step.title}</h3>
                  <p className="text-sm text-muted-foreground leading-relaxed">{step.desc}</p>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Metrics + social proof */}
      <section className="px-6 sm:px-10 lg:px-14 pb-16">
        <div className="mx-auto max-w-6xl grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
          <div className="rounded-2xl border border-border/70 bg-card/70 p-6 sm:p-8 shadow-soft space-y-4">
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <BarChart3 className="h-4 w-4" /> Operational metrics
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              {[{ label: "Render success", value: "99.2%" }, { label: "Token health", value: "Live" }, { label: "Avg retry", value: "<1x" }].map((m) => (
                <div key={m.label} className="rounded-xl border border-border/70 bg-background/70 px-4 py-3">
                  <p className="text-xs text-muted-foreground uppercase tracking-wide">{m.label}</p>
                  <p className="text-2xl font-semibold mt-2">{m.value}</p>
                </div>
              ))}
            </div>
            <p className="text-sm text-muted-foreground leading-relaxed">
              Built to stay within Meta Graph v19 constraints. Tokens, permissions, and page links are checked before you publish.
            </p>
          </div>
          <div className="rounded-2xl border border-border/70 bg-card/70 p-6 sm:p-7 shadow-soft space-y-4">
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <Shield className="h-4 w-4" /> Safe by default
            </div>
            <p className="text-lg font-semibold">Monochrome UI that keeps you in flow.</p>
            <p className="text-sm text-muted-foreground leading-relaxed">
              No extra tabs, no rainbow gradients. Everything you need—link input, processing, IG connection, status—lives inside one calm surface.
            </p>
            <div className="rounded-xl border border-border/70 bg-background/70 p-4 space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-muted-foreground">Instagram connect</span>
                <span className="font-medium">Live via Graph v19</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Publishing</span>
                <span className="font-medium">Direct to IG Reels</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Processing</span>
                <span className="font-medium">1080x1920, captioned</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="px-6 sm:px-10 lg:px-14 pb-20">
        <div className="mx-auto max-w-5xl rounded-2xl border border-border/70 bg-card/80 p-8 sm:p-10 text-center shadow-organic space-y-4">
          <h2 className="text-3xl sm:text-4xl font-bold">Keep everything monochrome. Ship reels faster.</h2>
          <p className="text-muted-foreground max-w-3xl mx-auto">
            Start with a link, end with a published reel. No sign-up loops, no multi-color chaos. Just GRAVIXAI doing the work.
          </p>
          <div className="flex flex-col sm:flex-row gap-3 justify-center">
            <Link href="/add-video">
              <Button size="lg">Add a video</Button>
            </Link>
            <Link href="/connect-instagram">
              <Button size="lg" variant="outline">Connect Instagram</Button>
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
