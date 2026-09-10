# 🧪 AI-Freelancer QA Portfolio

**Manual Software Testing • REST API Testing • Postman • SQL & Database Testing • QA Automation • Playwright • JavaScript • GitHub Actions • Bug Reporting • Evidence Collection**

A practical QA portfolio demonstrating entry-level Quality Assurance skills through **manual software testing**, **REST API testing**, **SQL/database testing**, and **browser test automation**.

The portfolio includes test planning, test case design, bug reporting, evidence collection, API validation, SQL query validation, Playwright automation, automated reporting, Git version control, and a verified GitHub Actions CI workflow.

This repository contains **four QA portfolio projects**:

1. 🤖 **Automated QA Testing** — Playwright automation against a deliberately broken website.
2. 🛒 **SauceDemo Manual QA Testing** — manual black-box testing of an e-commerce application.
3. 🔌 **REST API Testing with Postman** — manual testing of the JSONPlaceholder REST API.
4. 🗄️ **SQL & Database Testing** — practical SQL query testing with documented test cases and evidence.

---

# 🤖 Project 1 — Automated QA Testing

## Overview

Automated black-box testing using **Playwright** against a deliberately broken website.

The workflow:

- Executes browser tests.
- Detects observable defects.
- Captures screenshot evidence.
- Generates Markdown and HTML QA reports.
- Supports local execution and GitHub Actions CI.

## Technologies

| Technology | Purpose |
|---|---|
| JavaScript | Test logic and report-generation logic |
| Node.js | JavaScript runtime |
| Playwright | Browser automation and black-box testing |
| PowerShell | Local one-command QA workflow |
| GitHub Actions | Continuous Integration workflow |
| Markdown | Structured QA documentation |
| HTML/CSS | Visual QA reports |
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
Screenshot Evidence
   ↓
