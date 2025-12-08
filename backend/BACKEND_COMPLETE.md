# 🎬 GRAVIXAI Backend - Complete Documentation

## 🚀 Fully Production-Ready Backend System

This is a **complete, fully-functional, zero-placeholder backend** for GRAVIXAI - converting YouTube videos to Instagram Reels with:

- ✅ **NO LOGIN REQUIRED** - Direct Instagram connection for anyone
- ✅ **Facebook OAuth v19.0** - Real Instagram Graph API integration  
- ✅ **YouTube Download** - Full 4K video processing with transcripts
- ✅ **35-Second Chunks** - Sequential cutting (no random)
- ✅ **1080×1920 Vertical** - Letterbox format conversion
- ✅ **Gemini AI** - Auto metadata generation (title, captions, hashtags)
- ✅ **Direct Publishing** - Upload to Instagram instantly
- ✅ **Background Jobs** - RQ worker system for async processing
- ✅ **SQLAlchemy ORM** - SQLite/PostgreSQL database
- ✅ **100% Complete** - No TODOs, no incomplete parts

---

## 📋 Installation & Setup

### Step 1: Install System Dependencies

```bash
# FFmpeg (video processing)
sudo apt-get update
sudo apt-get install -y ffmpeg yt-dlp redis-server

# Or macOS:
brew install ffmpeg yt-dlp redis
```

### Step 2: Setup Python Environment

```bash
cd /home/ubuntu/autoreels-ai/backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install all dependencies
pip install -r requirements.txt
```

### Step 3: Configure Environment

```bash
# Copy example
cp .env.example .env

# Edit with your credentials
nano .env
```

**Add these credentials:**

```env
# Facebook Developer App (from https://developers.facebook.com)
FACEBOOK_APP_ID=your_app_id
FACEBOOK_APP_SECRET=your_app_secret
FACEBOOK_REDIRECT_URI=http://localhost:8000/api/social/facebook/callback

# Gemini API Key (from https://ai.google.dev)
GEMINI_API_KEY=your_gemini_api_key

# Database (SQLite by default)
DATABASE_URL=sqlite:///./gravixai.db

# Redis (for job queue)
REDIS_URL=redis://localhost:6379/0
```

### Step 4: Initialize Database

```bash
python3 << 'EOF'
from app.core.database import init_db
init_db()
print("✓ Database initialized successfully")
EOF
```

### Step 5: Start Services

**Terminal 1 - Start Redis:**
```bash
redis-server
```

**Terminal 2 - Start Backend API:**
```bash
cd /home/ubuntu/autoreels-ai/backend
source venv/bin/activate
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 3 - Start RQ Workers (optional):**
```bash
cd /home/ubuntu/autoreels-ai/backend
source venv/bin/activate
python -m app.workers.queue
```

### Verify Everything is Running

```bash
curl http://localhost:8000/health
# Response: {"status": "healthy", "service": "GRAVIXAI Backend", "version": "1.0.0"}
```

---

## 🔌 API Endpoints (Complete Reference)

### Health & Status Checks

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | API info and available endpoints |
| `/health` | GET | Health check |
| `/ready` | GET | Readiness check |

**Example:**
```bash
curl http://localhost:8000/health
```

---

### 📹 Video Processing (`/api/video`)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/video/youtube` | POST | Upload YouTube URL |
| `/api/video/` | GET | List all videos |
| `/api/video/{video_id}` | GET | Get video details with chunks/reels |
| `/api/video/{video_id}/status` | GET | Get processing status |
| `/api/video/{video_id}/process` | POST | Start processing pipeline |

**Upload YouTube Video:**
```bash
curl -X POST http://localhost:8000/api/video/youtube \
  -H "Content-Type: application/json" \
  -d '{
    "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
  }'

# Response:
# {
#   "id": "a1b2c3d4",
#   "youtube_video_id": "dQw4w9WgXcQ",
#   "title": "Processing...",
#   "status": "pending",
#   "created_at": "2025-01-01T00:00:00",
#   ...
# }
```

**Get Video Status:**
```bash
curl http://localhost:8000/api/video/a1b2c3d4/status

# Response:
# {
#   "video_id": "a1b2c3d4",
#   "status": "processing",
#   "title": "Video Title",
#   "duration": 3600,
#   "reels_created": 3,
#   "created_at": "2025-01-01T00:00:00",
#   "updated_at": "2025-01-01T00:05:00"
# }
```

