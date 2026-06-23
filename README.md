markdown
<p align="center">
  <img src="https://res.cloudinary.com/dfzrb3fac/image/upload/v1782188114/file_000000001cfc71fabf84b73eaa639faf_cpygth.png" alt="Gallery Logo" width="120" />
</p>

<h1 align="center">Gallery · Secure Media Vault</h1>

<p align="center">
  <b>A sleek, password-protected media gallery with Cloudinary integration.</b><br/>
  Upload, organize, and preview images & videos in a beautifully crafted dark-mode interface.
</p>

<p align="center">
  <a href="#features">Features</a> ·
  <a href="#tech-stack">Tech Stack</a> ·
  <a href="#getting-started">Getting Started</a> ·
  <a href="#configuration">Configuration</a> ·
  <a href="#api-reference">API</a> ·
  <a href="#license">License</a>
</p>

---

## Features

| Feature | Description |
|---------|-------------|
| **Secure Access** | Password-protected entry with server-side verification |
| **Dual Media Support** | Upload and preview both images (JPG, PNG, GIF, WebP) and videos (MP4, WebM, MOV) |
| **Cloudinary Integration** | Automatic cloud storage, transformation-ready URLs, and CDN delivery |
| **Drag & Drop Upload** | Intuitive file queue with real-time progress and validation |
| **Immersive Lightbox** | Full-screen media viewer with keyboard navigation (← → Esc) |
| **Long-Press Delete** | Touch-friendly deletion with haptic feedback and confirmation modal |
| **Responsive Grid** | Toggle between Grid and Compact layouts; optimized for all screen sizes |
| **Dark-First Design** | Polished dark UI with glassmorphism, subtle animations, and premium typography |
| **Local Persistence** | Lightweight JSON database for fast metadata retrieval |

---

## Tech Stack

**Backend**
- Python 3.9+
- Flask — lightweight WSGI web framework
- Cloudinary Python SDK — media upload, storage, and deletion
- Flask-CORS — cross-origin resource sharing

**Frontend**
- Vanilla JavaScript (ES6+) — zero build step
- Custom CSS3 — CSS variables, grid, flexbox, backdrop-filter
- Google Fonts (Inter + JetBrains Mono)

**Infrastructure**
- Cloudinary — cloud media management & CDN
- JSON file-based database (`media.json`)

---

## Getting Started

### Prerequisites

- Python 3.9 or higher
- A [Cloudinary](https://cloudinary.com) account (free tier available)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/gallery-vault.git
cd gallery-vault

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install flask flask-cors cloudinary

# 4. Configure your credentials (see Configuration below)
# Edit app.py and replace the placeholder Cloudinary credentials

# 5. Run the application
python app.py
```

The server will start on `http://localhost:5000`.

---

## Configuration

All critical settings are centralized at the top of `app.py`:

```python
# Security
PASSWORD = "password"           # <-- Change this to your secure access key

# Cloudinary Credentials
cloudinary.config(
    cloud_name="your_cloud_name",   # <-- Your Cloudinary cloud name
    api_key="your_api_key",         # <-- Your API key
    api_secret="your_api_secret"    # <-- Your API secret
)
```

### Upload Limits

| Media Type | Max Size | Supported Formats |
|------------|----------|-------------------|
| Images     | 20 MB    | JPEG, PNG, WebP, GIF |
| Videos     | 100 MB   | MP4, WebM, MOV, OGG |

---

## Project Structure

```
gallery-vault/
├── app.py              # Flask backend — API routes, Cloudinary logic, DB helpers
├── index.html          # Single-page frontend — UI, interactions, upload queue
├── media.json          # Auto-generated local database (created on first run)
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

---

## API Reference

### Authentication

| Method | Endpoint | Body | Response |
|--------|----------|------|----------|
| `POST` | `/verify-password` | `{ "password": "..." }` | `{ "success": true/false }` |

### Media Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/api/images` | Retrieve all media items |
| `POST` | `/api/upload` | Upload a file (multipart/form-data) |
| `POST` | `/api/delete` | Delete a media item by `public_id` or `url` |
| `GET`  | `/api/health` | Health check |

### Upload Response

```json
{
  "success": true,
  "url": "https://res.cloudinary.com/.../image/upload/...",
  "type": "image",
  "public_id": "gallery/abc123"
}
```

---

## User Interface

### Password Gate
A frosted-glass overlay secures the gallery. Enter your access key to unlock.

### Gallery Grid
- **Grid View** — Spacious tiles with hover lift and scale effects
- **Compact View** — Dense layout for quick browsing
- **Shimmer Loading** — Skeleton placeholders while fetching

### Media Lightbox
- Keyboard shortcuts: `←` previous, `→` next, `Esc` close
- Video autoplay with native controls
- One-click deletion with confirmation

### Upload Queue
- Drag & drop or click to select files
- Per-file validation (type, size)
- Real-time progress indicators
- Batch upload with individual status tracking

---

## Security Notes

- **Password** is stored in plain text in `app.py` for simplicity. For production, migrate to environment variables or a hashed credential store.
- **CORS** is enabled globally (`CORS(app)`). Restrict origins in production.
- **File validation** occurs on both client and server sides.
- **Cloudinary `invalidate=True`** ensures deleted assets are purged from CDN caches.

---

## Roadmap

- [ ] Environment variable configuration (`.env` support)
- [ ] User accounts & multi-gallery support
- [ ] Album / folder organization
- [ ] Search & filter by media type
- [ ] Infinite scroll pagination
- [ ] PWA support for offline viewing

---

## License

MIT License — feel free to use, modify, and distribute.

---

<p align="center">
  <sub>Crafted with precision. Built for creators.</sub>
</p>
```
