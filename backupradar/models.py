"""Model definitions for requests and responses from the BackupRadar API."""

import re

from pydantic import BaseModel, ConfigDict

# Regex for converting camelCase to snake_case
regex_for_camel = re.compile(
    r"""
        (?<=[a-z])      # preceded by lowercase
        (?=[A-Z])       # followed by uppercase
    """,
    re.VERBOSE,
)


def to_snake(string: str) -> str:
    """Convert camelCase string to snake_case."""
    return regex_for_camel.sub("_", string).lower()


class BackupRadarStatusModel(BaseModel):
    """Status model for BackupRadar responses, contains id and status name.

    Used in: /backups, /backups/bg, /backups/{backupId}, /backups/inactive
    """

    model_config = ConfigDict(alias_generator=to_snake)
    id: int
    name: str | None = None


class BackupRadarHistoryModel(BaseModel):
    """Model for backup history from BackupRadar list response.

    Used in: /backups, /backups/bg, /backups/{backupId}
    """

    status: BackupRadarStatusModel
    last_result_date: str | None = None
    is_scheduled: bool
    days_in_status: float
    date: str
    count_failure: int
    count_warning: int
    count_success: int
    count_no_result: int
    days_since_last_result: float
    days_since_last_good_result: float
    results_count: int


class BackupRadarResultModel(BaseModel):
    """Overarching model for BackupRadar results including status, company, and history.

    Used in: /backups, /backups/{backupId}
    """

    ticketing_company: str | None = None
    status: BackupRadarStatusModel
    days_in_status: float
    is_verified: bool
    last_result: str | None = None
    last_success: str | None = None
    ticket_count: int
    failure_threshold: float | None = None
    treat_warning_as_success: bool
    note: str | None = None
    day_start_hour: int | None = None
    tags: list[str] | None = None
    standalone: bool
    history: list[BackupRadarHistoryModel] | None = None
    backup_id: int
    company_name: str | None = None
    device_name: str | None = None
    device_type: str | None = None
    job_name: str | None = None
    method_name: str | None = None
    backup_type: BackupRadarStatusModel


class BackupRadarResponseModel(BaseModel):
    """Model for paginated responses, contains list of BackupRadar results.

    Used in: /backups
    """

    total: int
    page: int
    page_size: int
    total_pages: int
    results: list[BackupRadarResultModel] | None = None


class BackupRadarSingleBackupQueryParams(BaseModel):
    """Query params for fetching a single backup by ID, with optional date filter.

    Used in: /backups/{backupId}
    """

    date: str | None = None


class BackupRadarQueryParams(BaseModel):
    """Model for query parameters to filter backup results, includes search filters.

    Used in: /backups
    """

    page: int = 1
    size: int = 50
    search_by_company_name: str | None = None
    search_by_device_name: str | None = None
    search_by_job_name: str | None = None
    search_by_backup_method: str | None = None
    search_by_tooltip: str | None = None
    search_by_tag: str | None = None
    days_without_success: int | None = None
    history_days: int | None = None
    filter_scheduled: bool | None = None
    date: str | None = None
    search_string: str | None = None
    companies: list[str] | None = None
    tags: list[str] | None = None
    exclude_tags: list[str] | None = None
    backup_methods: list[str] | None = None
    device_types: list[str] | None = None
    exclude_device_types: list[str] | None = None
    statuses: list[str] | None = None
    policy_ids: list[str] | None = None
    exclude_backup_methods: list[str] | None = None
    policy_types: list[str] | None = None


class BackupRadarInactiveBackupModel(BaseModel):
    """Model for inactive backup records, includes device and job details.

    Used in: /backups/inactive, /backups/retired
    """

    email_from: str | None = None
    last_received: str | None = None
    backup_id: int
    company_name: str | None = None
    device_name: str | None = None
    device_type: str | None = None
    job_name: str | None = None
    method_name: str | None = None
    backup_type: BackupRadarStatusModel


class BackupRadarInactivePaginatedResponse(BaseModel):
    """Paginated response model for inactive backups.

    Used in: /backups/inactive, /backups/retired
    """

    total: int
    page: int
    page_size: int
    total_pages: int
    results: list[BackupRadarInactiveBackupModel] | None = None


class BackupRadarOverviewCountsModel(BaseModel):
    """Model for backup counts, provides totals for backups, policies, and workstations.

    Used in: /backups/overview
    """

    backups: int
    office365: int
    workstations: int
    active_policies: int
    inactive_policies: int
    retired_policies: int


class BackupRadarFiltersResponseModel(BaseModel):
    """Model for the available filter options.

    Used in: /backups/filters
    """

    device_types: list[str] | None = None
    companies: list[str] | None = None
    backup_methods: list[str] | None = None
    statuses: list[str] | None = None
    tags: list[str] | None = None
    policy_types: list[str] | None = None


class BackupRadarBackupResultModel(BaseModel):
    """Model representing individual backup results for a specific date.

    Used in: /backups/{backupId}/results
    """

    date_time: str
    success: bool
    warning: bool
    failure: bool
    manual: bool
    result_id: str | None = None


class BackupRadarBrightGaugeBackupModel(BaseModel):
    """Model for BrightGauge backups, includes device, job, and backup results.

    Used in: /backups/bg
    """

    id: int
    job: str | None = None
    device: str | None = None
    company: str | None = None
    device_type: str | None = None
    ticketing_company: str | None = None
    method: str | None = None
    is_verified: bool
    history: list[BackupRadarHistoryModel] | None = None
    results: dict[str, list[BackupRadarBackupResultModel]] | None = None


class BackupRadarPaginatedResponse(BaseModel):
    """Generic paginated response model, used for standard results.

    Used in: /backups, /backups/bg
    """

    total: int
    page: int
    page_size: int
    total_pages: int
    results: list[BackupRadarBackupResultModel] | None = None


class BackupRadarRetiredQueryParams(BaseModel):
    """Query parameters for filtering retired backups.

    Used in: /backups/retired
    """

    search_by_company_name: str | None = None
    search_by_device_name: str | None = None
    search_by_job_name: str | None = None
    search_by_backup_method: str | None = None
    search_by_email_from: str | None = None
    search_by_retire_message: str | None = None
    search_by_retired_by: str | None = None
    search_by_retired_date_start: str | None = None
    search_by_retired_date_end: str | None = None
    page: int = 1
    size: int = 50
