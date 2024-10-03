"""Client library for interacting with BR API."""

import logging

import httpx
from models import BackupRadarResponseModel


class BackupRadarAPI:
    """Base class for interacting with the BackupRadar API."""

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.backupradar.com",
    ) -> None:
        """Init BR class, set variables."""
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def get_backups(self, query_params: dict) -> BackupRadarResponseModel | None:
        """Get list of all backups."""
        url = f"{self.base_url}/backups"
        params = {k: v for k, v in query_params.items() if v is not None}

        try:
            response = httpx.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            return BackupRadarResponseModel(**data)
        except httpx.HTTPError:
            logging.exception("HTTP Error")
        except Exception:
            logging.exception("Other error occurred.")

        return None
