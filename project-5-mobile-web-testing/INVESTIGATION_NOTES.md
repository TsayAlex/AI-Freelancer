# Investigation Notes

## FINDING-001 — Blank Page During Checkout Input

### Observation
While browser translation was enabled, entering data into the checkout form repeatedly resulted in a blank white page.

### Initial Reproduction
The behavior was observed multiple times during the translated-page scenario.

### Isolation Test
Browser translation was disabled and the same checkout input flow was repeated.

### Result
The checkout form worked correctly without browser translation.

### Assessment
The behavior is environment-dependent.

It is **not confirmed as a SauceDemo application defect**, because removing browser translation changed the result.

**Status:** Needs environment-specific investigation.

---

## FINDING-002 — Authentication Lost on Finish

### Observation
During one checkout attempt, tapping Finish redirected the user to the Login page.

Displayed message:

`Epic sadface: You can only access '/checkout-complete.html' when you are logged in.`

### Expected
Checkout Complete page should open.

### Retest
The complete purchase flow was repeated.

### Retest Result
PASS — Checkout Complete page was displayed successfully.

### Reproducibility
Once.

### Assessment
Intermittent observation. Root cause was not established.

**Status:** Needs further investigation.

---

## QA Note
No root cause is claimed for either observation. Both findings are documented according to observed behavior and retest evidence only.
