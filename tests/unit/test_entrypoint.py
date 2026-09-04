"""Entrypoint не должен притворяться работающим приложением."""

from __future__ import annotations

from monik.app.main import run


def test_entrypoint_reports_not_implemented() -> None:
    """Пока wiring не реализован (S20), запуск обязан завершаться ненулевым кодом."""
    exit_code = run()
    assert exit_code != 0
