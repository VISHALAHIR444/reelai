# Instagram Account Management API Examples

## API Endpoints

### 1. Add Instagram Account
**POST** `/instagram/accounts`

```json
// Request
{
  "username": "tech_reels_official",
  "label": "Tech Content Account",
  "status": "active"
}

// Response 201
{
  "id": 1,
  "username": "tech_reels_official",
  "label": "Tech Content Account",
  "status": "active",
  "automation_enabled": false,
  "last_used_at": null,
  "created_at": "2026-01-04T12:00:00Z",
  "updated_at": "2026-01-04T12:00:00Z"
}

// Error 409 (Duplicate)
{
  "detail": "Instagram account with username 'tech_reels_official' already exists"
}
```

### 2. List All Instagram Accounts
**GET** `/instagram/accounts?status_filter=active`

```json
// Response 200
{
  "accounts": [
    {
      "id": 1,
      "username": "tech_reels_official",
      "label": "Tech Content Account",
      "status": "active",
      "automation_enabled": false,
      "last_used_at": "2026-01-04T14:30:00Z",
      "created_at": "2026-01-04T12:00:00Z",
      "updated_at": "2026-01-04T14:30:00Z"
    },
    {
      "id": 2,
      "username": "gaming_clips_daily",
      "label": "Gaming Highlights",
      "status": "active",
      "automation_enabled": false,
      "last_used_at": null,
      "created_at": "2026-01-04T13:00:00Z",
      "updated_at": "2026-01-04T13:00:00Z"
    }
  ],
  "total": 2,
  "active_count": 2,
  "inactive_count": 0
}
```

### 3. Get Account Details
**GET** `/instagram/accounts/{account_id}`

```json
// Response 200
{
  "id": 1,
  "username": "tech_reels_official",
  "label": "Tech Content Account",
  "status": "active",
  "automation_enabled": false,
  "last_used_at": "2026-01-04T14:30:00Z",
  "created_at": "2026-01-04T12:00:00Z",
  "updated_at": "2026-01-04T14:30:00Z"
}

// Error 404
{
  "detail": "Instagram account with id 999 not found"
}
```

### 4. Update Account
**PUT** `/instagram/accounts/{account_id}`

```json
// Request
{
  "label": "Tech & AI Reels",
  "status": "inactive"
}

// Response 200
{
  "id": 1,
  "username": "tech_reels_official",
  "label": "Tech & AI Reels",
  "status": "inactive",
  "automation_enabled": false,
  "last_used_at": "2026-01-04T14:30:00Z",
  "created_at": "2026-01-04T12:00:00Z",
  "updated_at": "2026-01-04T15:00:00Z"
}
```

### 5. Delete Account (Soft Delete)
**DELETE** `/instagram/accounts/{account_id}`

```json
// Response 204 No Content

// With hard delete query param
// DELETE /instagram/accounts/{account_id}?hard_delete=true
// Response 204 No Content
```

---

## Upload Queue API

### 1. Add Reel to Upload Queue
**POST** `/upload-queue`

```json
// Request
{
  "reel_id": "reel_abc123",
  "instagram_account_id": 1
}

// Response 201
{
  "id": 1,
  "reel_id": "reel_abc123",
  "instagram_account_id": 1,
  "upload_status": "pending",
  "upload_error": null,
  "uploaded_at": null,
  "instagram_post_id": null,
  "instagram_url": null,
  "created_at": "2026-01-04T15:00:00Z",
  "updated_at": "2026-01-04T15:00:00Z",
  "instagram_account": {
    "id": 1,
    "username": "tech_reels_official",
    "label": "Tech Content Account"
  },
  "reel": {
    "id": "reel_abc123",
    "title": "AI Revolution 2026",
    "duration": 35,
    "file_path": "/videos/reels/reel_abc123.mp4"
  }
}

// Error 400 (Inactive Account)
{
  "detail": "Cannot schedule reels to inactive Instagram account"
}

// Error 404 (Account Not Found)
{
  "detail": "Instagram account not found"
}

// Error 409 (Already in Queue)
{
  "detail": "Reel already in upload queue for this account"
}
```

### 2. List Upload Queue
**GET** `/upload-queue?status_filter=pending&instagram_account_id=1`

```json
// Response 200
[
  {
    "id": 1,
    "reel_id": "reel_abc123",
    "instagram_account_id": 1,
    "upload_status": "pending",
    "upload_error": null,
    "uploaded_at": null,
    "instagram_post_id": null,
    "instagram_url": null,
    "created_at": "2026-01-04T15:00:00Z",
    "updated_at": "2026-01-04T15:00:00Z",
    "instagram_account": {
      "id": 1,
      "username": "tech_reels_official",
      "label": "Tech Content Account"
    },
    "reel": {
      "id": "reel_abc123",
      "title": "AI Revolution 2026",
      "duration": 35,
      "file_path": "/videos/reels/reel_abc123.mp4"
    }
  },
  {
    "id": 2,
    "reel_id": "reel_def456",
    "instagram_account_id": 1,
    "upload_status": "pending",
    "upload_error": null,
    "uploaded_at": null,
    "instagram_post_id": null,
    "instagram_url": null,
    "created_at": "2026-01-04T15:05:00Z",
    "updated_at": "2026-01-04T15:05:00Z",
    "instagram_account": {
      "id": 1,
      "username": "tech_reels_official",
      "label": "Tech Content Account"
    },
    "reel": {
      "id": "reel_def456",
      "title": "Future of Technology",
      "duration": 32,
      "file_path": "/videos/reels/reel_def456.mp4"
    }
  }
]
```

