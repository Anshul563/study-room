import boto3

from app.config import settings

s3 = boto3.client(
    service_name="s3",

    endpoint_url=f"https://{settings.R2_ACCOUNT_ID}.r2.cloudflarestorage.com",

    aws_access_key_id=settings.R2_ACCESS_KEY,

    aws_secret_access_key=settings.R2_SECRET_KEY
)

def upload_file_to_r2(
    file,
    filename: str
):

    s3.upload_fileobj(
        file,
        settings.R2_BUCKET_NAME,
        filename
    )

    return f"{settings.R2_PUBLIC_URL}/{filename}"