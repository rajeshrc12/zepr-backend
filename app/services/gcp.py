from app.core.gcp import get_gcp_client
from app.core.config import settings

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
