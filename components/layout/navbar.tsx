"use client";

import React from "react";
import Link from "next/link";
import { useUIStore } from "@/lib/store";
import { Menu, Sparkles } from "lucide-react";

export function Navbar() {
  const { toggleSidebar } = useUIStore();

  return (
    <nav className="sticky top-0 z-40 w-full border-b border-white/10 bg-[#080B10]/80 backdrop-blur-xl">
      <div className="flex h-16 items-center justify-between px-4 sm:px-6">
        <div className="flex items-center gap-3">
          <button
            onClick={toggleSidebar}
            className="lg:hidden p-2 rounded-full border border-white/15 bg-white/5 text-white hover:bg-white/10 transition"
          >
            <Menu className="h-5 w-5" />
          </button>
          <Link href="/" className="flex items-center gap-3">
            <div className="h-9 w-9 rounded-xl border border-white/20 bg-gradient-to-br from-[#A4B4FF] to-[#F6C177] shadow-[0_10px_30px_-15px_rgba(0,0,0,0.6)]" />
            <div className="hidden sm:flex flex-col leading-tight text-white">
              <span className="font-semibold text-sm tracking-tight">YouTube → Reels Studio</span>
              <span className="text-[11px] text-white/60">Luxury control room</span>
            </div>
          </Link>
        </div>

        <div className="flex items-center gap-2 sm:gap-3 text-sm text-white/80">
          <Link
            href="/connect-instagram"
            className="inline-flex items-center gap-2 rounded-full border border-white/15 bg-white/5 px-3 py-2 hover:border-white/30 hover:bg-white/10 transition"
          >
            <Sparkles className="h-4 w-4" />
            Connect
          </Link>
          <Link
            href="/add-video"
            className="inline-flex items-center gap-2 rounded-full bg-[#F6C177] px-3 py-2 text-[#0A0C10] font-semibold shadow-[0_14px_40px_-18px_#F6C177] hover:-translate-y-0.5 transition"
          >
            Add video
          </Link>
        </div>
      </div>
    </nav>
  );
}