### 3. Update Upload Status
**PUT** `/upload-queue/{queue_id}`

```json
// Request (Mark as uploaded)
{
  "upload_status": "uploaded",
  "instagram_post_id": "18012345678901234",
  "instagram_url": "https://www.instagram.com/reel/ABC123def456/"
}

// Response 200
{
  "id": 1,
  "reel_id": "reel_abc123",
  "instagram_account_id": 1,
  "upload_status": "uploaded",
  "upload_error": null,
  "uploaded_at": "2026-01-04T16:00:00Z",
  "instagram_post_id": "18012345678901234",
  "instagram_url": "https://www.instagram.com/reel/ABC123def456/",
  "created_at": "2026-01-04T15:00:00Z",
  "updated_at": "2026-01-04T16:00:00Z",
  "instagram_account": {
    "id": 1,
    "username": "tech_reels_official",
    "label": "Tech Content Account"
  },
  "reel": {
    "id": "reel_abc123",
    "title": "AI Revolution 2026",
    "duration": 35,
    "file_path": "/videos/reels/reel_abc123.mp4"
  }
}

// Request (Mark as failed)
{
  "upload_status": "failed",
  "upload_error": "Upload failed: Connection timeout"
}

// Response 200
{
  "id": 2,
  "reel_id": "reel_def456",
  "instagram_account_id": 1,
  "upload_status": "failed",
  "upload_error": "Upload failed: Connection timeout",
  "uploaded_at": null,
  "instagram_post_id": null,
  "instagram_url": null,
  "created_at": "2026-01-04T15:05:00Z",
  "updated_at": "2026-01-04T16:10:00Z",
  "instagram_account": {
    "id": 1,
    "username": "tech_reels_official",
    "label": "Tech Content Account"
  },
  "reel": {
    "id": "reel_def456",
    "title": "Future of Technology",
    "duration": 32,
    "file_path": "/videos/reels/reel_def456.mp4"
  }
}
```

### 4. Remove from Queue
**DELETE** `/upload-queue/{queue_id}`

```json
// Response 204 No Content
```

---

## Validation Rules

### Instagram Username
- Alphanumeric, dots, and underscores only
- Max 30 characters
- Case-insensitive (stored lowercase)
- Cannot be empty

### Account Status
- Must be "active" or "inactive"
- Cannot schedule uploads to inactive accounts

### Upload Status
- Must be "pending", "uploaded", or "failed"
- Automatically sets uploaded_at when status = "uploaded"
- Updates last_used_at on Instagram account when uploaded

### Uniqueness
- Username must be unique across non-deleted accounts
- Same reel cannot be in queue twice for same account

---

## Database Schema

### instagram_accounts
```sql
CREATE TABLE instagram_accounts (
    id INTEGER PRIMARY KEY,
    username VARCHAR UNIQUE NOT NULL,
    label VARCHAR NOT NULL,
    status VARCHAR DEFAULT 'active' NOT NULL,
    automation_enabled BOOLEAN DEFAULT false,
    last_used_at DATETIME,
    is_deleted BOOLEAN DEFAULT false,
    deleted_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_instagram_accounts_username ON instagram_accounts(username);
CREATE INDEX idx_instagram_accounts_status ON instagram_accounts(status);
CREATE INDEX idx_instagram_accounts_is_deleted ON instagram_accounts(is_deleted);
```

### upload_queue
```sql
CREATE TABLE upload_queue (
    id INTEGER PRIMARY KEY,
    reel_id VARCHAR NOT NULL,
    instagram_account_id INTEGER NOT NULL,
    upload_status VARCHAR DEFAULT 'pending' NOT NULL,
    upload_error TEXT,
    uploaded_at DATETIME,
    instagram_post_id VARCHAR,
    instagram_url VARCHAR,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (reel_id) REFERENCES reels(id),
    FOREIGN KEY (instagram_account_id) REFERENCES instagram_accounts(id)
);

CREATE INDEX idx_upload_queue_reel_id ON upload_queue(reel_id);
CREATE INDEX idx_upload_queue_instagram_account_id ON upload_queue(instagram_account_id);
CREATE INDEX idx_upload_queue_upload_status ON upload_queue(upload_status);
```

---

## Integration with Reel Scheduling

When creating reels or scheduling uploads:

1. User selects one or more Instagram accounts from active accounts
2. System validates account is active
3. Reel is added to upload_queue with status "pending"
4. Dashboard displays queue with:
   - Reel information (title, duration, thumbnail)
   - Selected Instagram account username
   - Upload status badge (pending/uploaded/failed)
5. Manual upload process:
   - User uploads reel manually to Instagram
   - User updates status via API to "uploaded" with post URL
   - System tracks last_used_at for the account
6. Failed uploads can be retried or removed from queue

---

## Future Automation Support

This design supports future automation without schema changes:

```json
// Future: Enable automation for account
PUT /instagram/accounts/{account_id}
{
  "automation_enabled": true
}

// Future: Auto-upload triggers
// When automation_enabled = true
// System can automatically process upload_queue items
// Using emulator-based automation or API-based uploads
```

The `automation_enabled` field is already in place but currently defaults to `false`.
Upload queue remains the same - automation just processes it automatically instead of manually.
