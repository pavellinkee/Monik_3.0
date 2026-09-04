"""Notification System: режимы и типы destination."""

from __future__ import annotations

from monik.domain.enums.base import DomainEnum


class NotificationMode(DomainEnum):
    """Режим уведомлений (``CLAUDE.md`` §38, ``01_PROJECT_REQUIREMENTS.md`` §54).

    Режим влияет **только** на правила отправки уведомлений и не изменяет
    алгоритмы Level 1 / Level 2.
    """

    A = "A"
    B = "B"


class DestinationKind(DomainEnum):
    """Тип канала доставки.

    Destination является configuration/operational identity и не может
    приходить как произвольный внешний ввод (``36_DATA_MODELS.md`` §83).
    """

    TELEGRAM = "telegram"
