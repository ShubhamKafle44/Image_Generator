import boto3
import re
from botocore.client import Config
from botocore.exceptions import ClientError
from urllib.parse import quote_plus
import os
from datetime import datetime, timezone
import uuid
from src.models.result import Result

BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
REGION = os.getenv("AWS_REGION")

s3 = boto3.client(
    "s3",
    region_name=REGION,
    config=Config(signature_version="s3v4"),
)

def sanitize_filename(name: str):
    # Remove slashes or directory structures
    name = name.replace("/", "").replace("\\", "")
    # Remove extensions (png, jpg, jpeg, webp)
    name = re.sub(r"\.(png|jpg|jpeg|webp)$", "", name, flags=re.IGNORECASE)
    return name

def upload_image(data: bytes, user_id: str, transaction_id: str, filename: str):
    """
    Upload single image inside:
    images/{user_id}/{transaction_id}/{filename}.png
    """
    filename = sanitize_filename(filename)

    key = f"images/{user_id}/{transaction_id}/{filename}.png"

    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=key,
        Body=data,
        ContentType="image/png",
        Metadata={"timestamp": datetime.now(timezone.utc).isoformat()}
    )

    url = f"https://{BUCKET_NAME}.s3.{REGION}.amazonaws.com/{quote_plus(key)}"
    return key, url


def get_presigned_url(key: str, expires_in=3600):
    return s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": BUCKET_NAME, "Key": key},
        ExpiresIn=expires_in,
    )


def fetch_s3_results(user_id: str):
    """
    Fetch all transactions for a user and return grouped results like:
    [
        {
            "transaction_id": "...",
            "originalUrl": "...",
            "generatedUrl": "...",
            "timestamp": "..."
        }
    ]
    """

    prefix = f"images/{user_id}/"
    response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix)

    if "Contents" not in response:
        return []

    grouped = {}

    for obj in response["Contents"]:
        key = obj["Key"]

        parts = key.split("/")
        # [images, user_id, transaction_id, filename.png]
        if len(parts) != 4:
            continue

        _, user, transaction_id, filename = parts

        if transaction_id not in grouped:
            grouped[transaction_id] = {
                "transaction_id": transaction_id,
                "originalUrl": None,
                "generatedUrl": None,
                "timestamp": ""
            }

        presigned = get_presigned_url(key)

        # Check if this file is original or generated
        if "original" in filename:
            grouped[transaction_id]["originalUrl"] = presigned
        elif "generated" in filename:
            grouped[transaction_id]["generatedUrl"] = presigned
        
        # Pull timestamp from metadata
        meta = s3.head_object(Bucket=BUCKET_NAME, Key=key)
        ts = meta.get("Metadata", {}).get("timestamp", "")
        if ts:
            grouped[transaction_id]["timestamp"] = ts

    # Convert dict → list and sort
    results = list(grouped.values())
    results.sort(key=lambda x: x["timestamp"], reverse=True)

    return results


def delete_user_results(user_id: str, db):
    # Get all results for this user
    results = db.query(Result).filter(Result.user_id == user_id).all()

    for r in results:
        # Delete original
        if r.original_s3_key:
            try:
                s3.delete_object(Bucket=BUCKET_NAME, Key=r.original_s3_key)
            except ClientError as e:
                print(f"Error deleting original: {e}")

        # Delete generated
        if r.generated_s3_key:
            try:
                s3.delete_object(Bucket=BUCKET_NAME, Key=r.generated_s3_key)
            except ClientError as e:
                print(f"Error deleting generated: {e}")

        # Remove DB entry
        db.delete(r)

    db.commit()