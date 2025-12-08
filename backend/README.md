# AutoReels AI Backend

Complete, production-ready FastAPI backend for AutoReels AI - an automated Instagram Reel generator from YouTube videos.

## Tech Stack

- **FastAPI** - Modern, fast web framework for building APIs
- **Uvicorn** - ASGI server for running FastAPI
- **PostgreSQL** - Primary database for storing users, jobs, and reels
- **SQLAlchemy** - ORM for database operations
- **Pydantic** - Data validation and settings management
- **Redis** - Message broker for Celery task queue
- **Celery** - Distributed task queue for background processing
- **python-jose** - JWT token management
- **passlib** - Password hashing and verification

## Project Structure

```
backend/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
├── README.md               # This file
│
└── app/
    ├── __init__.py
    │
    ├── api/               # API routes and endpoints
    │   ├── __init__.py
    │   ├── health.py      # Health check endpoint
    │   ├── users.py       # User authentication routes
    │   ├── videos.py      # Video upload and processing routes
    │   ├── reels.py       # Reel management routes
    │   └── instagram.py   # Instagram integration routes
    │
    ├── core/              # Core configuration and settings
    │   ├── __init__.py
    │   └── config.py      # Application settings from environment
    │
    ├── db/                # Database setup and configuration
    │   ├── __init__.py
    │   ├── database.py    # SQLAlchemy engine and session setup
    │   └── base.py        # Base models and mixins
    │
    ├── models/            # SQLAlchemy ORM models
    │   ├── __init__.py
    │   ├── user.py        # User model
    │   ├── video_job.py   # Video processing job model
    │   └── reel.py        # Individual reel model
    │
    ├── schemas/           # Pydantic request/response schemas
    │   ├── __init__.py
    │   ├── user.py        # User schemas
    │   ├── video_job.py   # Video job schemas
    │   └── common.py      # Common response schemas
    │
    ├── services/          # Business logic layer (placeholders)
    │   ├── __init__.py
    │   ├── user_service.py        # User operations
    │   ├── video_service.py       # Video processing operations
    │   └── instagram_service.py   # Instagram integration operations
    │
    ├── workers/           # Celery background tasks (placeholders)
    │   ├── __init__.py
    │   └── celery_app.py  # Celery configuration and tasks
    │
    └── utils/             # Utility functions and helpers
        ├── __init__.py
        ├── helpers.py     # General utility functions
        └── security.py    # Security utilities (JWT, password hashing)
```

## Setup Instructions

### Prerequisites

- Python 3.9+
- PostgreSQL 12+
- Redis 6+
- pip (Python package manager)

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Setup Environment Variables

Copy the `.env.example` to `.env` and configure your settings:

```bash
cp .env.example .env
```

Edit `.env` with your actual configuration:

```env
# Database
DATABASE_URL=postgresql://username:password@localhost:5432/autoreels_db

# Redis
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API Keys (for future features)
GEMINI_API_KEY=your-gemini-api-key
YOUTUBE_API_KEY=your-youtube-api-key

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

### 3. Create PostgreSQL Database

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE autoreels_db;

# Create user (optional)
CREATE USER autoreels_user WITH PASSWORD 'password';
ALTER ROLE autoreels_user SET client_encoding TO 'utf8';
ALTER ROLE autoreels_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE autoreels_user SET default_transaction_deferrable TO on;
GRANT ALL PRIVILEGES ON DATABASE autoreels_db TO autoreels_user;

# Exit PostgreSQL
\q
```

### 4. Initialize Database Tables

Run migrations (when Alembic is set up):

```bash
# Initialize Alembic
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Initial migration"

# Apply migration
alembic upgrade head
```

For now, SQLAlchemy can create tables automatically. To do this, run:

```python
from app.db.database import engine
from app.db.base import Base
from app.models import user, video_job, reel

Base.metadata.create_all(bind=engine)
```

### 5. Start Redis Server

```bash
# Start Redis (if installed locally)
redis-server

# Or using Docker
docker run -d -p 6379:6379 redis:7
```

## Running the Server

### Development Mode

```bash
cd backend
python main.py
```

Or using Uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Health Check

Test the API is running:

```bash
curl http://localhost:8000/health
```

## Running Celery Workers

In a separate terminal, start the Celery worker:

```bash
# Install celery separately if needed
pip install celery[redis]

# Start worker
celery -A app.workers.celery_app worker --loglevel=info
```

## API Endpoints

### Health Check
- `GET /health` - Health check endpoint

### Users
- `POST /users/register` - Register new user
- `POST /users/login` - Login user
- `GET /users/me` - Get current user profile

