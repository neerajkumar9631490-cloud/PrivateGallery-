from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import cloudinary
import cloudinary.uploader
import os
import json
import re

app = Flask(__name__)
CORS(app)

# =========================
# CONFIG
# =========================
PASSWORD = "password" # <----- Here you set your password

cloudinary.config(
    cloud_name="********",  # <---- name of cloud (eg  wofneo43d)
    api_key="623838393394", # <----- api key
    api_secret="lKemmakrnfnaalwk8vMLY" # <---- Set api secret 
)

DB_FILE = "media.json"

MAX_IMAGE_SIZE = 20 * 1024 * 1024     # 20 MB
MAX_VIDEO_SIZE = 100 * 1024 * 1024    # 100 MB

ALLOWED_IMAGE_TYPES = {
    "image/jpeg", "image/png", "image/webp", "image/gif"
}
ALLOWED_VIDEO_TYPES = {
    "video/mp4", "video/webm", "video/quicktime", "video/ogg"
}

# =========================
# INIT DB
# =========================
if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        json.dump([], f)


# =========================
# HELPERS
# =========================
def detect_resource_type(url_or_mime):
    if url_or_mime.startswith("video/"):
        return "video"
    if url_or_mime.startswith("image/"):
        return "image"

    url = url_or_mime.lower().split("?")[0].split("#")[0]
    ext = url.rsplit(".", 1)[-1] if "." in url else ""
    if ext in {"mp4", "webm", "mov", "m4v", "ogg", "ogv", "avi", "mkv"}:
        return "video"
    return "image"


def public_id_from_url(url):
    """Extract public_id from a Cloudinary URL (best-effort fallback)."""
    try:
        url = url.split("?")[0].split("#")[0]
        parts = url.split("/upload/")
        if len(parts) < 2:
            return None
        after = parts[1]
        # Strip version segment like v1234567890/
        after = re.sub(r"^v\d+(?:/|$)", "", after)
        # Strip extension
        public_id = re.sub(r"\.[^.]+$", "", after)
        return public_id or None
    except Exception:
        return None


def load_db():
    """Load DB and migrate any old string-only entries to dicts."""
    try:
        with open(DB_FILE, "r") as f:
            raw = json.load(f)
        if not isinstance(raw, list):
            return []

        migrated = []
        for item in raw:
            if isinstance(item, str):
                rtype = detect_resource_type(item)
                migrated.append({
                    "url": item,
                    "public_id": public_id_from_url(item),
                    "resource_type": rtype,
                    "type": rtype,
                    "name": item.rsplit("/", 1)[-1],
                })
            elif isinstance(item, dict):
                # Ensure required keys exist
                url = item.get("url", "")
                rtype = item.get("resource_type") or item.get("type") or detect_resource_type(url)
                migrated.append({
                    "url": url,
                    "public_id": item.get("public_id") or public_id_from_url(url),
                    "resource_type": rtype,
                    "type": rtype,
                    "name": item.get("name") or url.rsplit("/", 1)[-1],
                    "duration": item.get("duration"),
                    "format": item.get("format"),
                })
        return migrated
    except Exception as e:
        print(f"load_db error: {e}")
        return []


def save_db(items):
    with open(DB_FILE, "w") as f:
        json.dump(items, f, indent=2)


# =========================
# ROUTES
# =========================
@app.route("/")
def home():
    if os.path.exists("index.html"):
        return send_from_directory(".", "index.html")
    return "index.html not found", 404


@app.route("/verify-password", methods=["POST"])
def verify_password():
    data = request.get_json(silent=True) or {}
    if data.get("password") == PASSWORD:
        return jsonify({"success": True})
    return jsonify({"success": False})


@app.route("/api/images", methods=["GET"])
def get_images():
    items = load_db()
    return jsonify({"images": items})


@app.route("/api/upload", methods=["POST"])
def upload_media():
    if "file" not in request.files:
        return jsonify({"success": False, "error": "No file provided"}), 400

    file = request.files["file"]
    if not file or not file.filename:
        return jsonify({"success": False, "error": "Empty file"}), 400

    # Validate type
    mimetype = (file.mimetype or "").lower()
    is_video = mimetype.startswith("video/") or detect_resource_type(file.filename) == "video"
    is_image = mimetype.startswith("image/") or detect_resource_type(file.filename) == "image"

    if is_video:
        if mimetype and mimetype not in ALLOWED_VIDEO_TYPES:
            return jsonify({"success": False, "error": f"Unsupported video type: {mimetype}"}), 400
    elif is_image:
        if mimetype and mimetype not in ALLOWED_IMAGE_TYPES:
            return jsonify({"success": False, "error": f"Unsupported image type: {mimetype}"}), 400
    else:
        return jsonify({"success": False, "error": "File must be an image or video"}), 400

    # Validate size
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)
    max_size = MAX_VIDEO_SIZE if is_video else MAX_IMAGE_SIZE
    if size > max_size:
        mb_limit = max_size // (1024 * 1024)
        return jsonify({
            "success": False,
            "error": f"File exceeds {mb_limit}MB limit"
        }), 400

    try:
        # Cloudinary auto-detects resource type from the file
        result = cloudinary.uploader.upload(
            file,
            resource_type="auto",
            folder="gallery"
        )

        resource_type = result.get("resource_type", "image")

        item = {
            "url": result["secure_url"],
            "public_id": result["public_id"],
            "resource_type": resource_type,
            "type": resource_type,
            "name": file.filename,
            "format": result.get("format"),
        }

        if resource_type == "video":
            duration = result.get("duration")
            if duration is not None:
                item["duration"] = float(duration)

        items = load_db()
        items.insert(0, item)
        save_db(items)

        return jsonify({
            "success": True,
            "url": item["url"],
            "type": item["type"],
            "public_id": item["public_id"],
        })

    except Exception as e:
        print(f"Upload error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/delete", methods=["POST"])
def delete_media():
    data = request.get_json(silent=True) or {}
    public_id = data.get("public_id")
    url = data.get("url")
    resource_type = data.get("type") or data.get("resource_type")

    if not public_id and not url:
        return jsonify({"success": False, "error": "No identifier provided"}), 400

    items = load_db()
    target = None

    for item in items:
        if public_id and item.get("public_id") == public_id:
            target = item
            break
        if url and item.get("url") == url:
            target = item
            break

    if not target:
        return jsonify({"success": False, "error": "Item not found"}), 404

    # Delete from Cloudinary if we have a public_id
    cloudinary_error = None
    pid = target.get("public_id")
    rtype = target.get("resource_type", "image")

    if pid:
        try:
            cloudinary.uploader.destroy(
                pid,
                resource_type=rtype,
                invalidate=True
            )
        except Exception as e:
            cloudinary_error = str(e)
            print(f"Cloudinary destroy error: {e}")

    # Remove from local DB regardless
    items = [
        i for i in items
        if not (
            (public_id and i.get("public_id") == public_id) or
            (url and i.get("url") == url)
        )
    ]
    save_db(items)

    return jsonify({
        "success": True,
        "deleted_url": target.get("url"),
        "cloudinary_warning": cloudinary_error,
    })


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
