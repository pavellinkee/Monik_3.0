"""Application entrypoint.

Здесь не должно быть business logic (``25_PROJECT_STRUCTURE.md`` §5).
Реальная последовательность запуска реализуется на этапе S20 плана
и обязана следовать порядку из ``CLAUDE.md`` §30:

configuration -> SQLite -> integrity -> migrations -> recovery -> adapters ->
Resource Manager -> Scheduler -> Telegram -> workers.
"""

from __future__ import annotations

import sys


def run() -> int:
    """Console entrypoint ``monik``.

    Пока приложение не собрано (этап S20), команда явно сообщает об этом
    и завершается с ненулевым кодом, а не имитирует успешный запуск.
    """
    sys.stderr.write(
        "monik: application wiring is not implemented yet (stage S20 of DEVELOPMENT_PLAN.md)\n"
    )
    return 1


if __name__ == "__main__":  # pragma: no cover - тонкая обёртка
    raise SystemExit(run())
