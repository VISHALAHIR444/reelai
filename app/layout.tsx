import type { Metadata } from "next";
import "@/styles/globals.css";
import { RootLayout } from "@/components/layout/root-layout";

export const metadata: Metadata = {
  title: "GRAVIXAI — Convert YouTube to Instagram Reels",
  description:
    "Convert YouTube long videos to Instagram Reels automatically with GRAVIXAI. Upload, process, and share perfectly cut clips.",
  keywords: ["GRAVIXAI", "YouTube", "Instagram", "Reels", "Video AI", "Automation"],
  authors: [{ name: "GRAVIXAI" }],
  creator: "GRAVIXAI",
};

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <meta charSet="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <meta name="theme-color" content="#0f0f0f" />
      </head>
      <body>
        <RootLayout>{children}</RootLayout>
      </body>
    </html>
  );
}
