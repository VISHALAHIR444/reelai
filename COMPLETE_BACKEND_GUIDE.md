# AutoReels AI Backend - Complete Implementation Guide

## 🎯 Project Overview

Complete production-ready FastAPI backend for AutoReels AI with:
- ✅ YouTube video download & processing
- ✅ Sequential 35-second chunk cutting
- ✅ 1080x1920 vertical reel generation
- ✅ AI metadata generation (Gemini API)
- ✅ Instagram Graph API integration
- ✅ Background job processing (RQ + Redis)
- ✅ PostgreSQL database
- ✅ JWT authentication
- ✅ Docker support

## 📋 System Requirements

- Python 3.11+
- PostgreSQL 12+
- Redis 6+
- FFmpeg
- 500GB+ storage for videos

## 🚀 Quick Start (on Linux VPS 210.79.129.253)

### 1. Clone & Setup

```bash
cd /home/ubuntu/autoreels-ai/backend
chmod +x complete_setup.sh
./complete_setup.sh
```

### 2. Configure Environment

Edit `.env` with your API keys:

```bash
nano .env
```

Required keys:
- `GEMINI_API_KEY` - Get from Google AI Studio
- `INSTAGRAM_BUSINESS_ACCOUNT_ID` - Get from Instagram Developers
- `YOUTUBE_API_KEY` - Get from Google Cloud Console
- `GOOGLE_APPLICATION_CREDENTIALS` - JSON key file for Speech-to-Text

### 3. Start Services

```bash
# Terminal 1 - Start backend
source venv/bin/activate
python main.py

# Terminal 2 - Start RQ worker
source venv/bin/activate
rq worker -u redis://localhost:6379/0
```

### 4. Access API

- **API Docs**: http://210.79.129.253:8000/docs
- **API Base**: http://210.79.129.253:8000
- **Health Check**: http://210.79.129.253:8000/health

## 📁 Project Structure

```
backend/
├── main.py                 # Main FastAPI application
├── requirements.txt        # Python dependencies
├── .env.example           # Environment template
├── complete_setup.sh      # Setup script
│
├── app/
│   ├── __init__.py
│   ├── core/
│   │   └── config.py      # Configuration settings
│   ├── db/
│   │   ├── base.py        # SQLAlchemy base + mixins
│   │   └── database.py    # Database session
│   ├── models/
│   │   ├── user.py        # User model
│   │   ├── video.py       # Video & VideoChunk models
│   │   └── reel.py        # Reel, InstagramToken, Job, Log models
│   ├── schemas/
│   │   ├── user.py        # User schemas
│   │   └── video.py       # Video schemas
│   ├── api/
│   │   ├── auth.py        # Auth endpoints (optional, all in main.py now)
│   │   ├── health.py      # Health check
│   │   ├── users.py       # User endpoints (optional)
│   │   ├── videos.py      # Video endpoints (optional)
│   │   ├── reels.py       # Reel endpoints (optional)
│   │   └── instagram.py   # Instagram endpoints (optional)
│   ├── services/
│   │   ├── user_service.py        # User CRUD + auth
│   │   ├── youtube_service.py     # YouTube download
│   │   ├── video_service.py       # FFmpeg processing
│   │   ├── gemini_service.py      # AI metadata
│   │   └── instagram_service.py   # Instagram upload
│   ├── workers/
│   │   ├── celery_app.py     # Celery config (legacy)
│   │   └── rq_worker.py      # RQ background jobs
│   └── utils/
│       ├── helpers.py        # Utility functions
│       └── security.py       # JWT + password hashing
│
└── tests/                  # Unit tests (to be added)
```

## 🔌 API Endpoints

### Authentication

```
POST   /auth/signup      # Register user
POST   /auth/login       # Login and get JWT
POST   /auth/refresh     # Refresh access token
```

### Videos

```
POST   /video/youtube         # Upload YouTube video
GET    /video/status/{id}     # Get processing status
GET    /jobs/{job_id}         # Get job status
```

### Reels

```
GET    /reels/{video_id}      # Get all reels for video
POST   /reels/{id}/upload-instagram  # Upload reel to Instagram
```

### Instagram

```
GET    /instagram/connect-url     # Get OAuth URL
POST   /instagram/callback        # Handle OAuth callback
POST   /instagram/disconnect      # Disconnect account
```

## 🔑 Environment Variables

```
# Core
APP_NAME=AutoReels AI Backend
DEBUG=False
ENVIRONMENT=production
SECRET_KEY=your-64-char-random-key

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/autoreels_db

# Redis
REDIS_URL=redis://localhost:6379/0

# Storage
STORAGE_BASE_PATH=/videos          # Where to store videos
CHUNK_DURATION=35                   # 35 second chunks

# FFmpeg
FFMPEG_PATH=/usr/bin/ffmpeg
FFPROBE_PATH=/usr/bin/ffprobe

# APIs
GEMINI_API_KEY=your-gemini-key
YOUTUBE_API_KEY=your-youtube-key
INSTAGRAM_BUSINESS_ACCOUNT_ID=your-ig-app-id
GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json
```

## 📊 Database Schema

### Users
```sql
users:
  - id (PK)
  - email (unique)
  - username (unique)
  - hashed_password
  - is_active
  - is_superuser
  - instagram_connected
  - instagram_user_id
```

