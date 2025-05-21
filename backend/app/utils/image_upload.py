from google.cloud import storage
from PIL import Image
import io
from flask import current_app
import os
import requests
from datetime import datetime


def upload_profile_picture(image_file, user_id):
    """
    Upload a profile picture to GCP bucket after resizing it.

    Args:
        image_file: FileStorage object from Flask request
        user_id: User ID to use in the filename

    Returns:
        str: Public URL of the uploaded image
    """
    try:
        # Check file size (1MB = 1024 * 1024 bytes)
        if len(image_file.read()) > 1024 * 1024:
            return None, "File size must be less than 1MB"
        image_file.seek(0)  # Reset file pointer after reading

        # Get bucket name and credentials path from config
        bucket_name = current_app.config.get("GCP_BUCKET_NAME")
        if not bucket_name:
            return None, "GCP bucket name not configured"

        # Resize image to 312x312
        with Image.open(image_file) as img:
            resized = img.resize((312, 312))
            buffer = io.BytesIO()
            resized.save(buffer, format="JPEG")
            buffer.seek(0)

        # Upload to GCS
        client = storage.Client()
        bucket = client.bucket(bucket_name)

        # Create unique filename using user_id and timestamp
        filename = f"profile_pictures/{user_id}_{int(datetime.now().timestamp())}.jpg"
        blob = bucket.blob(filename)
        blob.upload_from_file(buffer, content_type="image/jpeg")

        return blob.public_url, None

    except Exception as e:
        return None, str(e)


def upload_profile_picture_from_url(image_url, user_id):
    """
    Downloads an image from a URL (e.g., Google profile picture) and uploads it to a GCP bucket.

    Args:
        image_url (str): The external image URL (from Google profile)
        user_id (str): Unique user ID to name the uploaded file

    Returns:
        (str, str | None): (public URL of uploaded image, error message or None)
    """
    try:
        # Download the image from the URL
        response = requests.get(image_url)
        if response.status_code != 200:
            return None, f"Failed to fetch image (status code: {response.status_code})"

        # Get GCP bucket name
        bucket_name = current_app.config.get("GCP_BUCKET_NAME")
        if not bucket_name:
            return None, "GCP bucket name not configured"

        # Upload to GCS
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        filename = f"profile_pictures/{user_id}_{int(datetime.now().timestamp())}.jpg"
        blob = bucket.blob(filename)
        blob.upload_from_file(
            io.BytesIO(response.content),
            content_type=response.headers.get("Content-Type", "image/jpeg"),
        )

        # Make the file publicly accessible

        return blob.public_url, None

    except Exception as e:
        return None, str(e)
