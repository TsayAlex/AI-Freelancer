# SauceDemo Manual QA Test Report

## Test Information

| Field | Value |
|---|---|
| Project | SauceDemo E-commerce Testing |
| Application | SauceDemo |
| Test Type | Manual Black-box Testing |
| Tester | Alexei |
| Total Test Cases | 15 |
| Passed | 14 |
| Failed | 1 |
| Blocked | 0 |
| Not Tested | 0 |
| Pass Rate | 93.3% |
| Overall Result | FAIL |

---

# Executive Summary

Manual black-box testing was performed on the SauceDemo e-commerce application.

The main user journey was tested, including:

- Login
- Product catalogue
- Product sorting
- Shopping cart
- Adding multiple products
- Removing products
- Checkout validation
- Successful purchase
- Logout
- Reset App State
- Keyboard navigation

A total of **15 test cases** were executed.

**14 test cases passed and 1 test case failed.**

The overall pass rate was **93.3%**.

One accessibility/usability issue was identified during keyboard navigation.

---

# Test Execution Summary

| Status | Count |
|---|---:|
| Passed | 14 |
| Failed | 1 |
| Blocked | 0 |
| Not Tested | 0 |
| **Total** | **15** |

**Pass Rate: 93.3%**

---

# Defect Summary

| ID | Test Case | Area | Result |
|---|---|---|---|
| BUG-004 | TC-015 | Keyboard Navigation / Accessibility | Failed |

---

# BUG-004 — Login button is skipped during keyboard navigation

## Area

Accessibility / Usability

## Related Test Case

**TC-015 — Keyboard Navigation**

## Expected Result

Interactive elements should be reachable in a logical order using the **Tab** key.

The Login button should receive visible keyboard focus and should be possible to activate using the keyboard.

## Actual Result

During manual keyboard navigation, focus does not move to the Login button in the expected Tab sequence.

The focus moves to other interactive elements instead.

## Impact

Users who rely on keyboard navigation may have difficulty reaching and activating the Login button using the expected Tab navigation sequence.

## Evidence

Screenshot:

![BUG-004 — Login button skipped during keyboard navigation](evidence/BUG-004.png)

Evidence file:

`evidence/BUG-004.png`

Detailed bug report:

`evidence/BUG-004.md`

## Recommendation

Review the keyboard focus behaviour and tab order of the Login page.

Ensure that the Login button is keyboard-focusable and appears in a logical navigation sequence.

**Bug Status:** Open

---

# Final Assessment

## Overall QA Status: FAIL

The application successfully passed **14 of 15** executed test cases.

The core e-commerce workflow — login, product selection, cart operations, checkout and successful purchase — worked during the manual test session.

However, **TC-015 — Keyboard Navigation** failed because of the observed keyboard accessibility issue documented as **BUG-004**.

### Final statistics

**15 Test Cases**

**14 Passed**

**1 Failed**

**93.3% Pass Rate**

---

# Testing Artifacts

The project contains the following QA documentation:

- `QA_CHECKLIST.md` — manual test cases and execution results
- `SAUCEDEMO_QA_REPORT.md` — final manual QA report
- `evidence/BUG-004.md` — detailed bug report
- `evidence/BUG-004.png` — screenshot evidence

---

# Skills Demonstrated

This project demonstrates practical experience with:

- Manual QA testing
- Black-box testing
- Functional testing
- Negative testing
- End-to-end testing
- Accessibility and usability testing
- Test case design
- Test execution
- Bug reporting
- Screenshot evidence collection
- QA documentation
- Markdown
- Git / GitHub workflow

---

*Portfolio QA project.*