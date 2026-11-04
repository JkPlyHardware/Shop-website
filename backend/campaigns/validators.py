from pathlib import Path
from PIL import Image, UnidentifiedImageError
from django.conf import settings
from django.core.exceptions import ValidationError

def validate_campaign_image(upload):
    allowed = {".jpg", ".jpeg", ".png", ".webp"}
    suffix = Path(upload.name).suffix.lower()
    if suffix not in allowed:
        raise ValidationError("Upload a JPG, PNG or WebP image.")
    if upload.size > settings.MAX_UPLOAD_MB * 1024 * 1024:
        raise ValidationError(f"Image must be {settings.MAX_UPLOAD_MB} MB or smaller.")
    try:
        upload.seek(0)
        with Image.open(upload) as image:
            if image.format not in {"JPEG", "PNG", "WEBP"}:
                raise ValidationError("Unsupported image format.")
            image.verify()
        upload.seek(0)
    except (UnidentifiedImageError, OSError, ValueError):
        raise ValidationError("The uploaded file is not a valid image.")
