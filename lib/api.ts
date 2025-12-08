import axios, { AxiosInstance } from "axios";
import { storage } from "./utils";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

const apiClient: AxiosInstance = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Add token to requests
apiClient.interceptors.request.use((config) => {
  const token = storage.get("authToken");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      storage.remove("authToken");
      storage.remove("user");
      if (typeof window !== "undefined") {
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  }
);

// API endpoints
export const api = {
  // Auth (legacy; kept for compatibility)
  auth: {
    login: (email: string, password: string) => apiClient.post("/auth/login", { email, password }),
    signup: (name: string, email: string, password: string) => apiClient.post("/auth/signup", { name, email, password }),
    logout: () => apiClient.post("/auth/logout"),
    getMe: () => apiClient.get("/auth/me"),
  },

  // Video pipeline (aligns with backend /api/video routes)
  video: {
    uploadYoutube: (youtubeUrl: string) => apiClient.post("/video/youtube", { youtube_url: youtubeUrl }),
    list: () => apiClient.get("/video"),
    get: (videoId: string) => apiClient.get(`/video/${videoId}`),
    process: (videoId: string) => apiClient.post(`/video/${videoId}/process`),
    status: (videoId: string) => apiClient.get(`/video/${videoId}/status`),
  },

  // Reels (aligns with backend /api/reels routes)
  reels: {
    list: (params?: { status?: string; skip?: number; limit?: number }) =>
      apiClient.get("/reels", { params }),
    getDetails: (reelId: string) => apiClient.get(`/reels/${reelId}/details`),
    getByVideo: (videoId: string, params?: { skip?: number; limit?: number }) =>
      apiClient.get(`/reels/${videoId}`, { params }),
    publish: (reelId: string) => apiClient.post(`/reels/${reelId}/publish`),
    pendingPublishCount: () => apiClient.get(`/reels/pending-publish/count`),
  },

  // Instagram
  instagram: {
    connect: (code: string) => apiClient.post("/instagram/connect", { code }),
    disconnect: () => apiClient.post("/instagram/disconnect"),
    upload: (reelId: string) => apiClient.post(`/instagram/upload/${reelId}`),
    getStatus: () => apiClient.get("/instagram/status"),
  },

  // Social Accounts
  social: {
    getFacebookLoginUrl: () => apiClient.post("/social/facebook/login"),
    getSocialStatus: () => apiClient.get("/social/status"),
    refreshToken: () => apiClient.post("/social/refresh-token"),
    disconnect: () => apiClient.delete("/social/disconnect"),
    checkConnection: () => apiClient.get("/social/check"),
  },

  // User Settings
  user: {
    update: (data: any) => apiClient.put("/user", data),
    getSettings: () => apiClient.get("/user/settings"),
    updateSettings: (data: any) => apiClient.put("/user/settings", data),
  },
};

export default apiClient;
