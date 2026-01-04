# 🚀 Quick Start Guide - Run GRAVIXAI Locally

This guide will help you get both the **frontend** and **backend** servers running on your local machine.

## ⚠️ Important Note

The servers need to run on **YOUR local computer**, not on GitHub. Follow these steps to get everything working.

---

## 📋 Prerequisites

Before starting, make sure you have these installed:

1. **Node.js 18+** - Download from [nodejs.org](https://nodejs.org/)
2. **Python 3.9+** - Download from [python.org](https://www.python.org/)
3. **pip** - Comes with Python
4. **Git** - Download from [git-scm.com](https://git-scm.com/)

Verify installations by running:
```bash
node --version
npm --version
python --version
pip --version
```

---

## 🔧 Setup Instructions

### Step 1: Clone the Repository

Open your terminal/command prompt and run:

```bash
git clone https://github.com/VISHALAHIR444/reelai.git
cd reelai
```

### Step 2: Setup Frontend (Next.js)

```bash
# Install frontend dependencies
npm install

# Create environment file
cp .env.example .env.local

# The .env.local file will have the default values which work for local development
```

### Step 3: Setup Backend (FastAPI)

```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env

# Go back to root directory
cd ..
```

---

## ▶️ Running the Application

You need to run **TWO servers** at the same time - one for frontend, one for backend.

### Option 1: Using Two Terminal Windows (Recommended)

**Terminal 1 - Backend Server:**
```bash
cd backend
python main.py
```

You should see:
```
INFO:     Application startup complete.
✓ Database initialized
✓ All systems ready
```

**Terminal 2 - Frontend Server:**
```bash
# From the root directory
npm run dev
```

You should see:
```
✓ Ready in 1472ms
- Local:        http://localhost:3000
```

### Option 2: Using Screen/Tmux (Linux/Mac)

```bash
# Start backend in background
cd backend
python main.py &

# Start frontend
cd ..
npm run dev
```

### Option 3: Using PM2 (Advanced)

```bash
# Install PM2 globally
npm install -g pm2

# Start backend
cd backend
pm2 start main.py --name "backend" --interpreter python

# Start frontend
cd ..
pm2 start npm --name "frontend" -- run dev

# View logs
pm2 logs
```

---

## 🌐 Access the Website

Once both servers are running, open your web browser and go to:

**http://localhost:3000**

You should see the GRAVIXAI website with the monochrome design!

---

## 🔍 Verify Servers Are Running

### Check Frontend (Port 3000)
Open browser to: http://localhost:3000

### Check Backend (Port 8000)
Open browser to: http://localhost:8000

You should see:
```json
{
  "service": "GRAVIXAI Backend",
  "version": "1.0.0",
  "status": "running"
}
```

---

## 🛑 Stopping the Servers

### If you used Terminal windows:
Press `Ctrl+C` in each terminal window

### If you used PM2:
```bash
pm2 stop all
pm2 delete all
```

### If you used background process:
```bash
# Find process IDs
ps aux | grep python
ps aux | grep node

# Kill processes
kill <PID>
```

---

## ❌ Troubleshooting

### Error: "Port 3000 already in use"
```bash
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:3000 | xargs kill -9
```

### Error: "Port 8000 already in use"
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:8000 | xargs kill -9
```

### Error: "Module not found"
```bash
# Frontend
rm -rf node_modules
npm install

# Backend
pip install -r backend/requirements.txt
```

### Error: "Cannot connect to backend"
Make sure the backend server is running on port 8000 before starting the frontend.

### Error: "Database error"
The backend uses SQLite by default, which requires no setup. The database file will be created automatically at `backend/gravixai.db`

---

## 📁 Project Structure

```
reelai/
├── frontend files (Next.js)      → Port 3000
├── backend/                       → Port 8000
│   ├── main.py                   ← Start backend server
│   ├── requirements.txt          ← Backend dependencies
│   └── .env                      ← Backend config
├── package.json                  ← Frontend dependencies
└── .env.local                    ← Frontend config
```

---

## 🎯 What You Should See

When everything is working correctly:

1. **Terminal 1 (Backend):** Shows FastAPI logs
2. **Terminal 2 (Frontend):** Shows Next.js compilation
3. **Browser (http://localhost:3000):** Shows GRAVIXAI website
4. **Browser (http://localhost:8000):** Shows backend API response

---

## 💡 Need Help?

If you're still having issues:

1. Make sure **both servers are running**
2. Check that **no other programs** are using ports 3000 or 8000
3. Verify **all dependencies are installed** correctly
4. Check the **terminal output** for error messages

---

## ✅ Success!

When you see the GRAVIXAI website at http://localhost:3000, you're all set! 🎉

The website features:
- ✨ Monochrome design
- 📹 YouTube to Instagram Reels conversion
- 🎨 Modern UI with processing dashboard
- 📱 Responsive layout

---

**Built with ❤️ by GRAVIXAI Team**
