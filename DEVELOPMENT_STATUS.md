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
| Последний завершённый этап | **S12 — Level 1 Scanner** |
| Следующий этап | **S13 — Level 2 Scanner** |
| Статус разработки | ▶ идёт автономная разработка по DEVELOPMENT_PLAN.md |
| Тесты | 2310 passed |
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

### S6 — Registries ✅

**Реализовано (`monik/services/registries/`):**
- `NetworkRegistry` — сети из конфигурации, enabled-фильтр, RPC endpoint,
  canonical identity обёрнутого native token (поле стало обязательным
  в доменной модели `Network`);
- `TokenRegistry` — authoritative metadata, поиск по canonical identity и по
  адресу без учёта регистра, `decimals` только отсюда, поиск по символу
  возвращает набор, Top-N набор для сканирования без базового токена;
- `ProviderRegistry` — enabled-состояние, объявленные сети (не подтверждение
  поддержки), допустимые пары BUY/SELL;
- `CapabilityRegistry` — свежесть (`SUPPORTED → STALE`), persistence и
  загрузка при старте, discovery, пороги подряд идущих отказов, снимок и
  список устаревших ключей.

Добавлена секция конфигурации `capabilities`.

**Инварианты, закреплённые тестами:** `UNKNOWN ≠ SUPPORTED` и не блокирует
runtime-проверку · `UNSUPPORTED` блокирует запрос · timeout, rate limit и
отказ Resource Manager не переводят capability в `UNSUPPORTED` · один сигнал
`UNSUPPORTED` недостаточен · успех сбрасывает счётчик · просроченная
поддержка становится `STALE` · ключи независимы · lookup без ввода-вывода.

**Тестирование:** `pytest` ✅ **1157 passed**; `ruff` ✅ · `ruff format` ✅ ·
`mypy --strict` ✅ (128 модулей).

---

### S7 — HTTP infrastructure ✅

**Реализовано (`monik/infrastructure/http/`, секция конфигурации `http`):**
- `UrlPolicy` — allowlist хостов и защита от SSRF: только `https`, запрет
  credentials в URL, блокировка loopback, приватных, link-local, reserved,
  multicast и unspecified адресов;
- `HttpRequest` / `HttpResponse` — нормализованные контракты, объекты `httpx`
  наружу не выходят; некорректный JSON — `DataError`;
- `HttpxClient` — проверка URL до отправки и повторная проверка финального
  URL после редиректа, лимит размера тела, длительность по монотонным часам,
  нормализация transport-ошибок; retry и rate limiting **не** реализуются —
  это ответственность Resource Manager;
- `classify_response` — 429 → `RateLimitError` с разбором `Retry-After`,
  401/403 → `AuthenticationError`, 5xx → `ProviderError`, прочие 4xx →
  `DataError`;
- `FakeHttpClient` — детерминированная **test implementation**.

`verify_tls` отключить нельзя.

**Тестирование:** `pytest` ✅ **1355 passed**; `ruff` ✅ · `ruff format` ✅ ·
`mypy --strict` ✅ (133 модуля).

Architecture-тесты: HTTP-библиотеки не импортируются вне
`monik/infrastructure/http`; `verify=False` отсутствует в коде.
Security-тесты: заголовок авторизации и API-ключ не попадают в логи.

---

### S8 — Resource Manager ✅

**Реализовано (`monik/services/resources/`):**
- `RetryPolicy` — ограниченный бюджет попыток, экспоненциальный backoff,
  jitter в границах, приоритет `Retry-After`;
- `CircuitBreaker` — `CLOSED/OPEN/HALF_OPEN`, ограничение пробных вызовов,
  восстановление; **не изменяет** Capability Registry;
- `RateLimiter` — token bucket с явной стоимостью batch-запроса;
- `PriorityGate` — очередь по приоритету, затем `created_at` и `sequence`;
  backpressure, таймаут ожидания, гарантированный возврат слота при отмене;
- `InFlightRegistry` — объединение одинаковых одновременных запросов;
- `ResourceManager` — иерархический захват ворот в детерминированном
  порядке, timeout, retry, circuit breaker per resource, дедупликация,
  метрики задержек.

