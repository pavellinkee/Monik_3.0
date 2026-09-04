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
| Последний завершённый этап | **S5 — Repositories** |
| Следующий этап | **S6 — Token / Network / Provider / Capability registries** |
| Статус разработки | ▶ идёт автономная разработка по DEVELOPMENT_PLAN.md |
| Тесты | 1105 passed |
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

### S1 — Domain: enums, value objects, models ✅

**Реализовано (`monik/domain/`, 33 модуля):**
- **enums** — стабильные строковые значения (часть контракта БД): providers,
  operations и routing modes, quote status, fee types/status/inclusion,
  calculation status и threshold metric, lifecycle (Opportunity, Job,
  per-amount verification и confirmation, notification, scan, task execution),
  capability, health, errors, resources (priority с рангом, circuit state),
  notification modes, scheduler modes и overlap policy;
- **value objects** — числовые типы, отклоняющие `float`; timezone-aware UTC
  timestamps; `NetworkId` / `TokenAddress` / `TokenSymbol` с нормализацией;
  идентификаторы `#V` / `#K` в раздельных пространствах; детерминированные
  fingerprints; `TokenAmount` (raw base units + decimals) и `Percentage`;
- **models** — Network, Token, Provider, Route/RouteStep, Quote,
  Fee/FeeKey/FeeSnapshot, Gas/GasPrice, ConversionRate,
  ProfitCalculationInput/CostBreakdown/ThresholdOutcome/ProfitResult,
  Opportunity/OpportunityAmount/Candidate/RouteSnapshot,
  Level2Job/Level2Attempt/AmountVerificationResult/ConfirmationResult,
  Notification, Scan, Capability, Health, Resource, Scheduler.

**Инварианты, закреплённые кодом и тестами:**
UNKNOWN fee/gas не имеют суммы и не равны нулю · `included_in_quote` защищает
от двойного учёта · SELL считается от текущего BUY output · один route snapshot
на все суммы · ROUTE_UNAVAILABLE ≠ UNPROFITABLE · PARTIAL ≠ CONFIRMED ·
UNKNOWN capability ≠ SUPPORTED · очередь Level 2 > Level 1 SELL > Level 1 BUY >
Maintenance · порядок уведомлений по `created_at` + sequence.

**Тестирование:** `pytest` ✅ **466 passed** (unit + architecture);
`ruff` ✅ · `ruff format` ✅ · `mypy --strict` ✅ (73 модуля).

Architecture-тесты проверяют, что domain не импортирует HTTP/SQLite/Telegram/
верхние слои, не читает environment, не использует `float`, а все модели
frozen с `extra="forbid"`.

---

### S2 — Errors, Clock, structured logging + redaction ✅

**Реализовано:**
- `monik/domain/errors/` — `ErrorInfo` (сериализуемая модель ошибки) и
  иерархия `MonikError`: Configuration, DomainValidation, Calculation,
  Cancellation, Internal, Network, Timeout, RateLimit, Authentication,
  Provider, Data, Unsupported, Database, Resource; классификация
  retryable / non-retryable / conditional с учётом retry budget;
- `monik/services/observability/clock.py` — `Clock` protocol, `SystemClock`,
  `FakeClock` (детерминированное время, движение только вперёд);
- `monik/services/observability/context.py` — `CorrelationContext` на
  `contextvars` (scan_id, v_id, k_id, request_id, provider, network,
  operation), изолирован между конкурентными корутинами;
- `monik/services/observability/redaction.py` — `SecretRegistry` и редакция
  по именам полей и по шаблонам (Bearer, Telegram bot token в том числе
  внутри URL, приватный ключ, `key=value`);
- `monik/services/observability/logging.py` — `StructuredFormatter`:
  одна JSON-строка на запись, поля корреляции, классификация ошибки;
  редакция применяется к финальной строке, traceback не выводится.

**Инварианты:** UNSUPPORTED отделён от временного сбоя · data error и ошибка
аутентификации не повторяются · rate limit обрабатывается retry-политикой и
не является признаком убыточности · бесконечные повторы невозможны.

**Тестирование:** `pytest` ✅ **566 passed**; `ruff` ✅ · `ruff format` ✅ ·
`mypy --strict` ✅ (81 модуль).

Security-тесты (`tests/security/`) подтверждают, что секрет не появляется
в выводе логгера ни на одном уровне — в сообщении, структурированном поле,
тексте исключения и контексте корреляции.

---

