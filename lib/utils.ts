import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// Storage utilities
export const storage = {
  get: (key: string) => {
    if (typeof window === "undefined") return null;
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : null;
    } catch (error) {
      console.error(`Error reading from storage:`, error);
      return null;
    }
  },
  set: (key: string, value: any) => {
    if (typeof window === "undefined") return;
    try {
      window.localStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
      console.error(`Error writing to storage:`, error);
    }
  },
  remove: (key: string) => {
    if (typeof window === "undefined") return;
    try {
      window.localStorage.removeItem(key);
    } catch (error) {
      console.error(`Error removing from storage:`, error);
    }
  },
};

// Format utilities
export const formatDuration = (seconds: number): string => {
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const secs = Math.floor(seconds % 60);

  if (hours > 0) {
    return `${hours}h ${minutes}m`;
  }
  if (minutes > 0) {
    return `${minutes}m ${secs}s`;
  }
  return `${secs}s`;
};

export const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return "0 Bytes";
  const k = 1024;
  const sizes = ["Bytes", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + " " + sizes[i];
};

export const formatDate = (date: Date | string): string => {
  const d = typeof date === "string" ? new Date(date) : date;
  return d.toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
};

// Validation utilities
export const isValidYoutubeUrl = (url: string): boolean => {
  const youtubeRegex =
    /^(?:https?:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)\/(?:watch\?v=|)([^\s&]+)/;
  return youtubeRegex.test(url);
};

export const extractVideoId = (url: string): string | null => {
  const youtubeRegex =
    /(?:https?:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)\/(?:watch\?v=|)([^\s&]+)/;
  const match = url.match(youtubeRegex);
  return match ? match[1] : null;
};
