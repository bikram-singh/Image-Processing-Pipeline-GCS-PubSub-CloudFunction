import base64
import json
import os
from io import BytesIO
from google.cloud import storage
from PIL import Image

THUMB_BUCKET = os.environ.get("THUMB_BUCKET", "my-thumbnail-bucket")

def process_gcs_notification(event, context):
    """
    Pub/Sub-triggered Cloud Function.
    Expects Cloud Storage notification payload (JSON API v1) base64-encoded in event['data'].
    """
    if "data" not in event:
        print("No data in Pub/Sub message; nothing to do.")
        return

    payload = json.loads(base64.b64decode(event["data"]).decode("utf-8"))
    bucket_name = payload.get("bucket")
    object_name = payload.get("name")

    if not bucket_name or not object_name:
        print("Missing bucket or object name in payload:", payload)
        return

    print(f"Processing gs://{bucket_name}/{object_name}")

    storage_client = storage.Client()
    src_bucket = storage_client.bucket(bucket_name)
    blob = src_bucket.blob(object_name)

    # Read image bytes
    image_bytes = blob.download_as_bytes()
    img = Image.open(BytesIO(image_bytes))

    # Create thumbnail
    img.thumbnail((320, 320))
    out_buf = BytesIO()
    img.save(out_buf, format="JPEG")
    out_buf.seek(0)

    # Write to thumb bucket (name keeps path, prefixed with 'thumbs/')
    thumb_bucket = storage_client.bucket(THUMB_BUCKET)
    thumb_name = f"thumbs/{object_name.rsplit('/',1)[-1]}"
    thumb_blob = thumb_bucket.blob(thumb_name)
    thumb_blob.upload_from_file(out_buf, content_type="image/jpeg")

    print(f"Uploaded thumbnail to gs://{THUMB_BUCKET}/{thumb_name}")