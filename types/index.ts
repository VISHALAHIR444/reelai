// Global type definitions for AutoReels AI

// User Types
export interface User {
  id: string;
  email: string;
  name: string;
  avatar?: string;
  createdAt: Date;
}

// Video Types
export interface Video {
  id: string;
  userId: string;
  title: string;
  youtubeUrl: string;
  duration: number;
  thumbnail: string;
  status: "processing" | "completed" | "failed";
  reelsCount: number;
  createdAt: Date;
  updatedAt: Date;
}

// Reel Types
export interface Reel {
  id: string;
  videoId: string;
  title: string;
  duration: number;
  thumbnail: string;
  videoUrl: string;
  status: "ready" | "published" | "failed";
  instagramId?: string;
  instagramUrl?: string;
  createdAt: Date;
  updatedAt: Date;
}

// Instagram Types
export interface InstagramAccount {
  id: string;
  userId: string;
  handle: string;
  accessToken: string;
  refreshToken?: string;
  expiresAt?: Date;
  connectedAt: Date;
}

// Processing Types
export interface ProcessingStatus {
  videoId: string;
  progress: number;
  currentStep: string;
  status: "processing" | "completed" | "failed";
  estimatedTime: number;
  error?: string;
}

// API Response Types
export interface ApiResponse<T> {
  success: boolean;
  data: T;
  error?: string;
  message?: string;
}

export interface ApiError {
  statusCode: number;
  message: string;
  error: string;
}

// Settings Types
export interface UserSettings {
  userId: string;
  theme: "light" | "dark" | "system";
  notifications: {
    email: boolean;
    processing: boolean;
    upload: boolean;
  };
  defaultCaption: string;
  defaultHashtags: string[];
}
