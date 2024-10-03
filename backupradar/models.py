"""Model definitions for requests and responses from the BackupRadar API."""

from pydantic import BaseModel


class StatusModel(BaseModel):
    """Status model for BackupRadar responses.

    "name" could be better represented as status, i.e. Success/Failure.
    """

    id: int
    name: str


class HistoryModel(BaseModel):
    """Model for backup history from backupradar list response."""

    status: StatusModel
    last_result_date: str
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
    """Overarching model for BackupRadar Results including submodels."""

    ticketing_company: str
    status: StatusModel
    days_in_status: float
    is_verified: bool
    last_result: str
    last_success: str
    ticket_count: int
    failure_threshold: int
    treat_warning_as_success: bool
    note: str | None = None
    day_start_hour: int
    tags: list[str]
    standalone: bool
    history: list[HistoryModel]
    backup_id: int
    company_name: str
    device_name: str
    device_type: str
    job_name: str
    method_name: str
    backup_type: StatusModel


class BackupRadarResponseModel(BaseModel):
    """Model for generic response, contains a list of results."""

    total: int
    page: int
    page_size: int
    total_pages: int
    results: list[BackupRadarResultModel]


class BackupRadarQueryParams(BaseModel):
    """Model for query parameters to be sent alongside a request."""

    page: int
    size: int
    search_by_company_name: str | None
    search_by_device_name: str | None
    search_by_job_name: str | None
    search_by_backup_method: str | None
    search_by_tooltip: str | None
    search_by_tag: str | None
    days_without_success: int | None
    history_days: int | None
    filter_scheduled: bool | None
    date: str | None
    search_string: str | None
    companies: list[str] | None
    tags: list[str] | None
    exclude_tags: list[str] | None
    backup_methods: list[str] | None
    device_types: list[str] | None
    exclude_device_types: list[str] | None
    statuses: list[str] | None
    policy_ids: list[str] | None
    exclude_backup_methods: list[str] | None
    policy_types: list[str] | None