Время и ожидание инъектируются (`Clock`, `Sleeper`) — тесты детерминированы.

**Тестирование:** `pytest` ✅ **1427 passed**; `ruff` ✅ · `ruff format` ✅ ·
`mypy --strict` ✅ (139 модулей).

---

### S9.0 — Контракт адаптеров ✅

`AggregatorAdapter` protocol · `QuoteRequest` с проверкой согласованности ·
`RouteValidation` (`REPRODUCED` / `MISMATCH` / `UNSUPPORTED`) ·
`AdapterCapabilities` и `AdapterHealth` · модуль нормализации (разбор raw
amounts без float, отказ подставлять ноль, сборка маршрута и котировки с
проверкой провайдера, сети, операции и токенов) · `FakeAdapter` —
**test implementation** · `tests/contract/adapter_contract.py` — общий набор
требований, который обязан пройти каждый адаптер.

---

### S9.1 — 1inch adapter ✅

⚠️ **API contract NOT verified against live endpoint** (решение D-3).

- `endpoints.py` — базовый URL, версия API, chain id, пути
  quote / tokens / liquidity-sources; все provider-specific детали в одном
  файле;
- `HttpProviderAdapter` — общая основа HTTP-адаптеров: запрос через
  Resource Manager, credentials, нормализация статусов;
- `OneInchAdapter` — построение запроса, разбор `dstAmount` и `gas` без
  float, нормализация маршрута из `protocols` с устойчивым отпечатком,
  честное объявление отсутствия fixed-route поддержки, сравнение отпечатков
  для Level 2, `discover_fees` без выдуманных нулей, health check.

**Тестирование:** `pytest` ✅ **1520 passed**; `ruff` ✅ · `ruff format` ✅ ·
`mypy --strict` ✅ (145 модулей).

---

### S9.2 — 0x adapter ✅

⚠️ **API contract NOT verified against live endpoint** (решение D-3).

Swap API v2 (allowance-holder): собственная схема аутентификации
(`0x-api-key` + `0x-version`), индикативная цена `/swap/allowance-holder/price`
(Monik не исполняет свопы), разбор `buyAmount` и `gas` без float, проверка
совпадения `sellAmount`, маршрут из `route.fills` с устойчивым отпечатком.

---

### S9.3 — Velora (ParaSwap) adapter ✅

⚠️ **API contract NOT verified against live endpoint** (решение D-3).
Решение D-5: `provider_id = "velora"`, базовый URL `api.paraswap.io`
переопределяется конфигурацией.

Market API: используется только `/prices`; параметры включают
`srcDecimals`/`destDecimals` из метаданных токена; разбор `priceRoute`
(`destAmount`, `gasCost`), проверка `srcAmount`, рекурсивный сбор
обменников из вложенного `bestRoute`; работа без ключа с опциональным
partner-заголовком.

---

### S9.4 — Uniswap adapter ✅

⚠️ **API contract NOT verified against live endpoint** (решение D-3).

Trading API: POST `/v1/quote` с телом `EXACT_INPUT`, заголовок `x-api-key`,
разбор `output.amount` и `gasUseEstimate`, рекурсивный сбор пулов.

**Ключевое:** Classic и семейство UniswapX сохраняются как **разные**
routing modes и не объединяются. Routing mode входит в identity маршрута,
поэтому смена режима даёт другой отпечаток и распознаётся Level 2 как
`MISMATCH`. Неизвестное значение `routing` отклоняется, а не подменяется.

`HttpProviderAdapter` дополнен поддержкой метода и тела запроса.

**`scripts/verify_provider_api.py`** — реальная проверка контрактов
провайдерских API: вызывает те же адаптеры, что и приложение, не выполняет
свопов, запускается в среде с сетевым доступом и ключами. Именно этот
скрипт закрывает ограничение решения D-3.

**Тестирование:** `pytest` ✅ **1657 passed**; `ruff` ✅ · `ruff format` ✅ ·
`mypy --strict` ✅ (151 модуль). Все четыре адаптера проходят общий
contract suite.

---

