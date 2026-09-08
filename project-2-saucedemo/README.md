# 🧪 SauceDemo Manual QA Project

**Manual Black-Box Testing • Functional Testing • Negative Testing • End-to-End Testing • Accessibility Testing • Bug Reporting**

A practical manual QA portfolio project based on the SauceDemo e-commerce application.

---

## 📊 Test Results

| Metric | Result |
|---|---:|
| Total Test Cases | 15 |
| Passed | 14 |
| Failed | 1 |
| Blocked | 0 |
| Not Tested | 0 |
| Pass Rate | **93.3%** |
| Overall Result | **FAIL** |

> The overall result is **FAIL** because one executed test case identified a reproducible keyboard-navigation issue.

---

## 🎯 Scope

The manual test session covered the main e-commerce user journey and selected usability/accessibility behaviour:

- Login and invalid-login validation
- Locked-out user behaviour
- Product catalogue
- Product sorting
- Adding and removing products from the cart
- Multiple-product cart behaviour
- Checkout validation
- Successful purchase
- Logout
- Reset App State
- Keyboard navigation

---

## 🐞 Defect Found

### BUG-004 — Login button is skipped during keyboard navigation

**Related Test Case:** TC-015 — Keyboard Navigation  
**Severity:** Minor  
**Priority:** P2  
**Status:** Open

During keyboard-only navigation on the SauceDemo login page, the Login button was not reached in the expected Tab sequence.

**Expected:** Username → Password → Login  
**Actual:** Focus moves away from the login form instead of reaching the Login button in the expected sequence.

Screenshot evidence: [`../evidence/BUG-004.png`](../evidence/BUG-004.png)

Detailed bug report: [`../evidence/BUG-004.md`](../evidence/BUG-004.md)

---

## 📁 QA Documentation

| Document | Purpose |
|---|---|
| [TEST_PLAN.md](TEST_PLAN.md) | Testing scope, approach and objectives |
| [TEST_CASES.md](TEST_CASES.md) | Designed manual test cases |
| [QA_CHECKLIST.md](QA_CHECKLIST.md) | Test execution checklist |
| [BUG_REPORTS.md](BUG_REPORTS.md) | Defect documentation |
| [Final QA Report](../SAUCEDEMO_QA_REPORT.md) | Complete manual QA test report |
| [BUG-004 Detailed Report](../evidence/BUG-004.md) | Detailed defect report |
| [BUG-004 Screenshot](../evidence/BUG-004.png) | Screenshot evidence |

---

## 🧠 Testing Approach

This project uses a **manual black-box testing** approach.

**Test Case → User Action → Expected Result → Actual Result → Pass/Fail → Defect Evidence**

The project includes positive, negative, end-to-end, functional and basic accessibility/usability testing.

---

## 💡 Skills Demonstrated

- Manual QA testing
- Black-box and functional testing
- Positive and negative testing
- End-to-end testing
- Accessibility and usability observation
- Test planning and test case design
- Test execution
- Expected vs Actual analysis
- Bug reporting
- Severity and priority assessment
- Screenshot evidence collection
- QA documentation
- Git / GitHub workflow

---

## 📌 Project Status

| Component | Status |
|---|---|
| Test Plan | ✅ Completed |
| Test Cases | ✅ Completed |
| Manual Execution | ✅ Completed |
| Bug Report | ✅ Completed |
| Screenshot Evidence | ✅ Completed |
| Final QA Report | ✅ Completed |

**15 test cases • 14 passed • 1 failed • 93.3% pass rate**

---

## 👤 Portfolio Context

This is a **portfolio QA project** created to demonstrate practical entry-level manual software testing skills.

Relevant roles include **Junior QA Tester, Manual QA Tester, Junior Software Tester, QA Trainee, and Software Test Engineer Intern**.

**Author:** Alexei  
**Location:** Ireland

*Manual QA Portfolio Project*