**Start Processing:**
```bash
curl -X POST http://localhost:8000/api/video/a1b2c3d4/process

# Processing steps (automatic):
# 1. Download YouTube video + audio
# 2. Extract transcript (auto-captions or fallback)
# 3. Cut into 35-second chunks
# 4. Convert each chunk to 1080x1920 vertical format
# 5. Generate AI metadata with Gemini
# 6. Create Reel records
```

---

### 🎞️ Reels Management (`/api/reels`)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/reels/` | GET | List all reels |
| `/api/reels/{video_id}` | GET | Get reels for specific video |
| `/api/reels/{reel_id}/details` | GET | Get individual reel details |
| `/api/reels/{reel_id}/publish` | POST | Publish reel to Instagram |
| `/api/reels/pending-publish/count` | GET | Count unpublished reels |

**Get All Reels from Video:**
```bash
curl "http://localhost:8000/api/reels/a1b2c3d4?skip=0&limit=50"

# Response:
# [
#   {
#     "id": "reel_001",
#     "chunk_index": 0,
#     "title": "Check This Out!",
#     "caption": "Amazing content...",
#     "hashtags": "#viral #shorts #trending",
#     "topics": "Entertainment,Creative,Trending",
#     "quality_score": 87.5,
#     "publish_status": "pending",
#     "ig_media_id": null,
#     "created_at": "2025-01-01T00:05:00"
#   },
#   ...
# ]
```

**Publish Reel to Instagram:**
```bash
curl -X POST http://localhost:8000/api/reels/reel_001/publish

# Response:
# {
#   "reel_id": "reel_001",
#   "status": "publishing",
#   "message": "Reel publish job queued"
# }

# After publishing:
# {
#   "reel_id": "123456789",
#   "media_id": "media_123456789",
#   "status": "published",
#   "success": true
# }
```

---

### 🔐 Social/Instagram Connection (`/api/social`)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/social/connect` | GET | Get Facebook OAuth URL |
| `/api/social/facebook/callback` | GET | OAuth callback (auto-handled) |
| `/api/social/status` | GET | Check connection status |
| `/api/social/refresh-token` | POST | Refresh access token |
| `/api/social/disconnect` | DELETE | Disconnect account |

**Get OAuth URL:**
```bash
curl http://localhost:8000/api/social/connect

# Response:
# {
#   "authorization_url": "https://www.facebook.com/v19.0/dialog/oauth?client_id=...",
#   "state": "random-uuid"
# }

# User visits this URL, approves access
# Facebook redirects to: /api/social/facebook/callback?code=...
# Instagram account is automatically saved to database
```

**Check Connection Status:**
```bash
curl http://localhost:8000/api/social/status

# If connected:
# {
#   "connected": true,
#   "ig_user_id": "17841405410392105",
#   "fb_page_name": "My Business Page",
#   "token_expires_at": "2025-03-01T00:00:00"
# }

# If not connected:
# {
#   "connected": false,
#   "ig_user_id": null,
#   "fb_page_name": null,
#   "token_expires_at": null
# }
```

**Refresh Token:**
```bash
curl -X POST http://localhost:8000/api/social/refresh-token

# Response:
# {
#   "success": true,
#   "message": "Token refreshed",
#   "expires_at": "2025-03-01T12:00:00"
# }
```

**Disconnect:**
```bash
curl -X DELETE http://localhost:8000/api/social/disconnect

# Response:
# {
#   "success": true,
#   "message": "Instagram account disconnected"
# }
```

---

## 🗄️ Database Schema

### InstagramSettings
Stores Facebook OAuth tokens and Instagram account info

```python
{
  "id": 1,
  "fb_page_id": "123456789",
  "fb_page_name": "My Business Page",
  "fb_user_id": "987654321",
  "ig_user_id": "17841405410392105",
  "long_lived_access_token": "IGQVJf...",
  "token_expires_at": "2025-03-01T00:00:00",
  "is_active": true,
  "created_at": "2025-01-01T00:00:00",
  "updated_at": "2025-01-01T00:00:00"
}
```

### Video
YouTube video record with processing status

```python
{
  "id": "a1b2c3d4",
  "youtube_url": "https://youtu.be/dQw4w9WgXcQ",
  "youtube_video_id": "dQw4w9WgXcQ",
  "title": "Video Title",
  "description": "Video description",
  "thumbnail_url": "https://...",
  "duration": 3600,  # seconds
  "download_path": "/videos/a1b2c3d4/video.mp4",
  "transcript": "This is the video transcript...",
  "status": "completed",  # pending, processing, completed, failed
  "error_message": null,
  "instagram_account_id": 1,
  "created_at": "2025-01-01T00:00:00",
  "updated_at": "2025-01-01T00:10:00"
}
```

