#!/bin/bash

# AutoReels AI - Setup Script
# This script automates the setup of the AutoReels AI frontend

set -e

echo "🚀 AutoReels AI - Setup Script"
echo "================================"
echo ""

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi

NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "❌ Node.js 18+ is required. Current version: $(node -v)"
    exit 1
fi

echo "✅ Node.js $(node -v) detected"
echo "✅ npm $(npm -v) detected"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
npm install

echo ""
echo "✅ Dependencies installed!"
echo ""

# Setup environment variables
if [ ! -f .env.local ]; then
    echo "🔧 Setting up environment variables..."
    cp .env.example .env.local
    echo "✅ .env.local created from .env.example"
    echo "⚠️  Please update .env.local with your configuration"
else
    echo "✅ .env.local already exists"
fi

echo ""
echo "================================"
echo "✅ Setup Complete!"
echo "================================"
echo ""
echo "Next steps:"
echo "1. Update .env.local with your API configuration"
echo "2. Run 'npm run dev' to start the development server"
echo "3. Open http://localhost:3000 in your browser"
echo ""
echo "Production build:"
echo "  npm run build"
echo "  npm run start"
echo ""
