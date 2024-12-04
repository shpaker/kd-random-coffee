import logging
import requests
from typing import Any, Dict

from ..settings import get_app_settings

settings = get_app_settings()
logger = logging.getLogger(__name__)

def get_data_from_external_api(endpoint: str) -> Dict[str, Any]:
    url = f"{settings.external_api_base_url}/{endpoint}"
    headers = {
        "Authorization": f"Bearer {settings.external_api_token}"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as errh:
        logger.error(f"Http Error: {errh}")
        raise
    except requests.exceptions.ConnectionError as errc:
        logger.error(f"Error Connecting: {errc}")
        raise
    except requests.exceptions.Timeout as errt:
        logger.error(f"Timeout Error: {errt}")
        raise
    except requests.exceptions.RequestException as err:
        logger.error(f"Something Else: {err}")
        raise