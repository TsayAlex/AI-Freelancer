# Mobile Testing Checklist

| ID | Check | Expected Result | Status |
|---|---|---|---|
| MOB-001 | Open SauceDemo on mobile | Login page renders correctly | PASS |
| MOB-002 | Mobile keyboard interaction | Keyboard does not block critical controls | NOT TESTED |
| MOB-003 | Login with valid credentials | Products page opens correctly | PASS |
| MOB-004 | Scroll product content | Page scrolls without broken layout | PASS |
| MOB-005 | Add product to cart | Cart badge displays 1 | PASS |
| MOB-006 | Open cart | Added product is displayed | PASS |
| MOB-007 | Rotate portrait → landscape | Layout remains usable and cart state persists | PASS |
| MOB-008 | Open product sorting menu | Sorting options remain accessible | PASS |
| MOB-009 | Open checkout form | Checkout information form is displayed | PASS |
| MOB-010 | Submit completely empty checkout form | Required-field validation prevents progress | PASS |
| MOB-011 | Submit without Last Name | Last Name required error is displayed | PASS |
| MOB-012 | Submit without Postal Code | Postal Code required error is displayed | PASS |
| MOB-013 | Submit valid checkout information | Checkout Overview opens | PASS |
| MOB-014 | Finish checkout | Order confirmation is displayed | PASS |

## Summary
Executed: 13  
Passed: 13  
Failed: 0  
Not Tested: 1

Additional exploratory observations are documented separately in `INVESTIGATION_NOTES.md`.
