"""Порты Level 1: узкие интерфейсы окружающих подсистем.

Scanner зависит от протоколов, а не от конкретных реализаций
(``25_PROJECT_STRUCTURE.md`` §8). Это удерживает Level 1 от знания деталей
провайдеров (``02_LEVEL1_SCANNER.md`` §10), Fee System (§29-30),
gas (``10_LEVEL_1_SCANNER.md`` §51) и хранилища.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from monik.domain.models.conversion import ConversionRate
from monik.domain.models.fee import Fee
from monik.domain.models.gas import Gas
from monik.domain.models.job import Level2Job
from monik.domain.models.opportunity import Opportunity
from monik.domain.models.scan import Scan
from monik.domain.models.token import Token
from monik.domain.value_objects.fingerprints import OpportunityFingerprint
from monik.domain.value_objects.identity import NetworkId
from monik.domain.value_objects.timestamps import UtcDatetime
from monik.services.fees.context import FeeContext

__all__ = [
    "FeeSource",
    "GasSource",
    "IdSequenceSource",
    "Level2Dispatcher",
    "OpportunityStore",
    "RateSource",
    "ScanStore",
]


@runtime_checkable
class FeeSource(Protocol):
    """Источник комиссий. Level 1 не реализует provider-specific fee logic (§29)."""

    async def fees_for(self, context: FeeContext) -> tuple[Fee, ...]:
        """Комиссии, применимые к контексту операции."""
        ...


@runtime_checkable
class GasSource(Protocol):
    """Источник оценки газа (``10_LEVEL_1_SCANNER.md`` §51)."""

    async def estimate(
        self,
        network_id: NetworkId,
        *,
        gas_units: int | None,
        source: str = "gas_estimator",
    ) -> Gas:
        """Стоимость исполнения; при недостатке данных — ``UNKNOWN``."""
        ...


@runtime_checkable
class RateSource(Protocol):
    """Источник курсов конверсии."""

    async def rate(self, from_token: Token, to_token: Token) -> ConversionRate | None:
        """Курс заданного направления или ``None``."""
        ...


@runtime_checkable
class OpportunityStore(Protocol):
    """Хранилище Opportunity с атомарным созданием Level 2 Job (§85)."""

    async def create_with_job(self, opportunity: Opportunity, job: Level2Job) -> None:
        """Создать Opportunity и её Job одной транзакцией."""
        ...

    async def find_recent_by_fingerprint(
        self, fingerprint: OpportunityFingerprint, *, since: UtcDatetime
    ) -> Opportunity | None:
        """Найти логически такую же возможность в окне дедупликации."""
        ...


@runtime_checkable
class ScanStore(Protocol):
    """Хранилище метаданных цикла (``02_LEVEL1_SCANNER.md`` §57)."""

    async def create(self, scan: Scan) -> None:
        """Сохранить начатый цикл."""
        ...

    async def update(self, scan: Scan) -> None:
        """Обновить состояние цикла."""
        ...


@runtime_checkable
class IdSequenceSource(Protocol):
    """Монотонные номера ``#V`` и ``#K`` (``CLAUDE.md`` §20)."""

    async def next_value(self, name: str) -> int:
        """Следующий номер последовательности."""
        ...


@runtime_checkable
class Level2Dispatcher(Protocol):
    """Приёмник Job: немедленная передача в Level 2 (§46).

    Level 1 не выполняет подтверждение сам (``10_LEVEL_1_SCANNER.md`` §61).
    """

    def available_capacity(self) -> int:
        """Сколько ещё Job принимается сейчас (backpressure, §47)."""
        ...

    async def submit(self, opportunity: Opportunity, job: Level2Job) -> None:
        """Передать Job на подтверждение."""
        ...
