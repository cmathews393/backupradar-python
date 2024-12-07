"""Client library for interacting with BR API."""

import logging

import httpx
from models import (
    BackupRadarQueryParams,
    BackupRadarResponseModel,
    BackupRadarResultModel,
    BackupRadarSingleBackupQueryParams,
)


class BackupRadarAPI:
    """Base class for interacting with the BackupRadar API."""

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.backupradar.com",
    ) -> None:
        """Init BR class, set variables."""
        self.base_url = f"{base_url}/backups"
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
        params = query_params.model_dump(exclude_unset=True)
        try:
            response = httpx.get(self.base_url, headers=self.headers, params=params)
            response.raise_for_status()

            return BackupRadarResponseModel.model_validate_json(response.text)
        except httpx.HTTPError:
            logging.exception("HTTP Error")
        except Exception:
            logging.exception("Other error occurred.")

        return None

    def get_backup_results(
        self,
        query_params: BackupRadarSingleBackupQueryParams,
    ) -> BackupRadarResultModel | None:
        """Get backup results for a given backup for a given day."""
        params = query_params.model_dump(exclude_unset=True)

        try:
            response = httpx.get(url=self.base_url, headers=self.headers, params=params)
            response.raise_for_status()
            return BackupRadarResultModel.model_validate_json(response.text)
        except (httpx.HTTPStatusError, httpx.HTTPError):
            logging.exception("Request failed with error.")
            return None

    def get_backup(
        self,
        query_params: BackupRadarSingleBackupQueryParams,
    ) -> BackupRadarResultModel | None:
        """Get backup data for a given backup on a given day."""
        params = query_params.model_dump(exclude_unset=True)

        try:
            response = httpx.get(url=self.base_url, headers=self.headers, params=params)
            response.raise_for_status()
            return BackupRadarResultModel.model_validate_json(response.text)
        except (httpx.HTTPStatusError, httpx.HTTPError):
            logging.exception("Request failed with error.")
            return None
