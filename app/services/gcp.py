from app.core.gcp import get_gcp_client
from app.core.config import settings
from datetime import timedelta

client = get_gcp_client()


def upload_csv(file, dest_name):
    """
    Uploads a CSV file to GCS.
    """

    bucket = client.bucket(settings.GOOGLE_BUCKET_NAME)
    blob = bucket.blob(dest_name)

    if hasattr(file, "file"):
        data = file.file.read()
    else:
        data = file

    blob.upload_from_string(
        data,
        content_type="text/csv"
    )

    return {"uploaded": dest_name}


def generate_signed_url(
    user_id: int,
    csv_id: int,
):
    """
    Generates a signed GET URL for a GCS object.
    """
    dest_name = f"{settings.GOOGLE_BUCKET_CSV_FOLDER_NAME}/{user_id}/{csv_id}.csv"
    bucket = client.bucket(settings.GOOGLE_BUCKET_NAME)
    blob = bucket.blob(dest_name)

    return blob.generate_signed_url(
        version="v4",
        expiration=timedelta(minutes=15),
        method="GET",
    )
