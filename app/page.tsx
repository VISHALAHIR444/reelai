"use client";

import Link from "next/link";
import Hero from "@/components/hero/Hero";
import { Panel } from "@/components/dashboard/Panel";
import { motion } from "framer-motion";

const metrics = [
  { label: "Reels Generated", value: "1,247" },
  { label: "Avg Processing", value: "2m 18s" },
  { label: "Queue Active", value: "3" },
  { label: "Accounts", value: "2" },
];

export default function LandingPage() {
  return (
    <div className="relative min-h-screen">
      <Hero />

      <div className="max-w-7xl mx-auto px-6 py-24 space-y-16">
        <motion.div 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
          className="grid grid-cols-2 md:grid-cols-4 gap-6"
        >
          {metrics.map((metric, i) => (
            <div key={i} className="studio-panel p-6 text-center">
              <p className="studio-text-label mb-2">{metric.label}</p>
              <p className="text-3xl font-semibold text-studio-paper">{metric.value}</p>
            </div>
          ))}
        </motion.div>

        <div className="grid md:grid-cols-2 gap-6">
          <Panel title="Pipeline Status" subtitle="Live processing">
            <div className="space-y-4">
              <div className="flex items-center justify-between py-3 border-b border-white/5">
                <span className="text-studio-cloud">Segmenting video</span>
                <span className="studio-text-value">68%</span>
              </div>
              <div className="h-1 bg-studio-slate rounded-full overflow-hidden">
                <div className="h-full w-[68%] bg-gradient-to-r from-studio-accent to-studio-gold transition-all duration-500" />
              </div>
            </div>
          </Panel>

          <Panel title="Upload Queue" subtitle="Ready to publish">
            <div className="space-y-3">
              {["Founder story / Episode 12", "Product demo / Launch teaser", "Behind the scenes"].map((item, i) => (
                <div key={i} className="flex items-center justify-between p-3 bg-studio-slate/30 rounded-xl border border-white/5">
                  <span className="text-studio-cloud text-sm">{item}</span>
                  <span className="text-xs text-studio-accent">Ready</span>
                </div>
              ))}
            </div>
          </Panel>
        </div>

        <Panel title="Studio Actions" className="text-center">
          <div className="flex items-center justify-center gap-4">
            <Link href="/add-video">
              <button className="studio-button-primary">
                Add Video
              </button>
            </Link>
            <Link href="/dashboard">
              <button className="studio-button-secondary">
                View Dashboard
              </button>
            </Link>
            <Link href="/videos">
              <button className="studio-button-secondary">
                Reels Library
              </button>
            </Link>
          </div>
        </Panel>
      </div>
    </div>
  );
}

        <section className="grid gap-5 lg:grid-cols-3">
          <Panel title="Add YouTube link" subtitle="Primary lane">
            <div className="rounded-xl border border-white/10 bg-black/30 p-4 space-y-3">
              <div className="flex items-center gap-3 rounded-lg border border-white/10 bg-[#0B0F14] px-4 py-3">
                <span className="text-white/50">https://</span>
                <input className="w-full bg-transparent text-white placeholder:text-white/40 focus:outline-none" placeholder="youtube.com/watch?v=..." />
                <Button className="rounded-lg bg-white/10 text-white hover:bg-white/15" size="sm">Queue</Button>
              </div>
              <p className="text-xs text-white/50">Auto-crop, caption, score, and prep vertical output. Future: multi-platform split.</p>
            </div>
          </Panel>

          <Panel title="Processing status" subtitle="Live pipeline">
            <div className="space-y-3 text-sm text-white/80">
              <div className="flex items-center justify-between">
                <span className="text-white/60">Segmenting</span>
                <span className="font-semibold">68%</span>
              </div>
              <div className="h-2 rounded-full bg-white/10 overflow-hidden">
                <div className="h-full w-[68%] rounded-full bg-gradient-to-r from-[#A4B4FF] to-[#F6C177]" />
              </div>
              <div className="flex flex-wrap gap-2 text-[11px] text-white/70">
                {['AI captions', 'Vertical crop', 'Scene score', 'Audio normalize'].map((pill) => (
                  <span key={pill} className="rounded-lg border border-white/10 bg-white/5 px-2 py-1">{pill}</span>
                ))}
              </div>
            </div>
          </Panel>

          <Panel title="Generated reels" subtitle="Cinematic preview" action={<Link href="/videos" className="text-xs text-[#A4B4FF]">Open gallery</Link>}>
            <div className="grid grid-cols-3 gap-2">
              {reels.map((reel) => (
                <div key={reel.title} className="relative aspect-[9/16] overflow-hidden rounded-lg border border-white/10" style={{ backgroundImage: reel.gradient }}>
                  <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-black/0 to-transparent" />
                  <div className="absolute bottom-2 left-2 right-2 text-[11px] text-white/80">
                    <p className="line-clamp-2 leading-tight">{reel.title}</p>
                    <div className="flex items-center justify-between text-white/60">
                      <span>{reel.duration}</span>
                      <span className="rounded-full border border-white/15 bg-white/10 px-2 py-0.5">{reel.status}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </Panel>
        </section>

        <section className="grid gap-5 lg:grid-cols-[2fr_1.4fr]">
          <Panel title="Queue & scheduling" subtitle="Calm timeline">
            <QueueTimeline items={queueItems} />
          </Panel>

          <Panel title="Future-ready" subtitle="Automation lanes">
            <div className="space-y-3 text-sm text-white/70">
              <div className="flex items-center justify-between rounded-lg border border-white/10 bg-white/5 px-4 py-3">
                <span>AI captions</span>
                <span className="rounded-full border border-white/15 bg-white/10 px-3 py-1 text-[11px] text-white/70">Planned</span>
              </div>
              <div className="flex items-center justify-between rounded-lg border border-white/10 bg-white/5 px-4 py-3">
                <span>Multi-platform reels</span>
                <span className="rounded-full border border-white/15 bg-white/10 px-3 py-1 text-[11px] text-white/70">Soon</span>
              </div>
              <div className="flex items-center justify-between rounded-lg border border-white/10 bg-white/5 px-4 py-3">
                <span>Auto-upload automation</span>
                <span className="rounded-full border border-white/15 bg-white/10 px-3 py-1 text-[11px] text-white/70">Enabled</span>
              </div>
              <div className="flex items-center justify-between rounded-lg border border-white/10 bg-white/5 px-4 py-3">
                <span>Analytics dashboard</span>
                <span className="rounded-full border border-white/15 bg-white/10 px-3 py-1 text-[11px] text-white/70">Soon</span>
              </div>
            </div>
          </Panel>
        </section>

        <section className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold text-white">Generated reels</h2>
            <span className="text-xs text-white/50">Cinematic grid</span>
          </div>
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {reels.map((reel) => (
              <ReelCard key={reel.title} {...reel} />
            ))}
          </div>
        </section>

        <section className="grid gap-5 lg:grid-cols-3">
          <Panel title="Accounts" subtitle="Instagram + future platforms" action={<Link href="/settings/social-accounts" className="text-xs text-[#A4B4FF]">Manage</Link>}>
            <div className="space-y-2 text-sm text-white/70">
              <div className="flex items-center justify-between rounded-lg border border-white/10 bg-white/5 px-4 py-3">
                <span>Instagram Business</span>
                <span className="text-[#A4B4FF] text-xs">Connected</span>
              </div>
              <div className="flex items-center justify-between rounded-lg border border-white/10 bg-white/5 px-4 py-3">
                <span>Threads</span>
                <span className="text-white/50 text-xs">Planned</span>
              </div>
            </div>
          </Panel>

          <Panel title="Storage" subtitle="Usage">
            <div className="space-y-2 text-sm text-white/80">
              <div className="flex items-center justify-between">
                <span className="text-white/60">Used</span>
                <span className="font-semibold">38.4 GB / 120 GB</span>
              </div>
              <div className="h-2 rounded-full bg-white/10 overflow-hidden">
                <div className="h-full w-[32%] rounded-full bg-[#A4B4FF]" />
              </div>
              <p className="text-xs text-white/50">Auto-cleanup for completed jobs after 14 days.</p>
            </div>
          </Panel>

          <Panel title="Feature flags" subtitle="Disabled by default">
            <div className="space-y-2 text-sm text-white/70">
              {['AI captions v2', 'Multi-project workspaces', 'Analytics alpha', 'Scheduler v2'].map((flag) => (
                <div key={flag} className="flex items-center justify-between rounded-lg border border-white/10 bg-white/5 px-4 py-3">
                  <span>{flag}</span>
                  <span className="text-white/40 text-xs">Locked</span>
                </div>
              ))}
            </div>
          </Panel>
        </section>
      </div>
    </div>
  );
}