### VideoChunk
35-second segments cut from original video

```python
{
  "id": "chunk_001",
  "video_id": "a1b2c3d4",
  "chunk_index": 0,
  "start_time": 0,      # seconds
  "end_time": 35,
  "duration": 35,
  "file_path": "/videos/a1b2c3d4/chunks/chunk_000.mp4",
  "created_at": "2025-01-01T00:05:00"
}
```

### Reel
Processed 1080×1920 Instagram Reel

```python
{
  "id": "reel_001",
  "video_id": "a1b2c3d4",
  "chunk_id": "chunk_001",
  "chunk_index": 0,
  "title": "Check This Out!",
  "caption": "Amazing content that will change your life!",
  "hashtags": "#viral #shorts #trending #entertainment",
  "topics": "Entertainment,Creative,Trending",
  "quality_score": 87.5,
  "file_path": "/videos/a1b2c3d4/reels/reel_0.mp4",
  "duration": 35,
  "ig_media_id": "123456789",
  "publish_status": "published",  # pending, uploaded, published, failed
  "publish_error": null,
  "created_at": "2025-01-01T00:05:00",
  "updated_at": "2025-01-01T00:06:00"
}
```

### Job
Background job tracking

```python
{
  "id": "job_abc123",
  "job_type": "yt_download",  # or: video_cutting, vertical_convert, ai_generate, publish
  "video_id": "a1b2c3d4",
  "status": "completed",  # queued, processing, completed, failed
  "progress": 100.0,
  "started_at": "2025-01-01T00:00:30",
  "completed_at": "2025-01-01T00:05:00",
  "error_message": null,
  "created_at": "2025-01-01T00:00:00",
  "updated_at": "2025-01-01T00:05:00"
}
```

### ProcessingLog
Detailed processing information

```python
{
  "id": 1,
  "video_id": "a1b2c3d4",
  "level": "INFO",  # INFO, WARNING, ERROR
  "message": "Starting YouTube download...",
  "created_at": "2025-01-01T00:00:01"
}
```

---

## 🔄 Complete Processing Workflow

### User Flow

```
1. User opens website
   ↓
2. Clicks "Connect Instagram"
   ↓
3. System redirects to Facebook OAuth
   ↓
4. User logs in and approves
   ↓
5. Facebook redirects to callback
   ↓
6. Backend saves Instagram account to DB
   ↓
7. User pasts YouTube URL
   ↓
8. System queues download + processing
   ↓
9. Background jobs process video:
   - Download video (FFmpeg)
   - Extract transcript (yt-dlp)
   - Cut into 35s chunks (FFmpeg)
   - Convert to 1080×1920 (FFmpeg)
   - Generate metadata (Gemini AI)
   ↓
10. User sees list of reels
   ↓
11. User clicks "Publish"
   ↓
12. Reel is uploaded to Instagram via Graph API
   ↓
13. Done! Reel is live on Instagram
```

---

## 📁 File Structure

```
backend/
├── main.py                          # FastAPI application
├── requirements.txt                 # All Python dependencies
├── .env.example                     # Environment variables template
├── README.md                        # This file
│
└── app/
    ├── __init__.py
    │
    ├── api/                         # API Routes
    │   ├── __init__.py
    │   ├── health.py                # /health, /ready
    │   ├── video.py                 # /api/video/* endpoints
    │   ├── reels.py                 # /api/reels/* endpoints
    │   └── social.py                # /api/social/* endpoints
    │
    ├── models/                      # Database Models (SQLAlchemy ORM)
    │   └── __init__.py
    │       - InstagramSettings
    │       - Video
    │       - VideoChunk
    │       - Reel
    │       - Job
    │       - ProcessingLog
    │
    ├── schemas/                     # Request/Response Schemas (Pydantic)
    │   └── __init__.py
    │       - VideoCreate
    │       - VideoResponse
    │       - ReelResponse
    │       - SocialStatusResponse
    │       - And more...
    │
    ├── services/                    # Business Logic
    │   ├── youtube_downloader.py    # YouTube download + transcript
    │   ├── video_processor.py       # FFmpeg video cutting
    │   ├── reel_converter.py        # 1080×1920 conversion
    │   ├── gemini_client.py         # Gemini AI integration
    │   ├── instagram_oauth_service.py # Facebook OAuth v19
    │   └── instagram_publisher.py   # Instagram Graph API publishing
    │
    ├── workers/                     # Background Jobs
    │   └── queue.py                 # RQ worker setup
    │
    ├── core/                        # Configuration
    │   ├── config.py                # Settings from environment
    │   └── database.py              # SQLAlchemy setup
    │
    └── utils/                       # Utilities
        └── (logging, helpers, etc.)

videos/                             # Storage directory
├── <video_id>/
│   ├── video.mp4                   # Original YouTube download
│   ├── audio.m4a                   # Audio for STT
│   ├── video.info.json             # Metadata
│   ├── chunks/
│   │   ├── chunk_000.mp4
│   │   ├── chunk_001.mp4
│   │   └── ...
│   └── reels/
│       ├── reel_0.mp4              # 1080×1920
│       ├── reel_1.mp4
│       └── ...
```

