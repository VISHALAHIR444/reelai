"use client";

import React from "react";
import { Navbar } from "@/components/layout/navbar";
import { Sidebar } from "@/components/layout/sidebar";
import { Footer } from "@/components/layout/footer";
import { ThemeProvider } from "@/lib/theme";

export function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <ThemeProvider>
      <div className="relative flex min-h-screen flex-col bg-background">
        <div className="pointer-events-none absolute inset-0 opacity-70" aria-hidden>
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_20%_20%,rgba(0,0,0,0.06),transparent_35%),radial-gradient(circle_at_80%_10%,rgba(0,0,0,0.04),transparent_30%),radial-gradient(circle_at_40%_80%,rgba(0,0,0,0.05),transparent_35%)]" />
          <div className="absolute inset-0 bg-[linear-gradient(115deg,rgba(0,0,0,0.06),transparent_45%,rgba(0,0,0,0.05))]" />
        </div>
        <Navbar />
        <div className="flex flex-1">
          <Sidebar />
          <main className="flex-1 lg:ml-64">
            <div className="relative p-4 sm:p-6 lg:p-8">
              <div className="absolute inset-0 rounded-2xl border border-border/50" aria-hidden></div>
              <div className="relative">
                {children}
              </div>
            </div>
          </main>
        </div>
        <Footer />
      </div>
    </ThemeProvider>
  );
}