### S3 — Configuration subsystem ✅

**Реализовано (`monik/config/`):**
- секции: `application` (environment, IANA timezone), `networks`, `providers`,
  `tokens`, `routes` (политика пар провайдеров), `scanner` (level1/level2),
  `profitability`, `fees`, `gas`, `prices`, `resources` (retry, circuit
  breaker), `scheduler`, `notifications.telegram`, `database` (retention),
  `logging`, `metrics`;
- loader: YAML → env overrides (`MONIK__SECTION__FIELD`) → defaults →
  validation → immutable `Configuration` с детерминированным `version`;
  приоритет: env override > файл > безопасный default;
- секреты: `SecretRef` (`{env: "MONIK_..."}`), `SecretResolver` —
  единственное место, читающее `os.environ`; `SecretValue` не раскрывает
  значение в `repr`/`str`; `SecretStore` хранится **отдельно** от модели,
  поэтому дамп и fingerprint конфигурации физически не содержат секретов;
- `configuration_diagnostics` — безопасный снимок состояния;
- полный `config/config.example.yaml` и `.env.example`.

**Cross-subsystem валидация:** уникальность идентификаторов · tokens ↔
networks · providers ↔ networks · routes ↔ providers · amounts ↔ token
precision · базовая сеть и базовый токен · наличие торгуемой пары ·
production-safety (нет DEBUG-логов, у enabled-провайдера есть credentials
reference, integrity check включён).

**Инварианты, которые нельзя отключить конфигурацией:** unknown fee/gas ≠ 0 ·
Level 2 обязан подтверждать зафиксированный маршрут · `Retry-After`
обязателен · foreign keys включены · неизвестный расход блокирует порог.

**Тестирование:** `pytest` ✅ **649 passed**; `ruff` ✅ · `ruff format` ✅ ·
`mypy --strict` ✅ (100 модулей).

---

### S4 — Database: соединение, схема, migrations, транзакции ✅

**Реализовано (`monik/infrastructure/db/`):**
- `Database` — соединение `aiosqlite` с обязательными PRAGMA (WAL,
  `foreign_keys=ON`, busy timeout, `synchronous=FULL`), integrity check,
  ограниченный retry при блокировке, сериализация записей одним локом;
- `Transaction` — обёртка, переводящая исключения драйвера в `DatabaseError`;
- `TransactionManager` — границы атомарных операций;
- `MigrationRunner` — последовательное применение миграций, каждая в одной
  транзакции; `schema_migrations`; отказ при неизвестной версии схемы;
- `types` — `Decimal` и raw amounts хранятся как `TEXT` (raw amount токена
  с 18 decimals превышает диапазон `INTEGER` SQLite), timestamps — ISO-8601 UTC.

**Миграция 0001 — 18 таблиц:** `app_metadata`, `id_sequences`, `scans`,
`opportunities`, `opportunity_amounts`, `level2_jobs`, `level2_attempts`,
`level2_amount_results`, `notifications`, `notification_attempts`,
`fee_snapshots`, `fee_records`, `gas_snapshots`, `capabilities`,
`scheduler_tasks`, `scheduler_executions`, `state_transitions`,
`schema_migrations`.

**Ограничения схемы:** `UNIQUE(opportunity_id)` на `level2_jobs` (дедупликация
Level 2 workflow) · `UNIQUE(opportunity_id, destination_id)` на
`notifications` (идемпотентность доставки) · `UNIQUE v_id` · `RESTRICT` на
удаление opportunity с уведомлениями · `SET NULL` при удалении scan ·
`CASCADE` только внутри агрегата.

**Тестирование:** `pytest` ✅ **997 passed**; `ruff` ✅ · `ruff format` ✅ ·
`mypy --strict` ✅ (107 модулей).

Architecture-тесты: драйвер SQLite и raw SQL не используются вне db-слоя,
транзакция не оборачивает внешний вызов, в схеме нет `REAL`-колонок и колонок
для секретов. Security-тест: тесты не обращаются к production-пути БД.

---

### S5 — Repositories ✅

**Миграция 0002:** `preliminary_result_json` и `buy_output_decimals` для
`opportunity_amounts`; `buy_quote_json` и `sell_quote_json` для
`level2_amount_results`. Decimals промежуточного токена хранятся явно.

**Реализовано (`monik/repositories/`):**
- интерфейсы-Protocol в `interfaces/`, реализации в `sqlite/`;
- `SqliteIdSequenceRepository` — монотонные `#V` и `#K` в раздельных
  пространствах, переживают рестарт;
