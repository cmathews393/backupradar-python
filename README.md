BackupRadar API Python Library

A Python client library for interacting with the BackupRadar API. This library provides an easy-to-use interface for integrating with BackupRadar, allowing you to manage and interact with your backup monitoring data.

Features

- Authentication: Seamless integration with BackupRadar API using API keys.
- Backup Jobs: Fetch, create, update, and delete backup jobs.
- Reports: Retrieve various backup reports from BackupRadar.
- Accounts & Users: Manage accounts and user settings.
- Error Handling: Custom exceptions for API-specific errors.
- Pagination Support: Built-in pagination support for large result sets.
- Async Support: Optional async support using HTTPX for non-blocking API requests.

Installation

Install the package using Poetry (recommended):

```bash
poetry add backupradar-python
```

Alternatively, you can install it using pip:

```bash
pip install backupradar-python
```

Requirements

- Python 3.8+
- httpx for making HTTP requests
- pydantic for data validation and parsing

## Quick Start

Here is an example of how to use the BackupRadar Python library:

### Synchronous Example

from backupradar.client import BackupRadarClient

# Initialize the client with your API key

api_key = "your-api-key"
client = BackupRadarClient(api_key=api_key)

# Fetch backup jobs

jobs = client.get_backup_jobs()
for job in jobs:
    print(job)

# Create a new backup job

new_job = client.create_backup_job({
    "name": "New Backup Job",
    "schedule": "daily",
    # Other necessary fields
})
print(f"Created backup job: {new_job['id']}")

Asynchronous Example

import asyncio
from backupradar.client import AsyncBackupRadarClient

async def main():
    api_key = "your-api-key"
    async_client = AsyncBackupRadarClient(api_key=api_key)

    # Fetch backup jobs asynchronously
    jobs = await async_client.get_backup_jobs()
    for job in jobs:
        print(job)

    await async_client.close()

asyncio.run(main())

Configuration

The BackupRadarClient accepts various configuration options:

- api_key: Your BackupRadar API key (required).
- base_url: The base URL for the BackupRadar API (defaults to the official BackupRadar endpoint).
- timeout: Request timeout (defaults to 30 seconds).

You can configure these options during initialization:

client = BackupRadarClient(api_key="your-api-key", base_url="<https://custom-api-url.com>", timeout=60)

Endpoints

- Backup Jobs: get_backup_jobs(), create_backup_job(), update_backup_job(), delete_backup_job()
- Reports: get_reports()
- Accounts: get_accounts(), create_account(), update_account(), delete_account()
- Users: get_users(), create_user(), update_user(), delete_user()

For detailed information on all available endpoints, see the BackupRadar API Documentation.

Error Handling

The library raises custom exceptions for different error types:

- BackupRadarClientError: Base exception class for client-related errors.
- BackupRadarAuthenticationError: Raised for authentication failures.
- BackupRadarNotFoundError: Raised when a requested resource is not found.
- BackupRadarRateLimitError: Raised when the API rate limit is exceeded.

Example:

try:
    client.get_backup_jobs()
except BackupRadarAuthenticationError:
    print("Invalid API key.")
except BackupRadarRateLimitError:
    print("Rate limit exceeded. Try again later.")

Running Tests

The library comes with a set of unit tests. To run the tests, install the development dependencies and run:

$ poetry install --with dev
$ poetry run pytest

Contributing

Contributions are welcome! If you'd like to improve the library, feel free to open a pull request or report an issue.

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/my-feature`).
3. Commit your changes (`git commit -am 'Add my feature'`).
4. Push to the branch (`git push origin feature/my-feature`).
5. Create a new Pull Request.

License

This project is licensed under the MIT License - see the LICENSE file for details.

Happy coding! If you have any questions or issues, feel free to open an issue in the repository.
