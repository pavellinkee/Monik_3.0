# MONIK 3.0 — DEVELOPMENT STATUS

> Обновляется после каждого значимого этапа.
> Порядок чтения при старте новой сессии:
> `git log` → **этот файл** → `DEVELOPMENT_PLAN.md` → документы этапа из §4 плана.

---

## ТЕКУЩЕЕ СОСТОЯНИЕ

| Поле | Значение |
|---|---|
| Дата обновления | 2026-09-04 |
| Ветка | `claude/monik-implementation` |
| Последний завершённый этап | **S0 — Project Foundation** |
| Следующий этап | **S1 — Domain: enums, value objects, models** |
| Статус разработки | ▶ идёт автономная разработка по DEVELOPMENT_PLAN.md |
| Тесты | 37 passed |
| Проверки | ruff ✅ · ruff format ✅ · mypy --strict ✅ · pytest ✅ |

---

## ЗАВЕРШЁННЫЕ ЭТАПЫ

### S-A — Аудит и планирование ✅

**Выполнено:**
- Полный аудит репозитория: структура, код, конфигурация, тесты, документация.
- Изучены `CLAUDE.md` (55 разделов), `README.md` (27 разделов) и ключевые документы
  `docs/architecture/`: 01, 02, 06, 09, 10, 11, 17, 25, 30, 35, 36, 38, 39, 42
  прочитаны полностью; остальные — по структуре разделов и критическим инвариантам.
- Зафиксирована карта документов и пары «одна подсистема — два документа».
- Проверена среда выполнения (Python, uv, PyPI, сетевой доступ к провайдерам).
- Составлен `DEVELOPMENT_PLAN.md`: 26 этапов (S0–S25), зависимости, тесты, риски.

**Результат аудита:** в репозитории **нет исходного кода** — только архитектурная
документация и tooling-конфигурация. Реализация выполняется с нуля.

**Ключевые проверки среды:**
- ✅ Python 3.12, `uv`, `git`; PyPI доступен, установка зависимостей проверена
  (нужен `UV_HTTP_TIMEOUT=180`).
- ❌ `api.1inch.dev`, `api.0x.org`, `api.uniswap.org`, `api.telegram.org` и
  официальные doc-сайты провайдеров **заблокированы egress-политикой**.
- ❌ API-ключей провайдеров и Telegram bot token в окружении **нет**.

**Тестирование:** не проводилось (кода нет).

---

### S-B — Фиксация архитектурных решений ✅

Пользователь принял решения D-1…D-6; они внесены в `DEVELOPMENT_PLAN.md` §9
и распространены на §2 (модели, потоки, state machines), §5 (этапы S4, S5, S10,
S12, S13, S14) и §8 (риски Р-2, Р-3).

Ключевое: **`Opportunity` — официальное имя сущности Level 1 (`#V`)**,
`Candidate` — промежуточный value object до прохождения проверок (не персистится).

---

### S0 — Project Foundation ✅

**Реализовано:**
- структура пакета `monik/` по `25_PROJECT_STRUCTURE.md` (app, config, domain,
  services, repositories, infrastructure с провайдерами) — 35 модулей, каждый
  с описанием своей ответственности;
- `tests/` с семью уровнями (unit, component, contract, integration,
  architecture, security, e2e);
- `pyproject.toml`: runtime-зависимости (httpx, pydantic, PyYAML, aiosqlite),
  hatch wheel target, console script `monik`, маркер `external`;
- `uv.lock` — воспроизводимая установка через `uv sync --group dev`;
- `Makefile` (install / lint / format / typecheck / test / check-architecture-docs / ci);
- GitHub Actions CI: ruff → ruff format --check → mypy --strict → pytest;
- `conftest.py`, `config/config.example.yaml`, `.env.example`, `scripts/README.md`.

**Тестирование:** `ruff check` ✅ · `ruff format --check` ✅ ·
`mypy --strict` ✅ (35 модулей) · `pytest` ✅ **37 passed**.

**Проверено фактически:** `uv sync --group dev` устанавливает pytest 8.4.2 и
pytest-asyncio 0.26.0 в соответствии с пинами `pyproject.toml`.

---

## GIT COMMITS

