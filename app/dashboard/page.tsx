"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { BarChart3, Play, Plus, TrendingUp, Video, Clock, AlertCircle, ShieldCheck, PlugZap } from "lucide-react";
import { api } from "@/lib/api";

export default function Dashboard() {
  const [stats, setStats] = useState({
    totalVideos: 0,
    totalReels: 0,
    processingTime: "—",
    conversionRate: "—",
  });
  const [recentVideos, setRecentVideos] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [videosResp, reelsResp] = await Promise.all([
          api.video.list(),
          api.reels.list({ limit: 50 }),
        ]);

        const videos = videosResp.data || [];
        const reels = reelsResp.data || [];

        setRecentVideos(videos.slice(0, 4));
        setStats({
          totalVideos: videos.length,
          totalReels: reels.length,
          processingTime: "—",
          conversionRate: "—",
        });
      } catch (error) {
        console.error("Error fetching dashboard data:", error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, []);

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="space-y-2">
        <div className="inline-flex items-center gap-2 rounded-full border border-border/70 px-3 py-1 text-xs uppercase tracking-[0.14em] text-muted-foreground">
          <ShieldCheck className="h-4 w-4" /> Live workspace
        </div>
        <h1 className="text-3xl sm:text-4xl font-bold tracking-tight">
          GRAVIXAI control room
        </h1>
        <p className="text-muted-foreground">
          Monitor processing, reels, and Instagram link status in one monochrome view.
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          { title: "Total Videos", value: stats.totalVideos, icon: Video },
          { title: "Total Reels", value: stats.totalReels, icon: Play },
          { title: "Avg Processing", value: stats.processingTime, icon: Clock },
          { title: "Quality Score", value: `${stats.conversionRate}%`, icon: TrendingUp },
        ].map((stat, idx) => {
          const Icon = stat.icon;
          return (
            <Card key={idx} className="border border-border/70 bg-card/70 shadow-soft">
              <CardContent className="pt-6 space-y-4">
                <div className="flex items-center justify-between">
                  <div className="text-sm text-muted-foreground">{stat.title}</div>
                  <div className="p-2 rounded-lg border border-border/60">
                    <Icon className="h-5 w-5" />
                  </div>
                </div>
                <p className="text-3xl font-bold">{stat.value}</p>
              </CardContent>
            </Card>
          );
        })}
      </div>

      {/* Main Content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Recent Activity */}
        <div className="lg:col-span-2 space-y-6">
          <Card className="border border-border/70 bg-card/70 shadow-soft">
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle>Recent Videos</CardTitle>
                  <CardDescription>
                    Your latest video conversions
                  </CardDescription>
                </div>
                <Link href="/videos">
                  <Button variant="outline" size="sm">View all</Button>
                </Link>
              </div>
            </CardHeader>
            <CardContent>
              {isLoading ? (
                <div className="text-sm text-muted-foreground">Loading…</div>
              ) : recentVideos.length === 0 ? (
                <div className="text-center py-12 space-y-4">
                  <AlertCircle className="h-12 w-12 mx-auto text-muted-foreground" />
                  <div>
                    <p className="font-medium">No videos yet</p>
                    <p className="text-sm text-muted-foreground">
                      Upload your first video to get started
                    </p>
                  </div>
                  <Link href="/add-video">
                    <Button>Add Your First Video</Button>
                  </Link>
                </div>
              ) : (
                <div className="space-y-4">
                  {recentVideos.map((video) => (
                    <div
                      key={video.id}
                      className="flex items-center justify-between gap-4 p-4 rounded-xl border border-border/60 bg-background/70"
                    >
                      <div className="space-y-1">
                        <p className="font-medium">{video.title || "Untitled video"}</p>
                        <p className="text-sm text-muted-foreground">
                          {video.status ? video.status : "Pending"}
                        </p>
                      </div>
                      <div className="flex items-center gap-3">
                        {video.status === "processing" && (
                          <div className="w-32 space-y-1">
                            <Progress value={video.progress ?? 35} />
                            <p className="text-xs text-right text-muted-foreground">
                              {video.progress ?? 35}%
                            </p>
                          </div>
                        )}
                        <div
                          className={`px-3 py-1 rounded-full text-xs font-medium ${
                            video.status === "completed"
                              ? "bg-green-100 text-green-700 dark:bg-green-950 dark:text-green-300"
                              : "bg-amber-100 text-amber-700 dark:bg-amber-950 dark:text-amber-300"
                          }`}
                        >
                          {video.status === "completed" ? "✓ Completed" : "⟳ Processing"}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Quick Actions */}
        <div>
          <Card className="sticky top-20 border border-border/70 bg-card/70 shadow-soft">
            <CardHeader>
              <CardTitle>System</CardTitle>
              <CardDescription>Quick actions stay on one side.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              <Link href="/add-video">
                <Button className="w-full">
                  <Plus className="mr-2 h-4 w-4" />
                  Add new video
                </Button>
              </Link>
              <Link href="/connect-instagram">
                <Button variant="outline" className="w-full">
                  <Play className="mr-2 h-4 w-4" />
                  Connect Instagram
                </Button>
              </Link>
              <Link href="/settings">
                <Button variant="outline" className="w-full">
                  <BarChart3 className="mr-2 h-4 w-4" />
                  View settings
                </Button>
              </Link>
              <div className="rounded-lg border border-border/60 bg-background/70 p-3 text-sm text-muted-foreground space-y-1">
                <div className="flex items-center justify-between">
                  <span>IG link</span>
                  <span className="font-medium">Live</span>
                </div>
                <div className="flex items-center justify-between">
                  <span>Jobs</span>
                  <span className="font-medium">2 running</span>
                </div>
                <div className="flex items-center justify-between">
                  <span>Queue</span>
                  <span className="font-medium">Stable</span>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
