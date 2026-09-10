# SQL Test Cases

| ID | Scenario | Expected Result | Status |
|---|---|---|---|
| TC-SQL-001 | Retrieve all movie records | 14 movie records returned | PASS |
| TC-SQL-002 | Retrieve title and year only | Only title and year returned | NOT EXECUTED / NOT VERIFIED |
| TC-SQL-003 | Find Toy Story by title | One Toy Story record returned | PASS |
| TC-SQL-004 | Movies released after 2010 | 3 records returned | PASS |
| TC-SQL-005 | Movies by John Lasseter | 5 records returned | PASS |
| TC-SQL-006 | Movies longer than 100 minutes | Only length > 100 returned | PASS |
| TC-SQL-007 | Year > 2005 AND length > 110 | Cars, Ratatouille, Cars 2 returned | PASS |
| TC-SQL-008 | John Lasseter OR Brad Bird | Records for either director returned | PASS |
| TC-SQL-009 | Movies from 2000 through 2010 | Only inclusive range returned | PASS |
| TC-SQL-010 | Sort by year descending | Newest movies first | PASS |
| TC-SQL-011 | Count movie records | COUNT(*) = 14 | PASS |
| TC-SQL-012 | Count movies by director | Correct aggregate rows returned | PASS |
| TC-SQL-013 | JOIN title with rating | Related titles and ratings returned | PASS |
| TC-SQL-014 | JOIN title with domestic sales | Related titles and sales returned | PASS |
| TC-SQL-015 | Employees with missing building | Only building IS NULL returned | PASS |
| TC-SQL-016 | Employees with assigned building | Only building IS NOT NULL returned | PASS |

## Note
TC-SQL-002 is deliberately not marked PASS because the requested result was not independently confirmed.
