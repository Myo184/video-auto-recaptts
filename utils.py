import os
import shutil
from datetime import datetime, timedelta
from config import UPLOAD_FOLDER, OUTPUT_FOLDER, TEMP_FOLDER

def cleanup_old_files(days=1):
    """Delete files older than specified days"""
    folders = [UPLOAD_FOLDER, OUTPUT_FOLDER, TEMP_FOLDER]
    cutoff = datetime.now() - timedelta(days=days)
    
    for folder in folders:
        if os.path.exists(folder):
            for filename in os.listdir(folder):
                filepath = os.path.join(folder, filename)
                if os.path.isfile(filepath):
                    mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
                    if mtime < cutoff:
                        os.remove(filepath)
                        print(f"🗑️ Deleted: {filepath}")

def get_file_size(filepath):
    """Get file size in MB"""
    return os.path.getsize(filepath) / (1024 * 1024)

def ensure_directories():
    """Ensure all required directories exist"""
    for folder in [UPLOAD_FOLDER, OUTPUT_FOLDER, TEMP_FOLDER]:
        os.makedirs(folder, exist_ok=True)
        print(f"📁 Created directory: {folder}")