---

## 🛠️ Configuration Reference

All settings in `.env`:

```bash
# API
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# Database (default: SQLite)
DATABASE_URL=sqlite:///./gravixai.db
# For PostgreSQL: postgresql://user:password@localhost/gravixai

# Facebook OAuth v19 (Required)
FACEBOOK_APP_ID=
FACEBOOK_APP_SECRET=
FACEBOOK_REDIRECT_URI=http://localhost:8000/api/social/facebook/callback

# Gemini AI (Required)
GEMINI_API_KEY=
GEMINI_MODEL=gemini-1.5-pro

# Redis (for job queue)
REDIS_URL=redis://localhost:6379/0

# Video Processing
VIDEOS_DIR=./videos
CHUNK_DURATION=35
REEL_WIDTH=1080
REEL_HEIGHT=1920

# Tools
YT_DLP_PATH=yt-dlp
FFMPEG_PATH=ffmpeg

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://10.0.0.11:3000

# Logging
LOG_LEVEL=INFO
```

---

## 🚨 Troubleshooting

| Problem | Solution |
|---------|----------|
| `yt-dlp not found` | `pip install yt-dlp` or `apt-get install yt-dlp` |
| `ffmpeg not found` | `apt-get install ffmpeg` or `brew install ffmpeg` |
| `Redis connection refused` | `redis-server &` or install Redis |
| `Database locked` | Delete `gravixai.db` and reinitialize |
| `Facebook OAuth fails` | Verify App ID, Secret, and redirect URI match exactly |
| `Gemini API errors` | Check API key is valid and has quota |
| `Port 8000 already in use` | Kill existing process: `lsof -ti:8000 \| xargs kill -9` |

---

## 📚 Documentation Links

- **FastAPI**: https://fastapi.tiangolo.com/
- **SQLAlchemy**: https://docs.sqlalchemy.org/
- **Facebook Graph API v19**: https://developers.facebook.com/docs/instagram-api
- **Gemini API**: https://ai.google.dev/
- **yt-dlp**: https://github.com/yt-dlp/yt-dlp
- **FFmpeg**: https://ffmpeg.org/

---

## ✅ What's Included (100% Complete)

- ✅ All database models fully defined
- ✅ All API endpoints fully implemented
- ✅ Facebook OAuth v19.0 complete integration
- ✅ YouTube download with transcript extraction
- ✅ FFmpeg-based video cutting (35 seconds sequential)
- ✅ Vertical conversion (1080×1920 with letterbox)
- ✅ Gemini AI metadata generation
- ✅ Instagram Graph API publishing
- ✅ RQ background job queue
- ✅ SQLAlchemy ORM with relationships
- ✅ Pydantic request/response validation
- ✅ CORS configuration
- ✅ Error handling and logging
- ✅ Health check endpoints
- ✅ Environment configuration
- ✅ Complete documentation

## ❌ What's NOT Included (and why)

- ❌ User authentication/login - **NOT NEEDED**: Direct Instagram connection for all users
- ❌ Email verification - **NOT NEEDED**: No user registration required
- ❌ Payment/billing - **NOT NEEDED**: Could be added later as extension
- ❌ Analytics dashboard - **NOT NEEDED**: Basic status endpoints sufficient
- ❌ Admin panel - **NOT NEEDED**: Can be added via separate admin app

---

## 🎯 Quick Start (5 Minutes)

```bash
# 1. Setup
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

# 2. Add credentials to .env
nano .env
# - FACEBOOK_APP_ID
# - FACEBOOK_APP_SECRET
# - GEMINI_API_KEY

# 3. Initialize database
python -c "from app.core.database import init_db; init_db()"

# 4. Start Redis
redis-server &

# 5. Start API
python -m uvicorn main:app --host 0.0.0.0 --port 8000

# 6. Test
curl http://localhost:8000/health
# {"status": "healthy", "service": "GRAVIXAI Backend", "version": "1.0.0"}

# Done! Open http://localhost:3000 in browser
```

---

**GRAVIXAI © 2025** - All Rights Reserved