### Videos
```sql
videos:
  - id (PK)
  - user_id (FK users)
  - youtube_url
  - youtube_video_id (unique)
  - status (uploaded, downloading, processing, completed, failed)
  - duration
  - title, description
  - transcript
  - video_file_path
  - audio_file_path
```

### Video Chunks
```sql
video_chunks:
  - id (PK)
  - video_id (FK videos)
  - chunk_number (sequential)
  - start_time (seconds)
  - end_time (seconds)
  - file_path (to MP4 chunk)
```

### Reels
```sql
reels:
  - id (PK)
  - video_id (FK videos)
  - chunk_id (FK video_chunks)
  - reel_number (sequential)
  - file_path (to 1080x1920 vertical video)
  - title (AI generated)
  - caption (AI generated)
  - hashtags (JSON array)
  - topics (JSON array)
  - quality_score (0.0-1.0)
  - instagram_post_id (unique)
  - instagram_url
  - is_uploaded (boolean)
```

### Jobs
```sql
jobs:
  - id (PK)
  - user_id (FK users)
  - video_id (FK videos)
  - job_type (youtube_download, cutting, vertical_conversion, ai_generation, instagram_upload)
  - status (pending, processing, completed, failed)
  - progress (0-100)
  - result (JSON)
  - error_message
  - retry_count
  - rq_job_id
```

## 🎬 Processing Pipeline

### Flow:
1. **User uploads YouTube URL** → POST /video/youtube
2. **Backend enqueues download job** → RQ worker processes
3. **Downloads video & audio** → Stored in /videos/{video_id}/
4. **Extracts transcript** → YouTube or Google Speech-to-Text
5. **Cuts into 35s chunks** → /videos/{video_id}/chunks/
6. **Converts to 1080x1920** → /videos/{video_id}/reels/
7. **Generates AI metadata** → Title, caption, hashtags, quality score
8. **User uploads to Instagram** → Uses Graph API with access token

### Job Status Tracking:
- Check `/video/status/{video_id}` for overall progress
- Check `/jobs/{job_id}` for individual job status
- Each job shows progress 0-100%

## 🔐 Security

- **Passwords**: Hashed with bcrypt (passlib)
- **JWT**: HS256 algorithm, 30-min access token, 7-day refresh token
- **Instagram**: OAuth 2.0, long-lived access tokens stored in DB
- **Database**: Parameterized queries, no SQL injection
- **CORS**: Configured for frontend

## 📝 Usage Example

### 1. Sign Up

```bash
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "johndoe",
    "full_name": "John Doe",
    "password": "secure123"
  }'
```

### 2. Login

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "secure123"
  }'
```

Response:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

### 3. Upload YouTube Video

```bash
curl -X POST http://localhost:8000/video/youtube \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
  }'
```

Response:
```json
{
  "video_id": 1,
  "youtube_video_id": "dQw4w9WgXcQ",
  "job_id": "123",
  "status": "processing"
}
```

### 4. Check Processing Status

```bash
curl -X GET http://localhost:8000/video/status/1 \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

### 5. Get Generated Reels

```bash
curl -X GET http://localhost:8000/reels/1 \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

### 6. Upload Reel to Instagram

```bash
curl -X POST http://localhost:8000/reels/1/upload-instagram \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

## 🛠️ Troubleshooting

### FFmpeg not found

```bash
sudo apt install ffmpeg
# Update .env:
FFMPEG_PATH=/usr/bin/ffmpeg
FFPROBE_PATH=/usr/bin/ffprobe
```

### YouTube download fails

- Check YouTube URL is valid
- Ensure yt-dlp is installed: `pip install yt-dlp`
- Check storage path has write permissions

### Gemini API errors

- Verify API key in .env
- Ensure API is enabled in Google Cloud Console
- Check quota limits

### Instagram upload fails

- Verify access token is valid
- Check Instagram Business Account is set up
- Ensure video format matches requirements

### Background jobs not processing

```bash
# Check Redis
redis-cli ping

# Check RQ worker
rq worker -u redis://localhost:6379/0

# Monitor jobs
rq info -u redis://localhost:6379/0
```

## 📦 Deployment

### Docker

```bash
# Build image
docker build -t autoreels-ai .

# Run container
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql://... \
  -e REDIS_URL=redis://... \
  -e GEMINI_API_KEY=... \
  autoreels-ai
```

### systemd Service

Create `/etc/systemd/system/autoreels-backend.service`:

```ini
[Unit]
Description=AutoReels AI Backend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/home/ubuntu/autoreels-ai/backend
Environment="PATH=/home/ubuntu/autoreels-ai/backend/venv/bin"
ExecStart=/home/ubuntu/autoreels-ai/backend/venv/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Start:
```bash
sudo systemctl enable autoreels-backend
sudo systemctl start autoreels-backend
```

## 📚 Testing

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest tests/
```

## 🤝 Contributing

All endpoints and services are fully implemented. To extend:

1. Add new endpoint in `main.py`
2. Create service class in `app/services/`
3. Update database models if needed
4. Add tests in `tests/`

## 📄 License

All rights reserved

## 🚀 Ready to Deploy!

Your backend is production-ready. Just:

1. Add your API keys to `.env`
2. Run `./complete_setup.sh`
3. Start `python main.py` and `rq worker`
4. Connect your Next.js frontend

**Backend fully implemented and ready for production deployment!** 🎉
