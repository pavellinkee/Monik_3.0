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
| Последний завершённый этап | **нет** (реализация не начиналась) |
| Текущий этап | **S-A: Аудит и планирование — ЗАВЕРШЁН** |
| Следующий этап | **S0 — Project Foundation** |
| Статус разработки | ⏸ **ОЖИДАНИЕ КОМАНДЫ ПОЛЬЗОВАТЕЛЯ «ПОЕХАЛИ»** |
| Строк production-кода | 0 |
| Тестов | 0 |

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

**Commits:** см. следующий раздел.

---

## GIT COMMITS

| Этап | Commit | Описание |
|---|---|---|
| S-A | (текущий) | `docs: add development plan and status tracking` |

---

## ЧТО ОСТАЛОСЬ РЕАЛИЗОВАТЬ

Все 26 этапов плана:

| Этап | Модуль | Статус |
|---|---|---|
| S0 | Project foundation, tooling, CI | ⬜ |
| S1 | Domain models, enums, value objects | ⬜ |
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

| # | Проблема | Статус |
|---|---|---|
| D-1 | Конфликт наименования `Candidate` / `Opportunity` между документами 10/11 и 02/30/35/36 | ⏳ **ожидает решения пользователя** (предложение в `DEVELOPMENT_PLAN.md` §9) |
| D-2 | Telegram-команды и кнопка `об` есть в `CLAUDE.md`, но не в `15_NOTIFICATION_SYSTEM` | ⏳ предложена трактовка как расширение |
| D-3 | Live-верификация провайдерских API невозможна (egress заблокирован, ключей нет) | ⏳ предложен обходной путь + скрипт верификации |
| D-4 | Не зафиксирован источник gas и conversion rate | ⏳ предложен default |
| D-5 | Идентичность Velora (ребрендинг ParaSwap) | ⏳ предложен `provider_id = "velora"` |

---

## СЛЕДУЮЩИЙ ШАГ

После команды пользователя **«ПОЕХАЛИ»**:
начать **S0 — Project Foundation** согласно `DEVELOPMENT_PLAN.md` §5.
