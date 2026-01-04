# AutoReels AI - Frontend

A modern, premium-quality Next.js frontend for converting YouTube long-form videos into Instagram Reels. Built with cutting-edge technologies and best practices for production deployment.

## 🚀 **NEW USER? START HERE!**

**→ See [START_HERE.md](./START_HERE.md) for a simple guide to run the website on your local machine.**

This is a **full-stack application** that requires both frontend (Next.js) and backend (FastAPI) servers to be running on your computer.

---

## 🎯 Features

- **Modern UI**: Glassmorphism + gradient design with premium aesthetics
- **Dark/Light Theme**: Full theme support with system preference detection
- **Responsive Design**: Mobile-first layout that works on all devices
- **Dashboard-Style**: Comprehensive analytics and video management
- **Instagram Integration**: Direct connection and upload to Instagram
- **Real-time Processing**: Track video processing status in real-time
- **Reel Preview**: Preview and edit reels before upload
- **Authentication**: Secure login/signup with token management

## 📋 Tech Stack

- **Next.js 15+**: Latest React framework
- **TypeScript**: Type-safe development
- **TailwindCSS**: Utility-first styling
- **Shadcn UI**: Premium UI components
- **Zustand**: State management
- **Axios**: API client
- **React Hot Toast**: Toast notifications
- **Lucide Icons**: Beautiful icon set

## 📁 Project Structure

```
autoreels-ai/
├── app/                          # Next.js app directory
│   ├── layout.tsx               # Root layout
│   ├── page.tsx                 # Landing page
│   ├── login/                   # Authentication
│   ├── signup/
│   ├── dashboard/               # Main dashboard
│   ├── add-video/               # Video upload/processing
│   ├── processing-status/       # Processing tracker
│   ├── preview/                 # Reel preview
│   ├── connect-instagram/       # Instagram integration
│   ├── settings/                # User settings
│   └── videos/                  # Video management
├── components/
│   ├── ui/                      # Shadcn UI components
│   │   ├── button.tsx
│   │   ├── input.tsx
│   │   ├── card.tsx
│   │   ├── dialog.tsx
│   │   ├── dropdown-menu.tsx
│   │   ├── label.tsx
│   │   ├── progress.tsx
│   │   └── select.tsx
│   └── layout/                  # Layout components
│       ├── navbar.tsx           # Top navigation
│       ├── sidebar.tsx          # Side navigation
│       ├── footer.tsx           # Footer
│       └── root-layout.tsx      # Root layout wrapper
├── lib/
│   ├── api.ts                   # API client setup
│   ├── store.ts                 # Zustand stores
│   ├── theme.tsx                # Theme provider
│   └── utils.ts                 # Utility functions
├── styles/
│   └── globals.css              # Global styles
├── .env.example                 # Environment variables template
├── next.config.js               # Next.js configuration
├── tailwind.config.js           # TailwindCSS configuration
├── tsconfig.json                # TypeScript configuration
└── package.json                 # Dependencies

## 🚀 Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn package manager

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd autoreels-ai
```

2. **Install dependencies**
```bash
npm install
# or
yarn install
```

3. **Setup environment variables**
```bash
cp .env.example .env.local
```

Edit `.env.local` and update the following:
```env
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:3001/api

# Instagram OAuth
NEXT_PUBLIC_INSTAGRAM_CLIENT_ID=your_instagram_app_id
NEXT_PUBLIC_INSTAGRAM_REDIRECT_URI=http://localhost:3000/connect-instagram

# App Configuration
NEXT_PUBLIC_APP_NAME=AutoReels AI
```

4. **Run development server**
```bash
npm run dev
# or
yarn dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## 🏗️ Build for Production

### Building the project

```bash
npm run build
# or
yarn build
```

### Starting production server

```bash
npm run start
# or
yarn start
```

## 📦 Deployment

### Deploy to Vercel (Recommended)

```bash
npm install -g vercel
vercel
```

### Deploy to VPS (Linux)

1. **Install Node.js and npm**
```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
```

2. **Clone repository**
```bash
cd /var/www
git clone <repository-url> autoreels-ai
cd autoreels-ai
```

3. **Install dependencies and build**
```bash
npm install
npm run build
```

4. **Setup with PM2** (Process manager)
```bash
sudo npm install -g pm2
pm2 start npm --name "autoreels-ai" -- start
pm2 startup
pm2 save
```

5. **Setup with Nginx** (Reverse proxy)
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

6. **Setup SSL with Certbot**
```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