### S10 — Fee System, Gas System, Prices/Conversion ✅

Решение **D-4**: источники gas и conversion rate подключаются через независимые
абстракции и заменяются без изменения бизнес-логики Profit Calculator.

**Fee System (`monik/services/fees/`):**
- `FeeContext` — ключ комиссии: провайдер, сеть, операция, пара токенов,
  отпечаток маршрута и сумма входа; отдельный `cache_key()` без суммы,
  чтобы не обобщать сверх необходимого и не дробить кэш;
- `FeePolicy` (protocol) и реализации: `QuoteInclusiveFeePolicy` (комиссия уже
  учтена в котировке → `CostInclusion.INCLUDED_IN_QUOTE`, дополнительно
  вычитать нечего), `PercentageFeePolicy` (база процента задаётся явно),
  `UnknownFeePolicy` (статус `UNKNOWN`, суммы нет);
- `FeeService` — снимки с версией правил (`FEE_RULES_VERSION`), свежесть и
  переиспользование снимка, объединение одновременных одинаковых запросов
  через `InFlightRegistry`, группировка дубликатов в `refresh()`,
  опциональное сохранение через `SqliteFeeRepository`.
  **Провайдер без зарегистрированной policy даёт `UNKNOWN`, а не ноль.**

**Gas System (`monik/services/gas/`):**
- `GasPriceProvider` (protocol); `RpcGasPriceProvider` — EIP-1559 через
  `eth_feeHistory` (base fee + priority fee) с fallback на `eth_gasPrice`,
  запрос идёт **через Resource Manager** (владелец ресурса `rpc`);
  `StaticGasPriceProvider` — **test implementation**;
- `GasEstimator` — `cost = gas_units × wei_per_gas / 10^18` в точной
  арифметике `Decimal`; отсутствие units, цены или native token даёт
  `FeeStatus.UNKNOWN`, а не ноль.

**Prices (`monik/services/prices/`):**
- `TokenPriceProvider` (protocol); `AggregatorQuotePriceProvider` — курс из
  исполнимой котировки уже подключённого агрегатора; `HttpPriceProvider` —
  внешний сервис задаётся конфигурацией, binary float в ответе отклоняется,
  запрос через Resource Manager (владелец `prices`); `StaticPriceProvider` —
  **test implementation**;
- `ConversionService` — кэш с учётом свежести, последовательный перебор
  источников, **явное направление** конверсии (неявная инверсия запрещена),
  отказ использовать устаревший курс.

`ResourceKey.provider_id` расширен до `ProviderId | str`: через Resource
Manager проходят также не-агрегаторные владельцы (RPC, price API) — `01 §34`.

**Тестирование:** `pytest` ✅ **1730 passed**; `ruff` ✅ · `ruff format` ✅ ·
`mypy --strict` ✅ (158 модулей).

---

### S11 — Profit Calculator ✅

**Единственный владелец финансовых формул Monik** (`09 §2, §30`): Level 1,
Level 2, Telegram и история собственных формул не содержат.

**Реализовано (`monik/services/calculator/`):**
- `precision.py` — фиксированный decimal-контекст (`prec=50`,
  `ROUND_HALF_EVEN`, ловушки арифметических сбоев). Результат не зависит от
  process-wide контекста, поэтому расчёт детерминирован (`09 §49, §71`);
  промежуточные значения не округляются (`09 §39-40`);
- `conversion.py` — `RateBook`: курс выбирается строго по заданному
  направлению (`09 §38`) и только свежий (`09 §36`); совпадающие валюты
  курса не требуют (`09 §34`); отсутствие курса даёт `None`, а не
  выдуманное значение (`09 §37`);
- `costs.py` — `CostBreakdown` из комиссий и gas: rebate отдельным
  компонентом (`09 §15`), `included_in_quote` исключает двойной учёт
  (`09 §44-46`), неизвестный или просроченный расход попадает в
  `unknown_components` и никогда не заменяется нулём (`09 §16, §63`);
- `threshold.py` — сравнение `>=` (`09 §26`); неизвестный расход, влияющий
  на метрику, не позволяет считать порог пройденным (`09 §27`);
