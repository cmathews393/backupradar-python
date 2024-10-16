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
    """Status model for BackupRadar responses, contains id and status name."""

    model_config = ConfigDict(alias_generator=to_snake)
    id: int
    name: str | None = None


class BackupRadarHistoryModel(BaseModel):
    """Model for backup history from BackupRadar list response."""

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
    """Overarching model for BackupRadar results including details about status, company, and history."""

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
    backup_type: BackupRadarStatusModel  # I don't think this is correct?


class BackupRadarResponseModel(BaseModel):
    """Model for paginated responses, contains list of BackupRadar results."""

    total: int
    page: int
    page_size: int
    total_pages: int
    results: list[BackupRadarResultModel] | None = None


class BackupRadarSingleBackupQueryParams(BaseModel):
    """Query params for fetching a single backup by ID, with optional date filter."""

    backup_id: int
    date: str | None = None


class BackupRadarQueryParams(BaseModel):
    """Model for query parameters to filter backup results, includes various search filters."""

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
    """Model for inactive backup records, includes device and job details."""

    email_from: str | None = None
    last_received: str | None = None
    backup_id: int
    company_name: str | None = None
    device_name: str | None = None
    device_type: str | None = None
    job_name: str | None = None
    method_name: str | None = None
    backup_type: StatusModel


class BackupRadarPaginatedResponse(BaseModel):
    """Generic paginated response model, used for standard results."""

    total: int
    page: int
    page_size: int
    total_pages: int
    results: list[BackupRadarResultModel] | None = None


class BackupRadarInactivePaginatedResponse(BaseModel):
    """Paginated response model for inactive backups."""

    total: int
    page: int
    page_size: int
    total_pages: int
    results: list[BackupRadarInactiveBackupModel] | None = None


class BackupRadarOverviewCountsModel(BaseModel):
    """Model for backup overview counts, provides totals for backups, policies, and workstations."""

    backups: int
    office365: int
    workstations: int
    active_policies: int
    inactive_policies: int
    retired_policies: int


class BackupRadarFiltersResponseModel(BaseModel):
    """Model for the available filter options, including device types, companies, methods, etc."""

    device_types: list[str] | None = None
    companies: list[str] | None = None
    backup_methods: list[str] | None = None
    statuses: list[str] | None = None
    tags: list[str] | None = None
    policy_types: list[str] | None = None


class BackupRadarBackupResultModel(BaseModel):
    """Model representing individual backup results for a specific date."""

    date_time: str
    success: bool
    warning: bool
    failure: bool
    manual: bool
    result_id: str | None = None


class BackupRadarBrightGaugeBackupModel(BaseModel):
    """Model for BrightGauge backups, includes details about device, job, and backup results."""

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
