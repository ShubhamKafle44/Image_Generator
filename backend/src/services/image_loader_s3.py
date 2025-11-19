from fastapi import APIRouter, Header
from fastapi.responses import JSONResponse
import os
import boto3
from botocore.exceptions import ClientError

router = APIRouter()

s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)
BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

@router.get("/api/user/results")
async def get_user_results(user_id: str = Header(...)):
    """
    Fetch all S3 objects for a specific user and return presigned URLs.
    """
    prefix = f"users/{user_id}/"  # folder per user

    try:
        # List objects under the user's folder
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix)
        objects = response.get("Contents", [])

        results = []
        for obj in objects:
            key = obj["Key"]
            # Generate presigned URL valid for 1 hour
            url = s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": BUCKET_NAME, "Key": key},
                ExpiresIn=3600
            )
            # Optionally, parse the filename for ID or timestamp
            file_name = os.path.basename(key)
            results.append({
                "id": file_name.split(".")[0],
                "s3_url": url,
                "file_name": file_name
            })

        return JSONResponse(content=results)

    except ClientError as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
