#!/bin/bash

# AutoReels AI - Complete Setup and Installation Guide
# This file contains all necessary setup steps

cat << 'EOF'

╔══════════════════════════════════════════════════════════════════════╗
║                     AutoReels AI - Setup Guide                      ║
║                   Premium YouTube to Instagram Reels                 ║
╚══════════════════════════════════════════════════════════════════════╝

🎯 PROJECT OVERVIEW:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  AutoReels AI is a modern, production-ready frontend for converting
  long-form YouTube videos into multiple sequential Instagram Reels.
  
  ✨ Key Features:
    • Modern UI with glassmorphism & gradients
    • Dark/Light theme support
    • Full authentication system
    • Real-time processing status
    • Reel preview & management
    • Direct Instagram integration
    • Responsive mobile-first design

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 SYSTEM REQUIREMENTS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Minimum:
    • Node.js 18.0 or higher
    • npm 9.0 or higher (or yarn 3.0+)
    • 500MB free disk space
    • Modern web browser (Chrome, Firefox, Safari, Edge)

  Recommended:
    • Node.js 20 LTS
    • npm 10+
    • 1GB RAM
    • SSD storage

  For VPS Deployment:
    • Ubuntu 20.04 LTS or later
    • 2GB RAM minimum
    • 20GB disk space
    • Root or sudo access

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 INSTALLATION OPTIONS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

OPTION 1: Local Development (Linux/macOS/Windows)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  1. Install Node.js
     - Visit: https://nodejs.org/
     - Download LTS version (20+)
     - Install and verify: node -v && npm -v

  2. Clone Repository
     $ git clone <repository-url>
     $ cd autoreels-ai

  3. Install Dependencies
     $ npm install
     (Takes ~2-3 minutes)

  4. Setup Environment
     $ cp .env.example .env.local
     
     Edit .env.local:
     NEXT_PUBLIC_API_URL=http://localhost:3001/api
     NEXT_PUBLIC_INSTAGRAM_CLIENT_ID=your_app_id_here
     NEXT_PUBLIC_INSTAGRAM_REDIRECT_URI=http://localhost:3000/connect-instagram

  5. Start Development Server
     $ npm run dev
     
     Open: http://localhost:3000

  6. Stop Server
     Press Ctrl+C in terminal


