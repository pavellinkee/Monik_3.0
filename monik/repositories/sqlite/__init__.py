"""SQLite implementations. Единственное место с SQL.

Проверяется architecture-тестом: raw SQL и драйвер SQLite не используются
за пределами этого пакета и ``monik.infrastructure.db``.
"""

from monik.repositories.sqlite.jobs import SqliteJobRepository
from monik.repositories.sqlite.opportunities import SqliteOpportunityRepository
from monik.repositories.sqlite.scans import SqliteScanRepository
from monik.repositories.sqlite.sequences import (
    JOB_SEQUENCE,
    NOTIFICATION_SEQUENCE,
    OPPORTUNITY_SEQUENCE,
    SqliteIdSequenceRepository,
)

__all__ = [
    "JOB_SEQUENCE",
    "NOTIFICATION_SEQUENCE",
    "OPPORTUNITY_SEQUENCE",
    "SqliteIdSequenceRepository",
    "SqliteJobRepository",
    "SqliteOpportunityRepository",
    "SqliteScanRepository",
]
