#!/bin/bash

# AutoReels AI - Quick Start Guide
# This script shows how to get the project running

cat << 'EOF'

╔═══════════════════════════════════════════════════════════════╗
║                    AutoReels AI - Quick Start                ║
║              Modern YouTube to Instagram Reels                ║
╚═══════════════════════════════════════════════════════════════╝

📋 PREREQUISITES:
   • Node.js 18+ (https://nodejs.org/)
   • npm or yarn
   • Git (for version control)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ STEP 1: Clone Repository
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   git clone <repository-url>
   cd autoreels-ai

✅ STEP 2: Install Dependencies
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   npm install

✅ STEP 3: Setup Environment Variables
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   cp .env.example .env.local

   Edit .env.local and update:
   - NEXT_PUBLIC_API_URL = Your backend API URL
   - NEXT_PUBLIC_INSTAGRAM_CLIENT_ID = Instagram App ID
   - NEXT_PUBLIC_INSTAGRAM_REDIRECT_URI = Your domain/connect-instagram

✅ STEP 4: Start Development Server
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   npm run dev

✅ STEP 5: Open in Browser
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   Open: http://localhost:3000

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔨 COMMON COMMANDS:

   Development:      npm run dev
   Build:            npm run build
   Production:       npm run start
   Linting:          npm run lint

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 PROJECT STRUCTURE:

   app/              → Pages (Next.js App Router)
   components/       → Reusable UI components
   ├── ui/          → Shadcn UI components
   └── layout/      → Layout components (Navbar, Sidebar, Footer)
   lib/              → Utilities, API client, state management
   styles/           → Global CSS and Tailwind styles
   public/           → Static assets

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📚 DOCUMENTATION:

   README.md          → Full setup and features
   DEPLOYMENT.md      → VPS, Docker, Vercel deployment
   ARCHITECTURE.md    → Project structure and design

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 PRODUCTION DEPLOYMENT:

   For VPS:          See DEPLOYMENT.md
   For Vercel:       npm i -g vercel && vercel --prod
   For Docker:       docker-compose up -d

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔗 IMPORTANT LINKS:

   - Project Structure:  ./ARCHITECTURE.md
   - Deployment Guide:   ./DEPLOYMENT.md
   - Environment Setup:  ./.env.example
   - Dependencies:       ./package.json

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 TIPS:

   • Customize theme colors in tailwind.config.ts
   • All UI components are in components/ui/
   • API endpoints configured in lib/api.ts
   • State management using Zustand (lib/store.ts)
   • Use .env.local for local development
   • Check README.md for detailed documentation

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🆘 TROUBLESHOOTING:

   Port already in use:  npm run dev -- -p 3001
   Module not found:     rm -rf node_modules && npm install
   Build fails:          rm -rf .next && npm run build
   Clear cache:          npm cache clean --force

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✨ You're all set! Happy coding! ✨

EOF
