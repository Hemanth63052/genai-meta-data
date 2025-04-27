from functools import lru_cache

from google.cloud import secretmanager

@lru_cache(maxsize=128, typed=True)
def get_gcp_secrets(secret_id, project_id):
    client = secretmanager.SecretManagerServiceClient()
    secret_name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": secret_name})
    secret_data = response.payload.data.decode("UTF-8")
    return secret_data