- `SqliteScanRepository` — метаданные и статистика циклов, cleanup только
  завершённых;
- `SqliteOpportunityRepository` — **атомарное** создание Opportunity +
  amount-контекстов + Level 2 Job, поиск по `#V`, дедупликация по
  fingerprint в окне, выборки по статусу и истечению;
- `SqliteJobRepository` — Job, попытки, per-amount результаты; котировки
  сохраняются только для проверенных сумм как подтверждение решения;
- `SqliteNotificationRepository` — очередь по `created_at + sequence`,
  logical identity `opportunity + destination`, тексты для кнопки «об»;
- `SqliteFeeRepository` / `SqliteGasRepository` — снимки с сохранением
  UNKNOWN без суммы, контекстная выборка, retention;
- `SqliteCapabilityRepository`, `SqliteSchedulerRepository`,
  `SqliteStateTransitionRepository`.

**Тестирование:** `pytest` ✅ **1105 passed**; `ruff` ✅ · `ruff format` ✅ ·
`mypy --strict` ✅ (123 модуля).

---

## GIT COMMITS

| Этап | Commit | Описание |
|---|---|---|
| S-A | `ae34f99` | `docs: add development plan and status tracking` |
| S-B | `d8d2f64` | `docs: fix accepted architectural decisions D-1..D-6 in development plan` |
| S0 | `5b58af8` | `chore: bootstrap project structure, tooling and CI` |
| S0 | `d87328e` | `docs: update development status after stage S0` |
| S1 | `d434557` | `feat: add canonical domain models, enums and value objects` |
| S1 | `bcd9a93` | `docs: update development status after stage S1` |
| S2 | `316d14e` | `feat: add normalized error model, clock abstraction and redacting structured logger` |
| S2 | `26a53e5` | `docs: update development status after stage S2` |
| S3 | `d4f9803` | `feat: implement configuration loading, validation and secret references` |
| S3 | `93b2df1` | `docs: update development status after stage S3` |
| S4 | `0660ba8` | `feat: add sqlite infrastructure, schema migrations and transaction manager` |
| S4 | `c69065e` | `docs: update development status after stage S4` |
| S5 | `19503b8` | `feat: add core repositories for scans, opportunities and level 2 jobs` |
| S5 | `780d2a6` | `feat: add notification, fee, gas, capability, scheduler and audit repositories` |

---

## ЧТО ОСТАЛОСЬ РЕАЛИЗОВАТЬ

Все 26 этапов плана:

| Этап | Модуль | Статус |
|---|---|---|
| S0 | Project foundation, tooling, CI | ✅ |
| S1 | Domain models, enums, value objects | ✅ |
| S2 | Errors, Clock, structured logging + redaction | ✅ |
| S3 | Configuration subsystem | ✅ |
| S4 | SQLite, schema, migrations, transactions | ✅ |
| S5 | Repositories | ✅ |
| S6 | Token/Network/Provider/Capability registries | 🔜 следующий |
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

**S6 — Registries** согласно `DEVELOPMENT_PLAN.md` §5.

Что нужно сделать (`monik/services/registries/`):
- `NetworkRegistry` — enabled сети, chain_id, native token;
- `TokenRegistry` — authoritative token metadata (symbol, address, decimals,
  network, enabled), нормализация адресов, выбор Top-N; источник —
  configuration, hard-code списка запрещён;
- `ProviderRegistry` — регистрация Adapter'ов и enabled-состояние;
- `CapabilityRegistry` — состояния `SUPPORTED/UNSUPPORTED/UNKNOWN/DEGRADED/
  UNAVAILABLE/STALE/CHECKING/FAILED`, freshness, persistence через
  `SqliteCapabilityRepository`, failure/recovery thresholds, change detection.

Ключевые правила (уже зафиксированы): `UNKNOWN ≠ SUPPORTED` · discovery
выполняется только на startup и по расписанию, не перед каждым scan ·
runtime-ошибка не переводит capability в `UNSUPPORTED` мгновенно ·
Circuit Breaker **не меняет** Capability Registry · статические запросы
не делают сетевых вызовов.

Обязательные тесты этапа: identity токена, нормализация адресов, фильтрация
disabled, capability lookup и freshness, обработка STALE, пороги деградации
и восстановления, запрет мгновенного permanent disable, отсутствие сетевых
вызовов при статических запросах.
