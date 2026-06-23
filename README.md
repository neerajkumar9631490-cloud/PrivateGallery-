Gallery · Secure Media Gallery

A full‑stack, password‑protected media gallery with drag‑and‑drop uploads, Cloudinary storage, and a responsive dark‑theme UI. Built with Flask (backend) and vanilla HTML/CSS/JavaScript (frontend).

https://via.placeholder.com/800x450?text=Gallery+Screenshot
Replace with actual screenshot

---

Table of Contents

· Features
· Tech Stack
· Project Structure
· Installation & Setup
  · Prerequisites
  · Configuration
  · Running the Application
· API Reference
· Usage
· Deployment
· License

---

Features

· Password‑protected access – single‑key entry to keep your gallery private.
· Upload media – drag‑and‑drop or click‑to‑select for images and videos.
· Cloudinary integration – media stored in the cloud with automatic optimisation.
· Lightbox viewer – browse full‑size images and videos with keyboard navigation.
· Long‑press delete – on mobile or desktop, long‑press a thumbnail to reveal a delete button.
· Responsive grid – switch between standard and compact views.
· Real‑time feedback – upload progress indicators and toast notifications.
· Persistent storage – local JSON database keeps track of your media metadata.

---

Tech Stack

Layer Technologies
Frontend HTML5, CSS3, Vanilla JavaScript (ES6)
Backend Python 3, Flask
Storage Cloudinary (CDN + media hosting)
Database JSON file (local)
Other Flask‑CORS, Fonts (Inter, JetBrains Mono)

---

Project Structure

```
.
├── gallery1.html          # Frontend (single‑page application)
├── app.py                 # Flask backend
├── media.json             # Local database (created automatically)
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

---

Installation & Setup

Prerequisites

· Python 3.8+ and pip
· A Cloudinary account (free tier works)
· (Optional) git for cloning

Configuration

1. Clone or download this repository.
2. Install Python dependencies:
   ```bash
   pip install flask flask-cors cloudinary
   ```
   (Or use requirements.txt if provided.)
3. Set up Cloudinary credentials in app.py:
   ```python
   cloudinary.config(
       cloud_name="your_cloud_name",
       api_key="your_api_key",
       api_secret="your_api_secret"
   )
   ```
4. Change the gallery password (optional):
   In app.py, update PASSWORD = "killme" to your own secret.
5. Place a logo image (optional):
      If you want to display a logo in the navbar, add an logo.png file in the project root and update the HTML to reference it (or keep the existing brand‑mark icon).

Running the Application

1. Start the Flask server:
   ```bash
   python app.py
   ```
   The server will run on http://0.0.0.0:5000 by default.
2. Open your browser and go to http://localhost:5000.
      You will be prompted for the password you set in step 4.

---

API Reference

All endpoints are prefixed with /api.

Method Endpoint Description
POST /verify-password Check if provided password matches
GET /api/images Retrieve all media items
POST /api/upload Upload a file (multipart/form‑data)
POST /api/delete Delete a media item (by public_id or URL)
GET /api/health Health check

Example response from /api/images:

```json
{
  "images": [
    {
      "url": "https://res.cloudinary.com/...",
      "public_id": "gallery/abc123",
      "resource_type": "image",
      "type": "image",
      "name": "photo.jpg",
      "duration": null,
      "format": "jpg"
    }
  ]
}
```

---

Usage

1. Password entry – enter the access key on the overlay to unlock the gallery.
2. Viewing – click any thumbnail to open the lightbox. Use arrow keys or on‑screen buttons to navigate.
3. Upload – click the Upload button (top‑right) or drag files onto the drop zone.
4. Delete – on a thumbnail, press and hold (or long‑click) for ~600ms until the delete button appears.
      Alternatively, delete from the lightbox using the trash icon.
5. Change view – toggle between Grid and Compact layouts using the segmented control above the gallery.

---

Deployment

For production use, consider:

· Using a production WSGI server like Gunicorn or uWSGI.
· Setting a strong, environment‑based password (do not hard‑code).
· Using environment variables for Cloudinary credentials.
· Replacing the JSON file with a proper database (SQLite/PostgreSQL) for concurrent access.
· Enabling HTTPS and adding proper CORS policies.

Example with Gunicorn:

```bash
gunicorn app:app --bind 0.0.0.0:8000
```

---

License

This project is open‑source and available under the MIT License.
Feel free to adapt it for your own use.

---

Acknowledgements

· Cloudinary for media hosting and transformation.
· Inter and JetBrains Mono fonts.
· Icons from Feather Icons.

---

Happy sharing! 📷🎬
