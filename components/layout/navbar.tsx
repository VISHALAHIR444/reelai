"use client";

import React from "react";
import Link from "next/link";
import { useUIStore } from "@/lib/store";
import { Menu, Sparkles } from "lucide-react";

export function Navbar() {
  const { toggleSidebar } = useUIStore();

  return (
    <nav className="sticky top-0 z-40 w-full border-b border-border/50 bg-background/80 backdrop-blur-xl">
      <div className="flex h-16 items-center justify-between px-4 sm:px-6">
        {/* Left side */}
        <div className="flex items-center gap-3">
          <button
            onClick={toggleSidebar}
            className="lg:hidden p-2 rounded-full border border-border/60 hover:bg-foreground hover:text-background transition-colors"
          >
            <Menu className="h-5 w-5" />
          </button>
          <Link href="/" className="flex items-center gap-3">
            <div className="h-9 w-9 rounded-lg border border-border bg-foreground" />
            <div className="hidden sm:flex flex-col leading-tight">
              <span className="font-semibold text-foreground text-base tracking-tight">GRAVIXAI</span>
              <span className="text-xs text-muted-foreground">YouTube → Reels, monochrome</span>
            </div>
          </Link>
        </div>

        {/* Right side */}
        <div className="flex items-center gap-2 sm:gap-3 text-sm text-muted-foreground">
          <Link
            href="/connect-instagram"
            className="inline-flex items-center gap-2 rounded-full border border-border px-3 py-2 hover:bg-foreground hover:text-background transition-colors"
          >
            <Sparkles className="h-4 w-4" />
            Connect
          </Link>
          <Link
            href="/add-video"
            className="inline-flex items-center gap-2 rounded-full bg-foreground text-background px-3 py-2 hover:bg-foreground/90 transition-colors"
          >
            Add Video
          </Link>
        </div>
      </div>
    </nav>
  );
}