### Videos
- `POST /videos/upload` - Upload YouTube video for processing
- `GET /videos/jobs` - List video processing jobs
- `GET /videos/jobs/{job_id}` - Get job details and status
- `POST /videos/jobs/{job_id}/cancel` - Cancel video processing

### Reels
- `GET /reels/job/{job_id}` - Get all reels from a job
- `GET /reels/{reel_id}` - Get individual reel details
- `POST /reels/{reel_id}/upload-instagram` - Upload single reel to Instagram
- `POST /reels/job/{job_id}/upload-all-instagram` - Upload all reels to Instagram

### Instagram
- `GET /instagram/auth-url` - Get Instagram OAuth URL
- `POST /instagram/callback` - Instagram OAuth callback
- `GET /instagram/disconnect` - Disconnect Instagram account

## Features Currently Implemented (Skeleton)

✅ Project structure and folder organization
✅ FastAPI application setup with CORS
✅ Database models (User, VideoJob, Reel)
✅ Pydantic schemas for validation
✅ API route definitions with placeholders
✅ Service layer structure
✅ Celery worker configuration
✅ Configuration management via environment variables
✅ Security utilities (password hashing, JWT helpers)
✅ Logging setup

## Features to be Implemented

⏳ User authentication and JWT token generation
⏳ Video validation and metadata extraction
⏳ Video processing and reel generation (FFmpeg integration)
⏳ Reel splitting algorithm (30-40 second chunks)
⏳ Video format conversion (to 1080x1920 vertical)
⏳ Gemini AI integration
⏳ Instagram API integration and uploads
⏳ Database migrations (Alembic)
⏳ Input validation and error handling
⏳ Rate limiting
⏳ User profile and brand settings
⏳ Email notifications

## Database Schema

### Users Table
- `id` - Primary key
- `email` - User email (unique)
- `username` - Username (unique)
- `full_name` - User's full name
- `hashed_password` - Hashed password
- `is_active` - Account status
- `is_superuser` - Admin flag
- `instagram_connected` - Instagram integration status
- `instagram_user_id` - Instagram user ID
- `created_at` - Timestamp
- `updated_at` - Timestamp

### VideoJobs Table
- `id` - Primary key
- `user_id` - Foreign key to users
- `youtube_url` - YouTube video URL
- `job_status` - Job status (pending, processing, completed, failed)
- `video_title` - Video title
- `video_duration` - Duration in seconds
- `num_reels` - Number of generated reels
- `progress_percentage` - Processing progress
- `celery_task_id` - Task ID for tracking
- `error_message` - Error message if failed
- `created_at` - Timestamp
- `updated_at` - Timestamp

### Reels Table
- `id` - Primary key
- `video_job_id` - Foreign key to video_jobs
- `reel_number` - Sequential reel number
- `start_time` - Start time in seconds
- `end_time` - End time in seconds
- `duration` - Duration in seconds
- `file_path` - Path to processed video file
- `thumbnail_path` - Path to thumbnail
- `is_uploaded` - Upload status
- `instagram_post_id` - Instagram post ID after upload
- `created_at` - Timestamp
- `updated_at` - Timestamp

## Environment Variables Reference

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_NAME` | Application name | AutoReels AI Backend |
| `APP_VERSION` | Application version | 1.0.0 |
| `DEBUG` | Debug mode | False |
| `ENVIRONMENT` | Environment (development/production) | development |
| `DATABASE_URL` | PostgreSQL connection URL | postgresql://... |
| `REDIS_URL` | Redis connection URL | redis://localhost:6379/0 |
| `SECRET_KEY` | JWT secret key | (must set) |
| `ALLOWED_ORIGINS` | CORS allowed origins | http://localhost:3000 |

## Troubleshooting

### Database Connection Error
- Ensure PostgreSQL is running
- Check `DATABASE_URL` in `.env`
- Verify database exists and user has permissions

### Redis Connection Error
- Ensure Redis is running on port 6379
- Check `REDIS_URL` in `.env`

### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>
```

### Import Errors
- Ensure you're in the `backend` directory
- Check Python version is 3.9+
- Verify all dependencies are installed: `pip install -r requirements.txt`

## Next Steps

1. **Implement user authentication** - Hash passwords, generate JWT tokens
2. **Add video processing** - Integrate FFmpeg for video splitting and format conversion
3. **Implement Instagram OAuth** - Connect to Instagram Graph API
4. **Add Celery tasks** - Create background jobs for video processing and uploads
5. **Database migrations** - Set up Alembic for database versioning
6. **Error handling** - Add comprehensive error handling and validation
7. **Testing** - Add unit and integration tests
8. **Deployment** - Docker, systemd service, or VPS setup

## Contributing

This is a skeleton project. All core features need to be implemented based on the TODO comments throughout the codebase.

## License

MIT

---

**Built with ❤️ for AutoReels AI**