QA Reports
```

## Defects Detected

| ID | Area | Severity | Finding |
|---|---|---|---|
| BUG-001 | Navigation | Major | About page missing |
| BUG-002 | Navigation | Major | Broken navigation link |
| BUG-003 | Registration | Major | Invalid email accepted |

## Results

| Metric | Result |
|---|---:|
| Issues Found | 3 |
| Major Bugs | 3 |
| Tested Website | **FAIL** |
| Automation Workflow | ✅ PASS |
| GitHub Actions CI | ✅ PASS / Working |

> **Important:** the **FAIL** status belongs to the intentionally broken test website, not to the automation workflow.

## Run Locally

From the project root in PowerShell:

```powershell
.\run-qa.ps1
```

The workflow runs the Playwright tests, captures evidence, saves test output, and generates QA reports.

Generated reports:

```text
QA_TEST_REPORT.md
QA_TEST_REPORT.html
```

---

# 🛒 Project 2 — SauceDemo Manual QA Testing

## Overview

Manual black-box testing of the **SauceDemo** e-commerce application.

The test set covers the main customer journey together with positive, negative, validation, usability, and accessibility scenarios.

## Test Coverage

- Login validation
- Locked-out user
- Invalid credentials
- Product catalogue
- Product sorting
- Shopping cart
- Checkout validation
- Successful purchase
- Logout
- Reset App State
- Keyboard accessibility

## Manual QA Results

| Metric | Result |
|---|---:|
| Total Test Cases | 15 |
| Passed | 14 |
| Failed | 1 |
| Blocked | 0 |
| Not Tested | 0 |
| Pass Rate | **93.3%** |
| Overall Result | **FAIL** |

## Bug Found

| ID | Severity | Description |
|---|---|---|
| BUG-004 | Minor | Login button skipped during keyboard Tab navigation |

## Documentation

- `QA_CHECKLIST.md` — manual test cases and execution results
- `SAUCEDEMO_QA_REPORT.md` — final manual QA report
- `evidence/BUG-004.md` — detailed bug report
- `evidence/BUG-004.png` — screenshot evidence

---

# 🔌 Project 3 — REST API Testing with Postman

## Overview

Manual REST API testing using **Postman** against the public **JSONPlaceholder REST API**.

This project demonstrates practical API testing skills relevant to Junior QA and Manual QA roles.

## HTTP Methods Tested

- GET
- POST
- PUT
- PATCH
- DELETE

## API Test Coverage

- Retrieve all posts.
- Retrieve a specific resource.
- Retrieve a non-existing resource.
- Create a resource.
- Create an empty resource.
- Update a resource.
- Partially update a resource.
- Delete a resource.
- Filter resources using query parameters.
- Execute a negative filtering scenario.

## Test Results

| Metric | Result |
|---|---:|
| Total Test Cases | **10** |
| Passed | **10** |
| Failed | **0** |
| Blocked | **0** |
| Pass Rate | **100%** |
| Overall Result | **PASS** |

## HTTP Status Codes Verified

| Status | Meaning |
|---|---|
| **200 OK** | Resource retrieved or updated successfully |
| **201 Created** | Resource created successfully |
| **404 Not Found** | Non-existing resource handled correctly |

## Project Documentation

```text
project-3-api-testing/
├── TEST_PLAN.md
├── API_TEST_CASES.md
├── API_TEST_REPORT.md
└── README.md
```

## Skills Demonstrated

- REST API Testing
- Postman
- HTTP Methods
- JSON Validation
- Request / Response Validation
- Query Parameter Testing
- Positive Testing
- Negative Testing
- API Test Case Design
- QA Documentation

**Result:** ✅ **10 / 10 Test Cases Passed (100%)**

---

# 🗄️ Project 4 — SQL & Database Testing

## Overview

Practical SQL and database-testing project based on executed SQLBolt exercises.

The project demonstrates the ability to retrieve, filter, sort, aggregate, group, and combine relational data while documenting test cases, SQL queries, execution results, and screenshot evidence.

## SQL Coverage

- SELECT and column selection
- WHERE filtering
- Comparison operators
- AND / OR conditions
- BETWEEN
- ORDER BY
- COUNT(*)
- GROUP BY
- JOIN across related tables
- IS NULL
- IS NOT NULL

## SQL Test Results

| Metric | Result |
|---|---:|
| Documented Test Cases | **16** |
| Confirmed Passed | **15** |
| Failed | **0** |
| Not Verified | **1 (TC-SQL-002)** |
| Evidence Screenshots | **14** |
| Overall Project Status | ✅ Completed with one explicitly unverified case |

> **QA note:** TC-SQL-002 is intentionally marked **NOT VERIFIED** because a separate execution result was not captured. This keeps the portfolio evidence-based and avoids claiming an unverified PASS.

## Project Documentation

```text
project-4-sql-database-testing/
├── README.md
├── TEST_PLAN.md
├── SQL_TEST_CASES.md
├── SQL_QUERIES.sql
├── SQL_TEST_REPORT.md
└── evidence/
    ├── README.md
    ├── TC-SQL-003.jpg
    ├── ...
    └── TC-SQL-016.jpg
```

## Skills Demonstrated

- SQL
- Relational Data
- SELECT / WHERE
- AND / OR
- BETWEEN
- ORDER BY
- COUNT
- GROUP BY
- JOIN
- NULL Validation
- Query Result Verification
- SQL Test Case Design
- Evidence-Based QA Documentation

---

# 📸 Evidence

The repository contains screenshot evidence and detailed QA documentation.

```text
evidence/
├── BUG-001.png
├── BUG-002.png
├── BUG-003.png
├── BUG-004.png
└── BUG-004.md

