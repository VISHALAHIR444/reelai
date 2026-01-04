"use client";

import React from "react";
import { Navbar } from "@/components/layout/navbar";
import { Sidebar } from "@/components/layout/sidebar";
import { Footer } from "@/components/layout/footer";
import { ThemeProvider } from "@/lib/theme";

export function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <ThemeProvider>
      <div className="relative min-h-screen bg-background text-foreground">
        <div className="grain-overlay" aria-hidden />
        <Navbar />
        <div className="flex">
          <Sidebar />
          <main className="flex-1 lg:ml-64 px-4 sm:px-6 lg:px-10 pb-12 pt-6">
            {children}
          </main>
        </div>
        <Footer />
      </div>
    </ThemeProvider>
  );
}
