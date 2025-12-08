# Social Account Connect System - Setup Guide

## Overview

This guide walks you through setting up the Social Account Connection system for AutoReels AI, which allows users to connect their Instagram Business accounts via Facebook OAuth and automatically upload reels.

## Features Implemented

✅ Facebook OAuth 2.0 integration
✅ Long-lived access token generation
✅ Instagram Business Account linking
✅ Token refresh scheduling
✅ Frontend connection UI
✅ Settings page with status monitoring
✅ Background token refresh jobs
✅ Token expiry alerts
✅ Disconnect functionality

## Prerequisites

- Facebook Developer Account
- Facebook App with Instagram Graph API permissions
- Instagram Business Account linked to Facebook Page
- PostgreSQL database
- Redis instance

## Step 1: Facebook App Setup

### 1.1 Create Facebook App

1. Go to [Facebook Developers](https://developers.facebook.com)
2. Click "My Apps" → "Create App"
3. Choose "Consumer" type
4. Fill in app details:
   - App Name: "AutoReels AI"
   - App Contact Email: your-email@example.com
   - App Purpose: Business
5. Accept terms and create app

### 1.2 Add Instagram Graph API

1. In your app dashboard, click "Add Product"
2. Find "Instagram Graph API" and click "Set Up"
3. Click "Instagram Graph API" in the left menu
4. Go to "Settings" → "Basic"

### 1.3 Get App Credentials

In App Settings → Basic, copy:
- **App ID** → FACEBOOK_APP_ID
- **App Secret** → FACEBOOK_APP_SECRET

### 1.4 Configure OAuth Redirect URI

1. In Settings → Basic, scroll to "App Domains"
2. Add: `localhost:3002` (for development)
3. Add your production domain
4. In Instagram Graph API settings, add OAuth Redirect URIs:
   ```
   http://localhost:3002/settings/social-accounts/callback
   https://yourdomain.com/settings/social-accounts/callback
   ```

### 1.5 Set Up Permissions

In App Roles → Test Users:
1. Add yourself as a test user
2. Accept invitation

In Instagram Graph API → Permissions, request:
- `instagram_basic`
- `pages_show_list`
- `pages_manage_metadata`

## Step 2: Backend Configuration

### 2.1 Update .env File

```bash
# Facebook OAuth
FACEBOOK_APP_ID=your-app-id-here
FACEBOOK_APP_SECRET=your-app-secret-here
FACEBOOK_REDIRECT_URI=http://localhost:3002/settings/social-accounts/callback

# Database (ensure PostgreSQL is running)
DATABASE_URL=postgresql://user:password@localhost:5432/autoreels_db

# Redis (ensure Redis is running)
REDIS_URL=redis://localhost:6379/0

# CORS Origins (add your frontend domain)
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3002

# Frontend URL (for callback redirects)
FRONTEND_URL=http://localhost:3002
```

### 2.2 Apply Database Migrations

```bash
cd backend
alembic upgrade head  # If using alembic
# Or simply run the app - SQLAlchemy will create tables
```

The new `InstagramToken` table will be automatically created with columns:
- `fb_page_id`
- `fb_page_name`
- `ig_user_id`
- `instagram_username`
- `long_lived_token`
- `access_token`
- `expires_at`
- `token_expires_in`
- `last_refreshed_at`
- `refresh_count`
- `permissions`
- `is_connected`
- `is_valid`

## Step 3: Test the Flow

### 3.1 Test Facebook Login

1. Start backend:
```bash
cd backend
source venv/bin/activate
python main.py
```

2. Start frontend:
```bash
npm run dev
```

3. Navigate to: `http://localhost:3002/settings/social-accounts`

4. Click "Connect Instagram Account"

5. You should be redirected to Facebook login

6. After authorizing, you should see:
   - Instagram username
   - Facebook page name
   - Token expiry date
   - Connection status badge

### 3.2 Test Token Refresh

Click "Refresh Token" button to manually test token refresh.

### 3.3 Test Disconnect

Click "Disconnect Account" to test account removal.

## Step 4: Background Token Refresh Job

### 4.1 Set Up Scheduled Task

The system automatically schedules token refresh jobs. Tokens refresh automatically when:
- Less than 10 days remaining until expiry
- User manually clicks "Refresh Token"
- Auto-refresh job runs (every 3 days for tokens expiring within 3 days)

### 4.2 Start RQ Worker (for background jobs)

```bash
cd backend
source venv/bin/activate

# In a separate terminal
rq worker -u redis://localhost:6379/0
```

This worker will process:
- Token refresh jobs
- Video processing jobs
- AI generation jobs
- Reel uploads

### 4.3 Run Token Scheduler (Optional)

For advanced scheduling, run:

```bash
python -c "from app.services.token_scheduler import *; import asyncio; asyncio.run(schedule_token_refresh())"
```

Or add a cron job:

```bash
0 2 * * * cd /home/ubuntu/autoreels-ai && source backend/venv/bin/activate && python -c "from app.services.token_scheduler import *; import asyncio; asyncio.run(schedule_token_refresh())"
```

## Step 5: API Endpoints

All endpoints require authentication (Bearer token).

### Connect Flow

```bash
# 1. Get Facebook login URL
POST /social/facebook/login
Response: { login_url: "https://...", state: "..." }

# 2. User logs in and is redirected to:
GET /social/facebook/callback?code=...&state=...
Response: Redirects back to /settings/social-accounts

# 3. Check connection status
GET /social/status
Response: {
  is_connected: true,
  instagram_username: "username",
  facebook_page_name: "Page Name",
  token_expires_at: "2024-02-05T...",
  is_token_valid: true
}
```

### Token Management

```bash
# Refresh token
POST /social/refresh-token
Response: {
  success: true,
  message: "Token refreshed",
  new_expires_at: "2024-02-05T..."
}

# Disconnect account
DELETE /social/disconnect
Response: {
  success: true,
  message: "Successfully disconnected",
  disconnected: true
}
```

## Step 6: Frontend Integration

The frontend pages are already set up:

- `/settings/social-accounts` - Main connection page
- `/settings/social-accounts/callback` - OAuth callback handler

The UI includes:
- Connection status badge
- Token expiry display
- Refresh button
- Disconnect button
- Loading states
- Error handling

## Step 7: Production Deployment

### 7.1 Update Configuration

```bash
# .env
DEBUG=False
ENVIRONMENT=production
FACEBOOK_REDIRECT_URI=https://yourdomain.com/settings/social-accounts/callback
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
FRONTEND_URL=https://yourdomain.com
```

### 7.2 Update Facebook App Settings

1. Go to App Settings → Basic
2. Add your production domain to App Domains
3. In Instagram Graph API settings, add production callback URL
4. Change app mode from Development to Live (after testing)

### 7.3 Enable Webhooks (Optional)

For real-time token validation:

1. In Settings → Webhooks
2. Subscribe to Instagram topics
3. Implement webhook handler in backend

### 7.4 Start Services

```bash
# Backend
cd backend
source venv/bin/activate
python main.py &

# RQ Worker
rq worker -u redis://localhost:6379/0 &

# Frontend
npm run build
npm run start
```

## Troubleshooting

### Issue: "No Instagram business account found"

**Solution:** 
- Ensure your Facebook account has access to the Instagram Business Account
- Check that the Instagram account is linked to the Facebook Page
- Request `instagram_basic` permission

### Issue: "Token refresh failed"

**Solution:**
- Check if token has expired (> 60 days)
- Verify internet connection
- Check logs: `tail -f backend.log`

### Issue: "Login URL generation failed"

**Solution:**
- Verify `FACEBOOK_APP_ID` and `FACEBOOK_REDIRECT_URI` in .env
- Check that redirect URI is whitelisted in Facebook App settings
- Ensure app is not in development/testing mode restrictions

### Issue: "CORS error when connecting"

**Solution:**
- Add frontend domain to `ALLOWED_ORIGINS` in .env
- Restart backend after changing .env
- Check: `GET http://localhost:8000/health`

## Database Schema

### instagram_tokens Table

```sql
CREATE TABLE instagram_tokens (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL UNIQUE,
  
  -- Facebook
  fb_page_id VARCHAR(100),
  fb_page_name VARCHAR(200),
  fb_user_id VARCHAR(100),
  
  -- Instagram
  ig_user_id VARCHAR(100),
  instagram_username VARCHAR(100),
  ig_profile_picture VARCHAR(500),
  
  -- Tokens
  long_lived_token TEXT,
  access_token TEXT NOT NULL,
  token_type VARCHAR(50),
  
  -- Expiry
  expires_at TIMESTAMP,
  token_expires_in INTEGER,
  is_valid BOOLEAN DEFAULT true,
  
  -- Tracking
  last_refreshed_at TIMESTAMP,
  refresh_count INTEGER DEFAULT 0,
  
  -- Permissions
  permissions JSON,
  is_connected BOOLEAN DEFAULT false,
  
  -- Timestamps
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_instagram_tokens_user_id ON instagram_tokens(user_id);
CREATE INDEX idx_instagram_tokens_fb_page_id ON instagram_tokens(fb_page_id);
CREATE INDEX idx_instagram_tokens_ig_user_id ON instagram_tokens(ig_user_id);
```

## Next Steps

1. ✅ Backend routes implemented
2. ✅ Frontend UI created
3. ✅ Token refresh logic ready
4. ⏭️ Start services and test
5. ⏭️ Configure scheduled refresh job
6. ⏭️ Deploy to production
7. ⏭️ Monitor token expirations
8. ⏭️ Implement webhook for real-time updates (optional)

## Support

For issues:
1. Check logs: `tail -f /tmp/autoreels.log`
2. Verify .env configuration
3. Test endpoints with curl/Postman
4. Check Facebook App dashboard for errors

## Security Notes

- Never commit `.env` file with real credentials
- Use environment variables in production
- Rotate `SECRET_KEY` regularly
- Enable HTTPS in production
- Implement rate limiting on auth endpoints
- Log all token refresh attempts
- Validate all incoming requests
