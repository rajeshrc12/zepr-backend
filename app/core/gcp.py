import json
from functools import lru_cache
from google.cloud import storage
from google.oauth2.service_account import Credentials
from app.core.config import settings


@lru_cache()
def get_gcp_client():
    if not settings.GOOGLE_APPLICATION_CREDENTIALS_JSON:
        raise ValueError("Missing GOOGLE_APPLICATION_CREDENTIALS_JSON")

    info = json.loads(settings.GOOGLE_APPLICATION_CREDENTIALS_JSON)
    creds = Credentials.from_service_account_info(info)
    return storage.Client(credentials=creds, project=info["project_id"])
