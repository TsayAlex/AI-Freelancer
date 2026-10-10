# QA Portfolio | Projects 9–10 — Game Regression Lab + Release Gate
# Портфолио QA | Проекты 9–10 — Регрессионные тесты игр + Контроль выпуска

**Date / Дата:** 2026-10-09
**System / Система:** QA Factory v1.3, Python, Playwright, Chromium, Node.js.

## Goal / Цель
**EN:** Build reproducible regression QA for existing offline games and a conservative evidence-based release decision engine.
**RU:** Создать повторяемые регрессионные тесты существующих офлайн-игр и строгую систему решения о выпуске на основе доказательств.

## Test targets / Объекты тестирования
- Chess4 v8.3 original / Шахматы v8.3 исходные.
- Chess4 v8.3.1 language fix / Шахматы v8.3.1 с исправлением языка.
- Aquarium v9 Art Studio / Аквариум v9.
- Fighting Legends v19 Real3D / Боевые легенды v19.
- 10 repaired release ZIPs for websites / 10 исправленных ZIP сайтов.

## Actual results / Фактические результаты
| Category / Категория | Result / Результат |
|---|---|
| Project ZIPs scanned / ZIP проверено | **14** |
| Game/browser assertions PASS / Игровые проверки PASS | **78** |
| Game/browser assertions FAIL / Ошибки в проверках | **2** — original Chess4 v8.3 language changes / исходная v8.3, смена языка |
| NOT_RUN / Не проверено | **4** — GPU 3D/audio perception / аппаратный 3D/качество звука на слух |
| Release gate BLOCKED / Выпуск заблокирован | **1** — Chess4 v8.3 |
| Release gate HOLD_FOR_REVIEW / Нужна проверка | **13** |
| Release gate READY_FOR_STAGING / Готово к тестовому стенду | **0** |
| Automated unit/integration tests / Внутренние тесты | **28/28 PASS** |

## Reproduced defect / Воспроизведённая ошибка
**EN:** Chess4 v8.3 throws "Cannot set properties of null (setting 'textContent')" during language changes. Reproduced on desktop and mobile in offline Chromium. The corrected ZIP v8.3.1 passed the same language scenarios with zero uncaught exceptions.
**RU:** Chess4 v8.3 при смене языка выбрасывает исключение `Cannot set properties of null (setting 'textContent')`. Воспроизведено на ПК и телефоне в офлайн-Chromium. Исправленный ZIP v8.3.1 прошёл те же языковые сценарии без необработанных исключений.

## Scope / Ограничения
**EN:** Tests run client-side code in isolated offline Chromium. They cannot guarantee WebGL hardware rendering, music quality, production deployment or full gameplay coverage. Static findings are candidates, not confirmed defects.
**RU:** Проверки выполняли клиентский код в изолированном офлайн-Chromium. Они не доказывают качество аппаратного WebGL, музыки, боевой публикации или полного игрового процесса. Статические предупреждения — кандидаты, а не подтверждённые баги.

## Commercial relevance / Коммерческое применение
**EN:** Repeatable ZIP intake → static evidence → optional functional browser tests → reviewed release decision → customer documentation pack.
**RU:** Повторяемая цепочка: приём ZIP → статические доказательства → при необходимости браузерные тесты → решение о выпуске после проверки → пакет документов для клиента.

**Privacy / Конфиденциальность:** The repository case study should NOT include owner or client source ZIPs, uploaded personal contact data or private screenshots without review. / В публичном репозитории нельзя размещать исходные ZIP клиентов, персональные данные и приватные скриншоты без проверки.