- `profit.py` — `ProfitCalculator.calculate()`: gross/net profit и ROI,
  статусы `COMPLETE/PARTIAL/INVALID/UNKNOWN`, versioned formula.
  Противоречивые данные дают `INVALID` с явной причиной, а не молчаливое
  исправление (`09 §20, §73`).

**Доменные модели:** `Gas.inclusion` (gas, уже учтённый в исходном
значении, повторно не вычитается — `09 §46`); `ProfitResult.invalid_reason`
(причина `INVALID` фиксируется явно — `09 §73`).

**Тестирование:** `pytest` ✅ **2120 passed**; `ruff` ✅ · `ruff format` ✅ ·
`mypy --strict` ✅.

Architecture-тесты: финансовая арифметика и сравнение порога прибыльности
существуют **только** в модуле Calculator; сам Calculator не выполняет I/O
(`09 §74-76`).

---

### S12 — Level 1 Scanner ✅

**Реализовано (`monik/services/level1/`, 12 модулей):**
- `ports.py` — узкие протоколы окружения (Fee System, gas, курсы,
  хранилища, приёмник Level 2): Scanner не знает их реализаций;
- `scope.py` — границы цикла целиком из конфигурации и реестров
  (`02 §5, §68`); списки сетей, токенов, сумм и провайдеров в коде не зашиты;
- `filters.py` — capability-фильтрация **до** отправки запроса
  (`10 §15`, `02 §76`); `UNKNOWN` не приравнивается к `UNSUPPORTED` и
  допускает runtime-проверку, если это разрешено конфигурацией (`10 §16`);
- `validation.py` — провайдер, сеть, токены, сумма, статус, нулевой output
  и свежесть; невалидная котировка в сравнении не участвует (`10 §41`);
- `quotes.py` — запросы только через Adapter (а тот — через Resource
  Manager), ограниченная конкурентность (`02 §60`), диагностика каждой
  попытки;
- `cycle.py` — **самодостаточный цикл одного токена**: MAX BUY определяется
  после получения набора BUY-ответов, затем немедленно запускается SELL,
  не дожидаясь BUY других токенов (`CLAUDE.md §16`, `10 §75`);
- `preliminary.py` — сборка входа расчёта (комиссии обеих ног, gas
  round-trip, курс native token) и вызов `ProfitCalculator`; собственной
  формулы нет (`10 §46`);
- `grouping.py` — суммы объединяются в одну Opportunity только при
  совпадении пары провайдеров и обоих маршрутов: **один маршрут на все
  суммы** (`10 §24, §54, §89`);
- `ranking.py` / `dedup.py` — детерминированное ранжирование при нехватке
  ёмкости (`02 §49-50`) и дедупликация по отпечатку в окне (`02 §44`);
- `handoff.py` — **атомарное** создание Opportunity + Level 2 Job и
  немедленная передача (`CLAUDE.md §29`, `02 §46`);
- `scanner.py` — оркестрация: параллельные независимые токены, общий
  таймаут, изоляция ошибок, backpressure, статусы
  `COMPLETE/PARTIAL/FAILED/CANCELLED`.

Отпечаток Opportunity вынесен в функцию `opportunity_fingerprint`: значение
для дедупликации до создания и хранимое значение вычисляются одним кодом.

**Тестирование:** `pytest` ✅ **2310 passed**; `ruff` ✅ · `ruff format` ✅ ·
`mypy --strict` ✅ (176 модулей).

