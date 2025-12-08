# AutoReels AI - Project Overview

## 📋 Table of Contents
- [Project Structure](#project-structure)
- [File Descriptions](#file-descriptions)
- [Component Architecture](#component-architecture)
- [State Management](#state-management)
- [API Integration](#api-integration)
- [Styling System](#styling-system)

---

## 🏗️ Project Structure

```
autoreels-ai/
├── app/                          # Next.js App Router
│   ├── layout.tsx               # Root layout with providers
│   ├── page.tsx                 # Landing page
│   ├── login/
│   │   └── page.tsx             # Login page
│   ├── signup/
│   │   └── page.tsx             # Signup page
│   ├── dashboard/
│   │   └── page.tsx             # Main dashboard
│   ├── add-video/
│   │   └── page.tsx             # Add/process video
│   ├── processing-status/
│   │   └── page.tsx             # Processing tracker
│   ├── preview/
│   │   └── page.tsx             # Reel preview
│   ├── connect-instagram/
│   │   └── page.tsx             # Instagram integration
│   ├── settings/
│   │   └── page.tsx             # User settings
│   ├── videos/
│   │   └── page.tsx             # Video management
│   ├── globals.css              # Global styles
│   └── layout.tsx               # Main layout
│
├── components/
│   ├── ui/                      # Shadcn UI Components
│   │   ├── button.tsx           # Button component
│   │   ├── input.tsx            # Input field
│   │   ├── card.tsx             # Card container
│   │   ├── dialog.tsx           # Modal/Dialog
│   │   ├── dropdown-menu.tsx    # Dropdown menu
│   │   ├── label.tsx            # Form label
│   │   ├── progress.tsx         # Progress bar
│   │   ├── select.tsx           # Select dropdown
│   │   └── tabs.tsx             # Tab component
│   │
│   └── layout/                  # Layout Components
│       ├── navbar.tsx           # Top navigation bar
│       ├── sidebar.tsx          # Side navigation
│       ├── footer.tsx           # Footer
│       └── root-layout.tsx      # Root layout wrapper
│
├── lib/
│   ├── api.ts                   # API client & endpoints
│   ├── store.ts                 # Zustand state stores
│   ├── theme.tsx                # Theme provider & hook
│   └── utils.ts                 # Utility functions
│
├── styles/
│   └── globals.css              # Global TailwindCSS
│
├── public/                      # Static assets
│
├── Configuration Files
│   ├── next.config.ts           # Next.js config
│   ├── tsconfig.json            # TypeScript config
│   ├── tailwind.config.ts       # TailwindCSS config
│   ├── postcss.config.js        # PostCSS config
│   └── package.json             # Dependencies
│
├── Documentation
│   ├── README.md                # Main documentation
│   ├── DEPLOYMENT.md            # Deployment guide
│   ├── ARCHITECTURE.md          # This file
│   └── .env.example             # Environment template
│
└── Scripts
    ├── setup.sh                 # Setup script
    └── .gitignore               # Git ignore rules
```

---

## 📄 File Descriptions

### Core Application Files

| File | Purpose |
|------|---------|
| `app/layout.tsx` | Root layout with HTML structure and metadata |
| `app/page.tsx` | Landing page with hero, features, and CTA |
| `styles/globals.css` | Global styles, CSS variables, and theme |
| `lib/api.ts` | Axios instance, API endpoints, interceptors |
| `lib/store.ts` | Zustand stores for auth, reels, UI state |
| `lib/theme.tsx` | ThemeProvider, useTheme hook |
| `lib/utils.ts` | Helper functions, validation, formatting |

### Pages

| Page | Path | Purpose |
|------|------|---------|
| Landing | `/` | Hero, features, CTA |
| Login | `/login` | Email/password login |
| Signup | `/signup` | Account creation |
| Dashboard | `/dashboard` | Stats, recent videos, quick actions |
| Add Video | `/add-video` | YouTube URL input, options |
| Processing | `/processing-status` | Real-time processing tracker |
| Preview | `/preview` | Reel preview and management |
| Instagram | `/connect-instagram` | Instagram OAuth connection |
| Settings | `/settings` | User profile, appearance, notifications |
| Videos | `/videos` | Video library management |

### Components

#### UI Components (Shadcn-based)
- `button.tsx` - Primary CTA button with variants
- `input.tsx` - Text input with icons support
- `card.tsx` - Card container with header/footer
- `dialog.tsx` - Modal dialog box
- `dropdown-menu.tsx` - Dropdown menu with submenus
- `label.tsx` - Form label
- `progress.tsx` - Progress bar with gradient
- `select.tsx` - Dropdown select
- `tabs.tsx` - Tab navigation

#### Layout Components
- `navbar.tsx` - Top navigation with user menu
- `sidebar.tsx` - Collapsible side navigation
- `footer.tsx` - Footer with links and socials
- `root-layout.tsx` - Root wrapper with all layouts

---

## 🎨 Component Architecture

### Design System

#### Colors
```css
Primary: #667eea (Blue) → #764ba2 (Purple)
Gradients: Blue to Purple gradient
Dark Theme: Dark blue to purple
```

#### Spacing
- Base unit: 4px (TailwindCSS)
- Padding: 4, 6, 8, 12, 16, 24px
- Gaps: 2, 3, 4, 6, 8px

#### Typography
- Font: System fonts (SF Pro, Helvetica, Arial)
- Headings: 32px (h1), 24px (h2), 20px (h3)
- Body: 16px (base), 14px (small)

#### Rounded Corners
- lg: 0.5rem (8px)
- md: 0.375rem (6px)
- sm: 0.25rem (4px)

### Component Patterns

#### Button
```tsx
<Button variant="default" size="lg">
  Action
</Button>
// Variants: default, destructive, outline, secondary, ghost, link
// Sizes: default, sm, lg, icon
```

#### Card
```tsx
<Card>
  <CardHeader>
    <CardTitle>Title</CardTitle>
    <CardDescription>Description</CardDescription>
  </CardHeader>
  <CardContent>Content</CardContent>
  <CardFooter>Footer</CardFooter>
</Card>
```

#### Dialog
```tsx
<Dialog open={isOpen} onOpenChange={setIsOpen}>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Title</DialogTitle>
    </DialogHeader>
    Content
  </DialogContent>
</Dialog>
```

---

## 📊 State Management

### Zustand Stores

#### `useAuthStore`
```typescript
- user: User | null
- token: string | null
- isLoading: boolean
- setUser(user)
- setToken(token)
- setLoading(loading)
- logout()
- initialize()
```

#### `useReelsStore`
```typescript
- reels: any[]
- selectedReel: any | null
- isProcessing: boolean
- setReels(reels)
- addReel(reel)
- selectReel(reel)
- setProcessing(processing)
```

#### `useUIStore`
```typescript
- sidebarOpen: boolean
- theme: "light" | "dark" | "system"
- toggleSidebar()
- setTheme(theme)
```

### Context API

#### ThemeProvider
- Manages light/dark theme
- Persists theme preference
- useTheme hook for theme access

---

## 🔌 API Integration

### Base URL
```
Development: http://localhost:3001/api
Production: https://api.yourdomain.com/api
```

### Authentication Endpoints
```
POST   /auth/login          - Login
POST   /auth/signup         - Register
POST   /auth/logout         - Logout
GET    /auth/me             - Get current user
```

### Video Endpoints
```
GET    /videos              - List videos
POST   /videos              - Create video
GET    /videos/:id          - Get video
DELETE /videos/:id          - Delete video
```

### Reel Endpoints
```
GET    /reels               - List reels
POST   /reels/process       - Start processing
GET    /reels/:id           - Get reel
GET    /reels/video/:id     - Get reels by video
DELETE /reels/:id           - Delete reel
```

### Instagram Endpoints
```
POST   /instagram/connect   - Connect account
POST   /instagram/disconnect- Disconnect account
POST   /instagram/upload    - Upload reel
GET    /instagram/status    - Get status
```

### Request/Response Format
```typescript
// Request
{
  method: "GET" | "POST" | "PUT" | "DELETE",
  headers: {
    "Authorization": "Bearer token",
    "Content-Type": "application/json"
  },
  body: { /* data */ }
}

// Response
{
  success: boolean,
  data: { /* response */ },
  error?: string
}
```

---

## 🎨 Styling System

### TailwindCSS Configuration

#### Color Variables
```css
--primary: 221.2 83.2% 53.3%
--secondary: 217.2 91.2% 59.8%
--accent: 221.2 83.2% 53.3%
--background: 0 0% 100% (light) / 222.2 84% 4.9% (dark)
--foreground: 222.2 84% 4.9% (light) / 210 40% 98% (dark)
```

#### Responsive Breakpoints
```
sm: 640px
md: 768px
lg: 1024px
xl: 1280px
2xl: 1536px
```

#### Animations
```css
fade-in: 0.3s ease-out
slide-down: 0.3s ease-out
accordion-down: 0.2s ease-out
```

### CSS Architecture

```
globals.css
├── @tailwind base
├── @tailwind components
├── @tailwind utilities
└── Custom styles (scrollbar, selection, etc.)
```

---

## 🔒 Security Considerations

### Authentication
- JWT token storage in localStorage
- Token sent in Authorization header
- Auto-logout on 401 response
- Secure environment variables

### CORS
- Configure CORS in backend
- Use HTTPS in production
- Validate redirects

### Input Validation
- YouTube URL validation
- Form input sanitization
- XSS protection via Content Security Policy

### Sensitive Data
- Environment variables not exposed
- API keys kept server-side
- Tokens cleared on logout

---

## 🚀 Performance Optimizations

### Code Splitting
- Dynamic imports for heavy components
- Route-based code splitting
- Lazy loading images

### Caching
- Browser cache for static assets
- Service Workers (future implementation)
- Optimized database queries

### Bundle Size
- Tailwind CSS tree-shaking
- Unused icon removal
- Minified builds

### Database Queries
- Pagination implementation
- Database indexing
- Query optimization

---

## 📱 Responsive Design

### Mobile First Approach
```
Mobile: 320px (base)
Tablet: 768px (md breakpoint)
Desktop: 1024px (lg breakpoint)
Large: 1280px+ (xl breakpoint)
```

### Layout Breakpoints
- Sidebar hidden on mobile
- Hamburger menu < 1024px
- Grid columns adjust with screen size
- Images scale responsively

---

## 🧪 Testing Strategy

### Unit Tests
- Component rendering
- Utility functions
- Store mutations

### Integration Tests
- API calls
- Authentication flow
- Data flow between components

### E2E Tests
- Complete user journeys
- Form submissions
- Instagram upload flow

---

## 🔄 Data Flow

```
User Input → Component State → Zustand Store → API Call → Backend
                    ↓
            Re-render Component
                    ↓
            Update UI with Response
```

---

## 📦 Dependencies Overview

### Core
- `next` - React framework
- `react`, `react-dom` - React library

### UI
- `@radix-ui/*` - Accessible components
- `lucide-react` - Icons
- `tailwindcss` - Styling

### State & API
- `zustand` - State management
- `axios` - HTTP client

### Utilities
- `clsx` - Class composition
- `tailwind-merge` - Tailwind utilities
- `react-hot-toast` - Notifications

---

## 🚀 Future Enhancements

- [ ] Video uploading progress
- [ ] Advanced reel editing
- [ ] Multiple platform support (TikTok, YouTube Shorts)
- [ ] Analytics dashboard
- [ ] Batch processing
- [ ] AI captions/subtitles
- [ ] Watermark customization
- [ ] Mobile app (React Native)

---

**Version**: 1.0.0  
**Last Updated**: December 2024  
**Maintainer**: AutoReels AI Team