project-4-sql-database-testing/evidence/
├── README.md
├── TC-SQL-003.jpg
├── ...
└── TC-SQL-016.jpg
```

**BUG-001 to BUG-003** belong to the automated broken-site project.  
**BUG-004** belongs to the SauceDemo manual QA project.  
**TC-SQL-003 to TC-SQL-016** document SQL/database testing evidence.

---

# 📁 Project Structure

```text
AI-Freelancer/
├── .github/
│   └── workflows/
│       └── qa.yml
├── broken-site/
│   ├── app.js
│   ├── index.html
│   └── styles.css
├── evidence/
│   ├── BUG-001.png
│   ├── BUG-002.png
│   ├── BUG-003.png
│   ├── BUG-004.png
│   └── BUG-004.md
├── project-2-saucedemo/
├── project-3-api-testing/
│   ├── TEST_PLAN.md
│   ├── API_TEST_CASES.md
│   ├── API_TEST_REPORT.md
│   └── README.md
├── project-4-sql-database-testing/
│   ├── README.md
│   ├── TEST_PLAN.md
│   ├── SQL_TEST_CASES.md
│   ├── SQL_QUERIES.sql
│   ├── SQL_TEST_REPORT.md
│   └── evidence/
├── tests/
│   ├── broken-site.spec.js
│   ├── generate-report.js
│   └── smoke.spec.js
├── QA_CHECKLIST.md
├── QA_TEST_REPORT.md
├── QA_TEST_REPORT.html
├── SAUCEDEMO_QA_REPORT.md
├── README.md
├── run-qa.ps1
├── package.json
└── package-lock.json
```

---

# 💡 Skills Demonstrated

## Manual QA

- Black-box Testing
- Functional Testing
- End-to-End Testing
- Positive & Negative Testing
- Validation Testing
- Accessibility Testing
- Usability Testing
- Test Case Design
- Test Execution
- Bug Reporting
- Severity Assessment
- Evidence Collection
- QA Documentation

## API Testing

- REST API Testing
- Postman
- HTTP Methods
- Status Code Validation
- JSON Validation
- Request / Response Validation
- Query Parameters
- Positive & Negative API Testing
- API Test Case Design

## SQL / Database Testing

- SQL
- Relational Data
- SELECT
- WHERE
- AND / OR
- BETWEEN
- ORDER BY
- COUNT
- GROUP BY
- JOIN
- IS NULL / IS NOT NULL
- Query Result Verification

## QA Automation

- Playwright
- JavaScript
- Node.js
- Browser Automation
- Screenshot Capture
- Automated Defect Detection
- HTML Report Generation
- Markdown Report Generation
- PowerShell Automation

## CI / Tools

- Git
- GitHub
- GitHub Actions
- VS Code
- Postman
- Markdown

---

# 🎯 Portfolio Goal

This repository demonstrates practical QA skills relevant to entry-level roles such as:

- Junior QA Tester
- Manual QA Tester
- Junior Software Tester
- API Tester
- Junior QA / Database Tester
- QA Automation Trainee
- Software Test Engineer Intern

---

# 📌 Project Status

| Component | Status |
|---|---|
| Manual QA Testing | ✅ Completed |
| SauceDemo Testing | ✅ Completed |
| REST API Testing | ✅ Completed |
| Postman API Tests | ✅ 10/10 Passed |
| SQL & Database Testing | ✅ Completed |
| Playwright Automation | ✅ Working |
| Automated Bug Detection | ✅ Working |
| Screenshot Evidence | ✅ Working |
| Markdown Reports | ✅ Working |
| HTML Reports | ✅ Working |
| GitHub Actions CI | ✅ PASS / Working |
| Portfolio Documentation | ✅ Updated |

**Version: v3.0 — Manual QA + REST API + SQL Database Testing + Automation Portfolio**

---

# 👤 Author

## **Oleksii Tsai**

**Junior QA | Manual Testing | REST API & Postman | SQL | Playwright | AI & Digital Tools**

📍 **Longford, Ireland**

Transitioning into the digital sector with practical experience in:

- Manual QA Testing
- REST API Testing
- SQL / Database Testing
- QA Automation
- AI Tools
- Digital Design
- Website Testing
