import os
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent

# Environment detection
IS_RAILWAY = os.environ.get("RAILWAY_ENVIRONMENT", False) or os.environ.get("RAILWAY", False)
IS_PRODUCTION = os.environ.get("DEBUG", "False") == "False"

# Google Sheets
GOOGLE_SHEETS_CREDENTIALS = os.environ.get(
    "GOOGLE_SHEETS_CREDENTIALS", 
    "credentials.json"
)
SHEET_NAME = os.environ.get("SHEET_NAME", "VideoRecapUsers")

# Load credentials from environment variables (Railway)
if os.environ.get("GOOGLE_SHEETS_CREDENTIALS_JSON"):
    try:
        creds = json.loads(os.environ["GOOGLE_SHEETS_CREDENTIALS_JSON"])
        with open("credentials.json", "w") as f:
            json.dump(creds, f)
        print("✅ Google Sheets credentials loaded from env")
    except Exception as e:
        print(f"❌ Failed to load Google Sheets credentials: {e}")

if os.environ.get("GOOGLE_OAUTH_CREDENTIALS_JSON"):
    try:
        oauth = json.loads(os.environ["GOOGLE_OAUTH_CREDENTIALS_JSON"])
        with open("client_secret.json", "w") as f:
            json.dump(oauth, f)
        print("✅ Google OAuth credentials loaded from env")
    except Exception as e:
        print(f"❌ Failed to load Google OAuth credentials: {e}")

# Gemini
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-1.5-flash")

# Video Settings
MAX_VIDEO_SIZE_MB = int(os.environ.get("MAX_VIDEO_SIZE_MB", 500))
MAX_VIDEO_DURATION_MIN = int(os.environ.get("MAX_VIDEO_DURATION_MIN", 60))
OUTPUT_RESOLUTION = (1920, 1080)

# Free User
FREE_DAILY_LIMIT = int(os.environ.get("FREE_DAILY_LIMIT", 2))

# Subtitle Defaults
DEFAULT_SUBTITLE_COLOR = "#FFFFFF"
DEFAULT_SUBTITLE_SIZE = 40
DEFAULT_SUBTITLE_POSITION = "bottom"

# Logo Defaults
DEFAULT_LOGO_POSITION = "top-right"
DEFAULT_LOGO_OPACITY = 0.8
DEFAULT_LOGO_SIZE = (150, 150)

# Paths
UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER", "uploads")
OUTPUT_FOLDER = os.environ.get("OUTPUT_FOLDER", "outputs")
TEMP_FOLDER = os.environ.get("TEMP_FOLDER", "temp")

# Create folders
for folder in [UPLOAD_FOLDER, OUTPUT_FOLDER, TEMP_FOLDER]:
    os.makedirs(folder, exist_ok=True)

# Port
PORT = int(os.environ.get("PORT", 7860))

# Railway specific settings
if IS_RAILWAY:
    print("🚂 Running on Railway.app")
    print(f"📁 Upload folder: {UPLOAD_FOLDER}")
    print(f"📁 Output folder: {OUTPUT_FOLDER}")
    print(f"📁 Temp folder: {TEMP_FOLDER}")
    print(f"🔌 Port: {PORT}")
