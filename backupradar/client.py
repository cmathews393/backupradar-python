"""Client library for interacting with BR API."""

import logging

import httpx
from models import (
    BackupRadarBackupModel,
    BackupRadarQueryParams,
    BackupRadarResponseModel,
)


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

    def get_backups(
        self,
        query_params: BackupRadarQueryParams,
    ) -> BackupRadarResponseModel | None:
        """Get list of all backups."""
        url = f"{self.base_url}/backups"
        params = {k: v for k, v in query_params.model_fields if v is not None}

        try:
            response = httpx.get(url, headers=self.headers, params=params)
            response.raise_for_status()

            return BackupRadarResponseModel.model_validate_json(response.text)
        except httpx.HTTPError:
            logging.exception("HTTP Error")
        except Exception:
            logging.exception("Other error occurred.")

        return None

    def get_backup(self, query_params: dict) -> BackupRadarBackupModel | None:
        """Get details on a single backup."""
        return print("not implemented")
