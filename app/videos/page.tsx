"use client";

import React, { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { api } from "@/lib/api";
import { Badge } from "@/components/ui/badge";
import { Search, Trash2, Download, Eye, Clock, Video, ListFilter } from "lucide-react";

export default function VideosPage() {
  const [searchQuery, setSearchQuery] = useState("");
  const [videos, setVideos] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const fetchVideos = async () => {
      try {
        setIsLoading(true);
        const res = await api.video.list();
        setVideos(res.data || []);
      } catch (error) {
        console.error("Error loading videos", error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchVideos();
  }, []);

  const filteredVideos = useMemo(() => {
    return videos.filter((video) => (video.title || "Untitled").toLowerCase().includes(searchQuery.toLowerCase()));
  }, [videos, searchQuery]);

  const renderStatus = (status?: string) => {
    if (status === "completed") return <Badge className="bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200">✓ Completed</Badge>;
    if (status === "processing") return <Badge className="bg-amber-100 text-amber-800 dark:bg-amber-900 dark:text-amber-200">⟳ Processing</Badge>;
    return <Badge className="bg-muted text-foreground">Pending</Badge>;
  };

  return (
    <div className="space-y-8 max-w-6xl">
      <div className="space-y-3">
        <div className="inline-flex items-center gap-2 rounded-full border border-border/70 px-3 py-1 text-xs uppercase tracking-[0.14em] text-muted-foreground">
          <ListFilter className="h-4 w-4" /> Library
        </div>
        <h1 className="text-3xl sm:text-4xl font-bold tracking-tight">My videos, all in monochrome.</h1>
        <p className="text-muted-foreground max-w-2xl">Search, preview, and jump back into processing. No fake data—pulled straight from the backend.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-[1.1fr_0.9fr] gap-6">
        <Card className="border border-border/70 bg-card/70 shadow-soft">
          <CardHeader>
            <CardTitle>Search</CardTitle>
            <CardDescription>Filter across your processed videos.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-muted-foreground pointer-events-none" />
              <Input
                placeholder="Search videos..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10"
              />
            </div>
            <div className="text-xs text-muted-foreground">{isLoading ? "Loading..." : `${filteredVideos.length} videos`}</div>
          </CardContent>
        </Card>

        <Card className="border border-border/70 bg-card/70 shadow-soft">
          <CardHeader>
            <CardTitle>At a glance</CardTitle>
            <CardDescription>Counts update from the backend.</CardDescription>
          </CardHeader>
          <CardContent className="grid grid-cols-2 gap-3 text-sm">
            <div className="rounded-xl border border-border/60 bg-background/70 p-3 space-y-1">
              <p className="text-muted-foreground">Total videos</p>
              <p className="text-2xl font-semibold">{videos.length}</p>
            </div>
            <div className="rounded-xl border border-border/60 bg-background/70 p-3 space-y-1">
              <p className="text-muted-foreground">Completed</p>
              <p className="text-2xl font-semibold">{videos.filter((v) => v.status === "completed").length}</p>
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="space-y-4">
        {isLoading && (
          <Card className="border border-border/70 bg-card/70">
            <CardContent className="py-10 text-center text-sm text-muted-foreground">Loading videos…</CardContent>
          </Card>
        )}

        {!isLoading && filteredVideos.length === 0 && (
          <Card className="border border-border/70 bg-card/70">
            <CardContent className="py-12 text-center space-y-2">
              <p className="font-medium">No videos yet</p>
              <p className="text-sm text-muted-foreground">Add a YouTube link to start processing.</p>
              <Link href="/add-video">
                <Button>Add a video</Button>
              </Link>
            </CardContent>
          </Card>
        )}

        {!isLoading && filteredVideos.map((video) => (
          <Card key={video.id} className="border border-border/70 bg-card/70 shadow-soft">
            <CardContent className="p-5">
              <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                <div className="space-y-1">
                  <p className="font-semibold text-lg">{video.title || "Untitled video"}</p>
                  <p className="text-sm text-muted-foreground flex items-center gap-2">
                    <Clock className="h-4 w-4" /> {video.duration || "--"}
                    <span className="h-1 w-1 rounded-full bg-border" />
                    <Video className="h-4 w-4" /> {new Date(video.created_at || Date.now()).toLocaleDateString()}
                  </p>
                </div>
                <div className="flex items-center gap-3">
                  {renderStatus(video.status)}
                  <div className="flex gap-2">
                    <Link href={`/processing-status?videoId=${video.id}`}>
                      <Button variant="outline" size="icon">
                        <Eye className="h-4 w-4" />
                      </Button>
                    </Link>
                    <Button variant="outline" size="icon">
                      <Download className="h-4 w-4" />
                    </Button>
                    <Button variant="outline" size="icon" className="hover:bg-destructive/10">
                      <Trash2 className="h-4 w-4 text-destructive" />
                    </Button>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
