# 🧪 ALEX AI QA FACTORY v1.3 — RELEASE GATE + GAME LAB + CLIENT PORTAL
# 🧪 ALEX AI QA FACTORY v1.3 — КОНТРОЛЬ ВЫПУСКА + ИГРОВЫЕ ТЕСТЫ + КАБИНЕТ КЛИЕНТА

**EN:** This is a real offline-first Windows QA toolkit built on v1.2, not an online SaaS.
**RU:** Это настоящий локальный QA-инструментарий для Windows на основе v1.2, а не облачный SaaS.

## Quick start / Быстрый запуск

**EN:** Unzip the folder. Install Python 3.10+ and Node.js (recommended). Keep all files in one folder.
**RU:** Распакуй архив. Установи Python 3.10+ и Node.js (рекомендуется). Сохраняй файлы в одной папке.

**EN:** Run `RUN_ALL_TESTS_WINDOWS.bat` to verify the internal application tests.
**RU:** Запусти `RUN_ALL_TESTS_WINDOWS.bat`, чтобы проверить внутренние автотесты программы.

**EN:** For automatic static audits, put your own ZIP files into `QA_INBOX` and run `START_RELEASE_GATE_WINDOWS.bat`.
**RU:** Для автоматического статического аудита помести свои ZIP в `QA_INBOX` и запусти `START_RELEASE_GATE_WINDOWS.bat`.

**EN:** Open `QA_RESULTS/OPEN_RELEASE_MATRIX.html` to see BLOCKED / HOLD_FOR_REVIEW / READY_FOR_STAGING decisions.
**RU:** Открой `QA_RESULTS/OPEN_RELEASE_MATRIX.html`, чтобы увидеть решения: ЗАБЛОКИРОВАНО / НУЖНА ПРОВЕРКА / ГОТОВО К ТЕСТОВОМУ РАЗВЁРТЫВАНИЮ.

**EN:** For browser game testing on trusted game ZIP files, install Chromium and run `TEST_GAMES_WINDOWS.bat` (opt-in only).
**RU:** Для браузерного тестирования своих проверенных игровых ZIP установи Chromium и запусти `TEST_GAMES_WINDOWS.bat` (только по явному выбору).

**EN:** For the private local customer intake, run `START_CLIENT_PORTAL_WINDOWS.bat` and open `http://127.0.0.1:8790`.
**RU:** Для приватного локального приёма заявок запусти `START_CLIENT_PORTAL_WINDOWS.bat` и открой `http://127.0.0.1:8790`.

**EN:** Stop any watcher or portal by closing its terminal window or pressing Ctrl+C.
**RU:** Останови наблюдение или кабинет закрытием окна терминала либо Ctrl+C.

## Product modules / Модули

| English | Русский | Script / Файл |
|---|---|---|
| ZIP Autopilot | Автоматический анализ ZIP | `qa_autopilot.py` |
| Game Regression Lab | Регрессионные тесты игр | `game_regression_lab.py` |
| Release Gate | Решение о выпуске | `release_gate.py` |
| Combined QA Pipeline | Полная цепочка QA | `qa_pipeline.py` |
| Private Client Portal | Приватный кабинет клиента | `client_portal.py` |
| Existing QA UI | Прежний QA-интерфейс | `START_WINDOWS.bat` |
| GitHub Actions template | Шаблон GitHub Actions | `.github/workflows/qa-release-gate.yml` |

## Real proof / Реальные доказательства

**EN:** The separate evidence package contains actual results for 14 owner-owned ZIPs: ten fixed sites, Aquarium v9, Fighting Legends v19, Chess4 v8.3 and patched Chess4 v8.3.1.
**RU:** Отдельный пакет доказательств содержит реальные результаты 14 собственных ZIP: десяти исправленных сайтов, Aquarium v9, Fighting Legends v19, Chess4 v8.3 и исправленной Chess4 v8.3.1.

**EN:** The v1.3 test run produced 78 passed game assertions, 2 failed and 4 explicitly not run (hardware/audio). Original Chess4 v8.3 caused exceptions; v8.3.1 did not.
**RU:** Проверка v1.3 дала 78 успешных игровых тестов, 2 неуспешных и 4 явно непроведённых (аппаратный 3D/звук на слух). Исходные шахматы v8.3 вызывали исключения; v8.3.1 — нет.

**EN:** Release Gate on these 14 ZIPs: 1 BLOCKED, 13 HOLD_FOR_REVIEW, 0 READY_FOR_STAGING. The ten sites passed their static audit with zero candidate findings, but lacked full live functional verification.
**RU:** Контроль выпуска на этих 14 ZIP: 1 ЗАБЛОКИРОВАН, 13 ТРЕБУЮТ ПРОВЕРКИ, 0 ДОПУЩЕНЫ К ТЕСТОВОМУ РАЗВЁРТЫВАНИЮ. Десять сайтов не дали статических предупреждений, но полного онлайн-тестирования ещё нет.

**EN:** The v1.3 unit/integration test suite passed 28/28. It includes an HTTP request → ZIP upload → local scan → report download workflow.
**RU:** Внутренние и интеграционные тесты v1.3 прошли 28/28, включая HTTP-заявку → ZIP → локальную проверку → скачивание отчёта.

## Release safety / Безопасность выпуска

**EN:** STATIC PASS does not prove working features. READY_FOR_STAGING is not permission for automatic public release.
**RU:** Успешная статическая проверка не доказывает исправность функций. READY_FOR_STAGING не является разрешением на автоматическую публичную публикацию.

**EN:** ZIP files are not automatically executed as programs. The game browser runs client-side JS only when you deliberately invoke the trusted-game option; external requests are blocked.
**RU:** ZIP не запускаются автоматически как программы. Игровой браузер исполняет клиентский JavaScript только по твоему явному выбору; внешняя сеть заблокирована.

**EN:** This prototype is bound to 127.0.0.1 and is NOT ready to be deployed to a public hosting platform. Never upload confidential customer ZIPs to a public GitHub repository.
**RU:** Прототип работает только на 127.0.0.1 и НЕ готов для публичного хостинга. Никогда не загружай конфиденциальные клиентские ZIP в открытый GitHub.

**EN:** GPU/WebGL rendering, natural sound quality, account sign-in, billing, secure multi-tenant hosting and real Netlify deployments remain outside verified scope.
**RU:** Аппаратный WebGL/3D, естественность музыки, авторизация, оплата, защищённый многоклиентский хостинг и реальные публикации Netlify пока не подтверждены.

## GitHub / GitHub

**EN:** The GitHub connector can read `TsayAlex/AI-Freelancer`, but write attempts returned `403 Resource not accessible by integration`. Nothing from this version was published automatically.
**RU:** Подключение GitHub читает `TsayAlex/AI-Freelancer`, но запись отклоняется ошибкой `403 Resource not accessible by integration`. Эта версия автоматически не опубликована.

**EN:** `GITHUB_READY` contains the publishable source (without customer ZIPs). You may commit it after reviewing the files, or use the local Git script if Git credentials are already configured.
**RU:** В `GITHUB_READY` находятся подготовленные исходники без клиентских ZIP. Их можно проверить и опубликовать через Git; локальный скрипт использует уже настроенный вход в GitHub.
