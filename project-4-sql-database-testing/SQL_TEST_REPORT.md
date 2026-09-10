# SQL Database Testing — Final Test Report

## Summary
Read-only SQL validation was performed using SQLBolt sample tables. Coverage included retrieval, filtering, compound conditions, ranges, sorting, aggregation, JOINs and missing-data checks.

| Metric | Result |
|---|---:|
| Documented test cases | 16 |
| PASS | 15 |
| FAIL | 0 |
| Not executed / not independently verified | 1 |
| Confirmed executed pass rate | 100% (15/15) |

## Key Results
- Confirmed 14 Movies records with COUNT(*).
- Validated text and numeric filters.
- Combined conditions with AND and OR.
- Validated ranges with BETWEEN.
- Sorted data with ORDER BY DESC.
- Aggregated counts with GROUP BY.
- Validated Movies ↔ Boxoffice relationships with JOIN.
- Detected missing Building values with IS NULL and confirmed populated values with IS NOT NULL.

## Defects
No product defect is claimed. NULL rows demonstrate missing-data detection, but without a business requirement that Building is mandatory they should not be reported as defects.

## Overall Result
PASS for all 15 confirmed executed scenarios.
