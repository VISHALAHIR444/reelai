import type { Metadata } from "next";
import "@/styles/globals.css";
import { RootLayout } from "@/components/layout/root-layout";

export const metadata: Metadata = {
  title: "Reels Studio — Convert YouTube to Instagram Reels",
  description:
    "Transform YouTube videos into viral reels with cinematic precision. AI-powered automation for creators.",
  keywords: ["Reels Studio", "YouTube", "Instagram", "Reels", "Video AI", "Automation"],
  authors: [{ name: "Reels Studio" }],
  creator: "Reels Studio",
};

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <meta charSet="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <meta name="theme-color" content="#09090b" />
      </head>
      <body>
        <RootLayout>{children}</RootLayout>
      </body>
    </html>
  );
}
