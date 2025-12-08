import { create } from "zustand";
import { storage } from "@/lib/utils";

interface User {
  id: string;
  email: string;
  name: string;
  avatar?: string;
}

interface AuthStore {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  setUser: (user: User | null) => void;
  setToken: (token: string | null) => void;
  setLoading: (loading: boolean) => void;
  logout: () => void;
  initialize: () => void;
}

export const useAuthStore = create<AuthStore>((set) => ({
  user: null,
  token: null,
  isLoading: false,
  setUser: (user) => {
    set({ user });
    if (user) {
      storage.set("user", user);
    } else {
      storage.remove("user");
    }
  },
  setToken: (token) => {
    set({ token });
    if (token) {
      storage.set("authToken", token);
    } else {
      storage.remove("authToken");
    }
  },
  setLoading: (loading) => set({ isLoading: loading }),
  logout: () => {
    set({ user: null, token: null });
    storage.remove("user");
    storage.remove("authToken");
  },
  initialize: () => {
    const user = storage.get("user");
    const token = storage.get("authToken");
    if (user && token) {
      set({ user, token });
    }
  },
}));

interface ReelsStore {
  reels: any[];
  selectedReel: any | null;
  isProcessing: boolean;
  setReels: (reels: any[]) => void;
  addReel: (reel: any) => void;
  selectReel: (reel: any | null) => void;
  setProcessing: (processing: boolean) => void;
}

export const useReelsStore = create<ReelsStore>((set) => ({
  reels: [],
  selectedReel: null,
  isProcessing: false,
  setReels: (reels) => set({ reels }),
  addReel: (reel) => set((state) => ({ reels: [...state.reels, reel] })),
  selectReel: (reel) => set({ selectedReel: reel }),
  setProcessing: (processing) => set({ isProcessing: processing }),
}));

interface UIStore {
  sidebarOpen: boolean;
  theme: "light" | "dark" | "system";
  toggleSidebar: () => void;
  setTheme: (theme: "light" | "dark" | "system") => void;
}

export const useUIStore = create<UIStore>((set) => ({
  sidebarOpen: true,
  theme: "system",
  toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
  setTheme: (theme) => {
    set({ theme });
    storage.set("theme", theme);
  },
}));