Component-тесты цикла: фильтрация token/provider/capability, несколько сумм,
один маршрут на все суммы, порог, неизвестные fee/gas/курс, дедупликация и
её окно, backpressure, лимит на цикл, изоляция ошибок провайдера, rate
limit, нулевой output, устаревшая котировка, отмена, expiration.
Отдельно проверено: **SELL токена A не ждёт BUY токена B**, ограниченная
конкурентность и детерминизм результата.
Architecture-тесты: Level 1 не обходит Adapter/Resource Manager, не
отправляет уведомления, не создаёт собственный таймер и не зашивает
параметры сканирования.

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
| S5 | `238aaeb` | `docs: update development status after stage S5` |
| S6 | `f7e73e9` | `feat: add token, network, provider and capability registries` |
| S6 | `61eec08` | `docs: update development status after stage S6` |
| S7 | `03b8997` | `feat: add controlled async http client with ssrf and tls safeguards` |
| S7 | `b687649` | `docs: update development status after stage S7` |
| S8 | `ccca655` | `feat: implement resource manager with priorities, rate limits, retry and circuit breaker` |
| S8 | `cd8facf` | `docs: update development status after stage S8` |
| S9.0 | `a835438` | `feat: add aggregator adapter contract and shared contract test suite` |
| S9.1 | `f0d62fc` | `feat: implement 1inch adapter` |
| S9.1 | `0021a38` | `docs: update development status after stages S9.0 and S9.1` |
| S9.2 | `ab4dcfc` | `feat: implement 0x adapter` |
| S9.3 | `702e5c5` | `feat: implement velora adapter` |
| S9.4 | `66311ff` | `feat: implement uniswap adapter and provider api verification script` |
| S9.4 | `75c5e75` | `docs: update development status after stages S9.2-S9.4` |
| S10 | `425e1fc` | `feat: implement fee system, gas providers and price conversion` |
| S10 | `ddf4b6f` | `docs: update development status after stage S10` |
| S11 | `cee04fc` | `feat: implement deterministic profit calculator with decimal arithmetic` |
| S12 | `0536965` | `feat: implement level 1 scanner with independent per-token buy/sell cycles` |

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
| S6 | Token/Network/Provider/Capability registries | ✅ |
| S7 | HTTP infrastructure (TLS, SSRF, limits) | ✅ |
| S8 | Resource Manager | ✅ |
| S9.0 | Adapter contract + contract test suite + FakeAdapter | ✅ |
| S9.1 | 1inch adapter | ✅ |
| S9.2 | 0x adapter | ✅ |
| S9.3 | Velora adapter | ✅ |
| S9.4 | Uniswap adapter | ✅ |
| S10 | Fee System, Gas System, conversion | ✅ |
| S11 | Profit Calculator | ✅ |
| S12 | Level 1 Scanner | ✅ |
| S13 | Level 2 Scanner | 🔜 следующий |
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

**S13 — Level 2 Scanner** согласно `DEVELOPMENT_PLAN.md` §5.

Ключевое правило этапа: **Level 2 проверяет именно тот маршрут, который
зафиксировал Level 1** (`11 §5`, `10 §31`). Он не ищет новый маршрут, не
выбирает другой пул и не меняет routing mode; невозможность воспроизвести
маршрут — это `ROUTE_UNAVAILABLE`, а не `UNPROFITABLE`.

Что нужно сделать (`monik/services/level2/`):
- воркер Job: `QUEUED → RUNNING → {CONFIRMED, REJECTED, FAILED, EXPIRED,
  CANCELLED}`; `max_parallel` по умолчанию 20 и никогда не превышается
  (`CLAUDE.md` §18); логические Job отделены от resource locks;
- дедупликация одинаковых workflow (`CLAUDE.md` §19);
- свежие BUY-котировки по фиксированному маршруту через
  `validate_fixed_route`; **SELL считается от текущего BUY output**, а не от
  значения Level 1 (`11 §16-17`);
- комиссии, gas и conversion для каждой суммы отдельно; расчёт через
  `ProfitCalculator`; статусы подтверждения `CONFIRMED/UNCONFIRMED/PARTIAL`
  (`CLAUDE.md` §26) и confirmation rate без `PARTIAL` (`CLAUDE.md` §27);
- прерванная попытка после аварии становится `INTERRUPTED`, старые
  котировки свежими не считаются (`CLAUDE.md` §30).

Готово для этапа: `Level2Job`/`Level2Attempt`/`AmountVerificationResult`/
`ConfirmationResult`, `SqliteJobRepository`, `RouteValidation` во всех
четырёх адаптерах, `ProfitCalculator`, Fee/Gas/Conversion, Resource Manager
с приоритетом `LEVEL2` и дедупликацией, порт `Level2Dispatcher` из Level 1.
