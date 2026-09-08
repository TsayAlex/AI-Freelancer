# 🧪 AI-Freelancer QA Portfolio

[![QA Automation](https://github.com/TsayAlex/AI-Freelancer/actions/workflows/qa.yml/badge.svg)](https://github.com/TsayAlex/AI-Freelancer/actions/workflows/qa.yml)

**Manual Software Testing • QA Automation • Playwright • JavaScript • GitHub Actions • Bug Reporting • Evidence Collection**

A practical QA portfolio demonstrating both **Manual Software Testing** and **QA Automation** skills.

This repository contains two QA projects:

1. **Automated black-box testing** of a deliberately broken website.
2. **Manual black-box testing** of the SauceDemo e-commerce application.

---

# 🤖 Project 1 — Automated QA Testing

## Overview

This project demonstrates automated black-box testing using **Playwright**.

The QA workflow tests a deliberately broken local website, detects observable defects, captures evidence, saves the test output, and generates QA reports automatically.

## Technologies

| Technology | Purpose |
| --- | --- |
| JavaScript | Test and report-generation logic |
| Node.js | JavaScript runtime |
| Playwright | Browser automation and black-box testing |
| PowerShell | One-command local QA workflow |
| GitHub Actions | CI execution on push / pull request |
| Markdown | Structured QA documentation |
| HTML / CSS | Visual QA report/dashboard |
| VS Code | Development environment |

## QA Automation Pipeline

```text
Website
  ↓
Playwright
  ↓
Black-box Testing
  ↓
Defect Detection
  ↓
Severity Classification
  ↓
Screenshot Evidence
  ↓
QA Log
  ↓
Report Generator
  ↓
Markdown + HTML QA Reports
```

## Detected Defects

The automated test detected **3 Major defects**:

| ID | Area | Severity | Finding |
| --- | --- | --- | --- |
| BUG-001 | Navigation | Major | About link points to a missing page |
| BUG-002 | Navigation | Major | Missing Page link points to a missing page |
| BUG-003 | Registration | Major | Malformed email is accepted |

## Automated QA Result

| Metric | Result |
| --- | ---: |
| Total Issues | 3 |
| Critical | 0 |
| Major | 3 |
| Minor | 0 |
| Trivial | 0 |
| Tested Application Status | **FAIL** |
| QA Automation Workflow | **WORKING** |
| GitHub Actions / CI | **WORKING** |

> **Important:** `FAIL` describes the tested deliberately broken website. The QA automation workflow itself completes successfully.

## Run Locally

From the project root in PowerShell:

```powershell
.\run-qa.ps1
```

The workflow:

1. runs the Playwright black-box test;
2. captures supported defect evidence;
3. saves the QA execution log;
4. parses and deduplicates defects;
5. calculates severity totals;
6. determines the tested application's QA status;
7. generates `QA_TEST_REPORT.md`;
8. generates `QA_TEST_REPORT.html`.

## Run Playwright Directly

```powershell
npx playwright test tests/broken-site.spec.js --reporter=list
```

## Generate Reports Separately

```powershell
node .\tests\generate-report.js
```

Generated reports:

```text
QA_TEST_REPORT.md
QA_TEST_REPORT.html
```

---

# 🧑‍💻 Project 2 — SauceDemo Manual QA Testing

## Overview

Manual black-box testing was performed on the **SauceDemo** e-commerce application.

The test set covers the main customer journey and several negative, validation, usability, and accessibility scenarios.

## Areas Tested

- Login with valid credentials
- Invalid login behaviour
- Empty login fields
- Locked-out user behaviour
- Product catalogue
- Product sorting
- Add product to cart
- Add multiple products
- Remove product from cart
- Checkout with empty information
- Checkout without postal code
- Complete successful purchase
- Logout
- Reset App State
- Keyboard navigation

## Manual Test Results

| Metric | Result |
| --- | ---: |
| Total Test Cases | 15 |
| Passed | 14 |
| Failed | 1 |
| Blocked | 0 |
| Not Tested | 0 |
| Pass Rate | **93.3%** |
| Overall Result | **FAIL** |

## Manual Defect Found

| ID | Related Test | Area | Severity | Finding |
| --- | --- | --- | --- | --- |
| BUG-004 | TC-015 | Accessibility / Usability | Minor | Login button is skipped during expected keyboard Tab navigation |

### BUG-004 — Keyboard Navigation

**Expected:** keyboard focus should move through the login controls in a logical order, including the **Login** button.

**Actual:** during the observed manual test, focus moved through the Username and Password fields but did not move to the Login button in the expected Tab sequence.

**Status:** Open

Detailed bug report: [`evidence/BUG-004.md`](evidence/BUG-004.md)

Screenshot evidence:

![BUG-004 — Login button skipped during keyboard navigation](evidence/BUG-004.png)

## Manual QA Report

Full report: [`SAUCEDEMO_QA_REPORT.md`](SAUCEDEMO_QA_REPORT.md)

Manual execution results: [`QA_CHECKLIST.md`](QA_CHECKLIST.md)

---

# 📸 Evidence

The repository contains screenshot evidence for detected issues:

```text
evidence/
├── BUG-001.png
├── BUG-002.png
├── BUG-003.png
├── BUG-004.png
└── BUG-004.md
```

---

# 📁 Project Structure

```text
AI-Freelancer/
│
├── .github/
│   └── workflows/
│       └── qa.yml
│
├── broken-site/
│   ├── app.js
│   ├── index.html
│   └── styles.css
│
├── evidence/
│   ├── BUG-001.png
│   ├── BUG-002.png
│   ├── BUG-003.png
│   ├── BUG-004.png
│   └── BUG-004.md
│
├── project-2-saucedemo/
│   ├── BUG_REPORTS.md
│   ├── QA_CHECKLIST.md
│   ├── TEST_CASES.md
│   ├── TEST_PLAN.md
│   └── tests/
│
├── tests/
│   ├── broken-site.spec.js
│   ├── generate-report.js
│   └── smoke.spec.js
│
├── BUG_REPORT_TEMPLATE.md
├── CLIENT_DELIVERY_TEMPLATE.md
├── EXECUTION_PLAN.md
├── QA_CHECKLIST.md
├── QA_TEST_REPORT.md
├── QA_TEST_REPORT.html
├── SAUCEDEMO_QA_REPORT.md
├── README.md
├── run-qa.ps1
├── package.json
├── package-lock.json
└── .gitignore
```

---

# 💡 Skills Demonstrated

## Manual QA

- Black-box testing
- Functional testing
- Positive and negative testing
- End-to-end testing
- Validation testing
- Basic accessibility / usability testing
- Test case execution
- Expected vs Actual analysis
- Bug reporting
- Severity assessment
- Evidence collection
- QA documentation

## QA Automation

- Playwright
- JavaScript
- Node.js
- Browser automation
- Automated defect detection
- Screenshot evidence capture
- QA log processing
- Automated Markdown reporting
- Automated HTML reporting
- PowerShell workflow automation

## CI / Tools

- Git
- GitHub
- GitHub Actions
- VS Code
- Markdown

---

# 🎯 Portfolio Goal

This repository is a **portfolio demonstration**, not a production-scale QA framework.

It demonstrates practical entry-level QA skills relevant to roles such as:

- Junior QA Tester
- Manual QA Tester
- Junior Software Tester
- QA Automation Trainee
- Junior Automation QA
- Software Test Engineer Intern

---

# 📌 Project Status

| Component | Status |
| --- | --- |
| Manual QA | ✅ Completed |
| Playwright automation | ✅ Working |
| Automated defect detection | ✅ Working |
| Screenshot evidence | ✅ Working |
| Markdown QA report | ✅ Working |
| HTML QA report | ✅ Working |
| One-command workflow | ✅ Working |
| GitHub Actions / CI | ✅ Working |
| Portfolio documentation | ✅ Completed |

**Version: v1.5 — Manual QA + Automation Portfolio**

---

# 👤 Author

**Alexei**  
QA / Digital Technology Portfolio  
Ireland