OPTION 2: Docker (Linux/macOS/Windows with Docker)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Prerequisites: Docker Desktop (https://www.docker.com/)

  1. Create Dockerfile (if not exists)
     $ docker build -t autoreels-ai .

  2. Run Container
     $ docker run -p 3000:3000 autoreels-ai

  3. Using Docker Compose
     $ docker-compose up

  4. Access Application
     Open: http://localhost:3000

  5. Stop Container
     $ docker stop <container_id>
     $ docker-compose down


OPTION 3: VPS Deployment (Ubuntu 20.04+)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  See DEPLOYMENT.md for complete VPS setup instructions.

  Quick Steps:
  1. SSH into your VPS
  2. Install Node.js, Nginx, SSL
  3. Clone repository
  4. Setup environment variables
  5. Build application
  6. Configure reverse proxy
  7. Enable HTTPS


OPTION 4: Vercel (Recommended for Production)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  1. Sign up at https://vercel.com
  2. Import Git repository
  3. Set environment variables
  4. Deploy (auto-deployed on git push)
  5. Access via Vercel domain or custom domain

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚙️ DEVELOPMENT COMMANDS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  npm run dev          Start development server (with hot reload)
  npm run build        Build for production
  npm run start        Start production server
  npm run lint         Run ESLint checks
  npm run type-check   Check TypeScript types

  Development Tips:
  • Development server runs on http://localhost:3000
  • Hot reload enabled - changes update instantly
  • Open browser DevTools (F12) for debugging
  • Check console for any errors

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔧 ENVIRONMENT VARIABLES GUIDE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Variable                            | Purpose
  ─────────────────────────────────────────────────────────────────
  NEXT_PUBLIC_API_URL                 | Backend API base URL
  NEXT_PUBLIC_INSTAGRAM_CLIENT_ID     | Instagram App ID
  NEXT_PUBLIC_INSTAGRAM_REDIRECT_URI  | OAuth callback URL
  NEXT_PUBLIC_APP_NAME                | Application name
  NODE_ENV                            | development/production

  Example .env.local:
  ─────────────────────────────────────────────────────────────────
  NEXT_PUBLIC_API_URL=http://localhost:3001/api
  NEXT_PUBLIC_INSTAGRAM_CLIENT_ID=123456789
  NEXT_PUBLIC_INSTAGRAM_REDIRECT_URI=http://localhost:3000/connect-instagram
  NEXT_PUBLIC_APP_NAME=AutoReels AI

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 PROJECT STRUCTURE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  autoreels-ai/
  ├── app/                  # Next.js pages and routes
  │   ├── page.tsx         # Landing page
  │   ├── login/           # Login page
  │   ├── signup/          # Signup page
  │   ├── dashboard/       # Main dashboard
  │   ├── add-video/       # Add video page
  │   ├── preview/         # Preview reels
  │   ├── settings/        # User settings
  │   └── ...
  │
  ├── components/          # Reusable React components
  │   ├── ui/             # Shadcn UI components
  │   │   ├── button.tsx
  │   │   ├── card.tsx
  │   │   ├── input.tsx
  │   │   └── ...
  │   └── layout/         # Layout components
  │       ├── navbar.tsx
  │       ├── sidebar.tsx
  │       └── footer.tsx
  │
  ├── lib/                # Utility functions & config
  │   ├── api.ts          # API client
  │   ├── store.ts        # State management (Zustand)
  │   ├── theme.tsx       # Theme provider
  │   └── utils.ts        # Helper functions
  │
  ├── styles/             # CSS files
  │   └── globals.css     # Global styles
  │
  ├── types/              # TypeScript definitions
  │   └── index.ts        # Type definitions
  │
  ├── public/             # Static assets
  │
  ├── Configuration Files
  │   ├── next.config.ts  # Next.js config
  │   ├── tailwind.config.ts
  │   ├── tsconfig.json
  │   ├── package.json
  │   └── .env.example
  │
  └── Documentation
      ├── README.md           # Full documentation
      ├── DEPLOYMENT.md       # Deployment guide
      ├── ARCHITECTURE.md     # Architecture details
      └── QUICKSTART.sh       # This file

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎨 KEY FEATURES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  1. Modern UI Design
     • Glassmorphism + gradient effects
     • Premium color scheme (blue/purple)
     • Smooth animations & transitions
     • Responsive across all devices

  2. Authentication
     • Email/password login & signup
     • OAuth support (Google, GitHub)
     • JWT token management
     • Secure session handling

  3. Video Processing
     • YouTube URL validation
     • Customizable clip length (30-60s)
     • Multiple processing styles
     • Real-time progress tracking

  4. Reel Management
     • Preview reels before upload
     • Batch operations
     • Individual reel editing
     • Delete/download options

  5. Instagram Integration
     • OAuth connection
     • Direct reel upload
     • Account management
     • Connection status

  6. User Settings
     • Profile management
     • Theme preferences
     • Notification settings
     • Security options

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔌 PAGES & ROUTES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Public Pages:
    / ......................... Landing page
    /login ..................... Login
    /signup .................... Signup

  Protected Pages (requires authentication):
    /dashboard ................ Main dashboard
    /add-video ................ Add & process video
    /processing-status ....... Processing tracker
    /preview ................. Reel preview
    /connect-instagram ....... Instagram connection
    /settings ................ User settings
    /videos .................. Video library

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🧪 TESTING LOCALLY:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  1. Start Development Server
     $ npm run dev

  2. Open Browser
     http://localhost:3000

  3. Test Pages
     • Landing: Load and check styling
     • Auth: Signup (uses mock API)
     • Dashboard: View stats
     • Add Video: Test YouTube URL validation
     • Settings: Change theme

  4. Test Theme
     Click theme toggle in navbar to switch light/dark mode

  5. Check Responsive
     F12 → Toggle device toolbar → Test mobile view

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚨 TROUBLESHOOTING:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Issue: "Port 3000 already in use"
  Solution: npm run dev -- -p 3001

  Issue: "Module not found" errors
  Solution: 
    $ rm -rf node_modules
    $ npm cache clean --force
    $ npm install

  Issue: "Build fails"
  Solution:
    $ rm -rf .next
    $ npm run build

  Issue: "Styling looks broken"
  Solution:
    $ npm run dev
    (Wait for full compile)

  Issue: "npm install slow or fails"
  Solution:
    $ npm config set registry https://registry.npmjs.org/
    $ npm install

  Issue: "Cannot find .env.local"
  Solution:
    $ cp .env.example .env.local
    (Then update with your values)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📚 DOCUMENTATION LINKS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  README.md .............. Full documentation & features
  DEPLOYMENT.md ......... VPS, Docker, Vercel deployment
  ARCHITECTURE.md ....... Project structure & design
  .env.example .......... Environment variables template
  package.json .......... Dependencies list

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 USEFUL TIPS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  • Customize colors in tailwind.config.ts
  • Modify API endpoints in lib/api.ts
  • Update UI components in components/ui/
  • Add new pages in app/ directory
  • Use environment variables for sensitive data
  • Always use .env.local for local development
  • Don't commit .env.local to Git

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎓 NEXT STEPS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  1. ✅ Setup frontend (this project)
  2. 🔲 Create backend API server
  3. 🔲 Setup database (PostgreSQL/MongoDB)
  4. 🔲 Configure Instagram OAuth app
  5. 🔲 Implement video processing service
  6. 🔲 Setup file storage (AWS S3/Cloudinary)
  7. 🔲 Configure email service
  8. 🔲 Deploy to production

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎉 READY TO START?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Run these commands:
  
  $ git clone <repository-url>
  $ cd autoreels-ai
  $ npm install
  $ cp .env.example .env.local
  $ npm run dev
  
  Then open: http://localhost:3000

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📞 SUPPORT & RESOURCES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  • Next.js Docs: https://nextjs.org/docs
  • React Docs: https://react.dev
  • Tailwind CSS: https://tailwindcss.com/docs
  • Shadcn UI: https://ui.shadcn.com
  • TypeScript: https://www.typescriptlang.org/docs

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✨ Happy Coding! Build something amazing! ✨

EOF
