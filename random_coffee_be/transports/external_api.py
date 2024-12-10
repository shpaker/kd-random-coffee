import requests

from random_coffee_be_versia10.settings import get_app_settings

settings = get_app_settings()

def get_data_from_external_api(endpoint: str):
    url = f"{settings.external_api_base_url}/{endpoint}"
    headers = {
        "Authorization": f"Bearer {settings.external_api_token}"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()