## 🔐 Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | `http://localhost:3001/api` |
| `NEXT_PUBLIC_INSTAGRAM_CLIENT_ID` | Instagram App ID | `your_app_id` |
| `NEXT_PUBLIC_INSTAGRAM_REDIRECT_URI` | Instagram OAuth redirect | `http://localhost:3000/connect-instagram` |
| `NEXT_PUBLIC_APP_NAME` | Application name | `AutoReels AI` |

## 📄 Pages Overview

### Public Pages
- **Landing Page** (`/`): Hero, features, CTA
- **Login** (`/login`): Email/password authentication
- **Signup** (`/signup`): Account creation

### Protected Pages
- **Dashboard** (`/dashboard`): Stats, recent videos, quick actions
- **Add Video** (`/add-video`): YouTube URL input, processing options
- **Processing Status** (`/processing-status`): Real-time processing tracker
- **Preview** (`/preview`): Reel preview and management
- **Connect Instagram** (`/connect-instagram`): Instagram OAuth integration
- **Videos** (`/videos`): Video library and management
- **Settings** (`/settings`): User profile and preferences

## 🎨 Customization

### Theme Colors

Edit `tailwind.config.js` to change the primary colors:

```js
extend: {
  colors: {
    primary: 'your-color',
    // ... more colors
  }
}
```

### Component Styling

All UI components are in `components/ui/` and use TailwindCSS. Modify them to match your brand.

## 🔗 API Integration

The frontend expects these API endpoints:

### Authentication
- `POST /auth/login` - Login
- `POST /auth/signup` - Signup
- `POST /auth/logout` - Logout
- `GET /auth/me` - Get current user

### Videos
- `GET /videos` - List user's videos
- `POST /videos` - Create video
- `GET /videos/:id` - Get video details
- `DELETE /videos/:id` - Delete video

### Reels
- `GET /reels` - List user's reels
- `POST /reels/process` - Start reel processing
- `GET /reels/:id` - Get reel details

### Instagram
- `POST /instagram/connect` - Connect Instagram
- `POST /instagram/disconnect` - Disconnect Instagram
- `POST /instagram/upload/:reelId` - Upload reel to Instagram
- `GET /instagram/status` - Get connection status

## 📚 Component Documentation

### Button Component
```tsx
<Button variant="default" size="lg">
  Action
</Button>

// Variants: default, destructive, outline, secondary, ghost, link
// Sizes: default, sm, lg, icon
```

### Card Component
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

## 🐛 Troubleshooting

### Port 3000 already in use
```bash
npm run dev -- -p 3001
```

### Build errors
```bash
rm -rf .next
npm run build
```

### Styling issues
```bash
# Rebuild TailwindCSS
npm run dev
```

## 📝 License

This project is proprietary. All rights reserved.

## 🤝 Support

For support, contact: support@autoreels-ai.com

## 🚀 Performance Tips

1. Use Next.js Image component for optimized images
2. Enable static generation where possible
3. Implement code splitting for large bundles
4. Monitor Core Web Vitals in Vercel Analytics
5. Use CDN for static assets

## 📞 Backend Integration Checklist

- [ ] Setup backend API server
- [ ] Configure CORS settings
- [ ] Setup authentication tokens
- [ ] Implement video processing logic
- [ ] Setup Instagram OAuth app
- [ ] Configure database
- [ ] Setup email notifications
- [ ] Implement file upload storage

## 🎓 Best Practices

1. **Authentication**: Always validate tokens on backend
2. **Security**: Never expose sensitive keys in client code
3. **Performance**: Use React.memo for heavy components
4. **Accessibility**: Follow WCAG guidelines
5. **Testing**: Write tests for critical paths

---

**Built with ❤️ for content creators**
