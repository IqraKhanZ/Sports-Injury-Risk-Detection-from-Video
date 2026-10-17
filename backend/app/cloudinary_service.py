import os
import cloudinary
import cloudinary.uploader
import cloudinary.api
from app.config import settings

# Cloudinary Configuration
CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME", getattr(settings, "CLOUDINARY_CLOUD_NAME", "dooj4emku"))
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY", getattr(settings, "CLOUDINARY_API_KEY", "793317176787249"))
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET", getattr(settings, "CLOUDINARY_API_SECRET", "h4V_jLLyFReYkiR8cFoU6MwaRZE"))

cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET,
    secure=True
)

def is_cloudinary_configured() -> bool:
    return bool(CLOUDINARY_CLOUD_NAME and CLOUDINARY_API_KEY and CLOUDINARY_API_SECRET)

def upload_video_file(file_path: str, public_id: str = None) -> str:
    """
    Uploads a processed video to Cloudinary and returns the secure HTTPS URL.
    Falls back to the local path if upload fails or Cloudinary is unavailable.
    """
    if not file_path or not os.path.exists(file_path):
        return file_path
    
    if not is_cloudinary_configured():
        return file_path

    try:
        print(f"[Cloudinary] Uploading video: {file_path}...")
        options = {
            "resource_type": "video",
            "folder": "sports_injury/videos",
            "overwrite": True
        }
        if public_id:
            options["public_id"] = public_id
            
        result = cloudinary.uploader.upload(file_path, **options)
        secure_url = result.get("secure_url")
        print(f"[Cloudinary] Video upload success: {secure_url}")
        return secure_url
    except Exception as e:
        print(f"[Cloudinary] Video upload error: {e}")
        return file_path

def upload_image_file(file_path: str, public_id: str = None) -> str:
    """
    Uploads a thumbnail image to Cloudinary and returns the secure HTTPS URL.
    Falls back to the local path if upload fails.
    """
    if not file_path or not os.path.exists(file_path):
        return file_path
    
    if not is_cloudinary_configured():
        return file_path

    try:
        options = {
            "resource_type": "image",
            "folder": "sports_injury/thumbnails",
            "overwrite": True
        }
        if public_id:
            options["public_id"] = public_id
            
        result = cloudinary.uploader.upload(file_path, **options)
        secure_url = result.get("secure_url")
        return secure_url
    except Exception as e:
        print(f"[Cloudinary] Image upload error: {e}")
        return file_path

def upload_pdf_file(file_path: str, public_id: str = None) -> str:
    """
    Uploads a PDF report to Cloudinary and returns the secure HTTPS URL.
    Falls back to the local path if upload fails.
    """
    if not file_path or not os.path.exists(file_path):
        return file_path
    
    if not is_cloudinary_configured():
        return file_path

    try:
        options = {
            "resource_type": "raw",
            "folder": "sports_injury/reports",
            "overwrite": True
        }
        if public_id:
            options["public_id"] = public_id
            
        result = cloudinary.uploader.upload(file_path, **options)
        secure_url = result.get("secure_url")
        return secure_url
    except Exception as e:
        print(f"[Cloudinary] PDF report upload error: {e}")
        return file_path