| Этап | Commit | Описание |
|---|---|---|
| S-A | `ae34f99` | `docs: add development plan and status tracking` |
| S-B | `d8d2f64` | `docs: fix accepted architectural decisions D-1..D-6 in development plan` |
| S0 | `5b58af8` | `chore: bootstrap project structure, tooling and CI` |

---

## ЧТО ОСТАЛОСЬ РЕАЛИЗОВАТЬ

Все 26 этапов плана:

| Этап | Модуль | Статус |
|---|---|---|
| S0 | Project foundation, tooling, CI | ✅ |
| S1 | Domain models, enums, value objects | 🔜 следующий |
| S2 | Errors, Clock, structured logging + redaction | ⬜ |
| S3 | Configuration subsystem | ⬜ |
| S4 | SQLite, schema, migrations, transactions | ⬜ |
| S5 | Repositories | ⬜ |
| S6 | Token/Network/Provider/Capability registries | ⬜ |
| S7 | HTTP infrastructure (TLS, SSRF, limits) | ⬜ |
| S8 | Resource Manager | ⬜ |
| S9.0 | Adapter contract + contract test suite + FakeAdapter | ⬜ |
| S9.1 | 1inch adapter | ⬜ |
| S9.2 | 0x adapter | ⬜ |
| S9.3 | Velora adapter | ⬜ |
| S9.4 | Uniswap adapter | ⬜ |
| S10 | Fee System, Gas System, conversion | ⬜ |
| S11 | Profit Calculator | ⬜ |
| S12 | Level 1 Scanner | ⬜ |
| S13 | Level 2 Scanner | ⬜ |
| S14 | Opportunity Service | ⬜ |
| S15 | Notification System + Telegram delivery + кнопка `об` | ⬜ |
| S16 | Telegram commands | ⬜ |
| S17 | Scheduler | ⬜ |
| S18 | Health Monitoring + Supervisor | ⬜ |
| S19 | Observability | ⬜ |
| S20 | App wiring, startup, recovery, shutdown | ⬜ |
| S21 | Integration / E2E тесты | ⬜ |
| S22 | Recovery / crash тесты | ⬜ |
| S23 | Architecture + security тесты | ⬜ |
| S24 | Performance проверки | ⬜ |
| S25 | Deployment, документация, финальный отчёт | ⬜ |

---

## ОТКРЫТЫЕ ПРОБЛЕМЫ И ОГРАНИЧЕНИЯ

| # | Вопрос | Статус |
|---|---|---|
| D-1 | Наименование сущности Level 1 | ✅ решено: `Opportunity` (`#V`); `Candidate` — промежуточный value object |
| D-2 | Telegram-команды и кнопка `об` | ✅ решено: входящий канал Notification-подсистемы |
| D-3 | Live-верификация провайдерских API | ✅ решено: адаптеры без live-проверки + `scripts/verify_provider_api.py` |
| D-4 | Источник gas и conversion rate | ✅ решено: `GasPriceProvider` / `TokenPriceProvider` как независимые абстракции |
| D-5 | Идентичность Velora | ✅ решено: `provider_id = "velora"` |
| D-6 | API-ключи и Telegram token | ✅ решено: только через environment variables, добавляются после разработки |

**Действующие ограничения среды:** провайдерские API, их doc-сайты, RPC и
Telegram API заблокированы egress-политикой; ключей нет. Все адаптеры и
внешние интеграции разрабатываются и тестируются на mocks/fakes и будут помечены
как непроверенные вживую.

---

## СЛЕДУЮЩИЙ ШАГ

**S1 — Domain: enums, value objects, models** согласно `DEVELOPMENT_PLAN.md` §5.

Ключевое для S1 (уже зафиксировано, документацию перечитывать не требуется):
- `Opportunity` — сущность Level 1 с `#V`-ID, единый lifecycle
  `CREATED → VERIFYING → {CONFIRMED, PARTIAL, UNPROFITABLE, ROUTE_UNAVAILABLE,
  EXPIRED, FAILED, CANCELLED} → {NOTIFIED, NOTIFIED_PARTIAL, NOTIFIED_FAILED}`;
- `Level2Job` — `#K`-ID, отдельное пространство идентификаторов;
- `Candidate` — промежуточный value object Level 1, не персистится;
- `int` для raw base units, `Decimal` для денег и процентов, `float` запрещён;
- все timestamps — timezone-aware UTC.
