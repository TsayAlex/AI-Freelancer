# 🧪 API Testing — Test Plan

## 1. Project Overview

**Project:** REST API Testing Portfolio Project  
**Testing Type:** Manual API Testing  
**Tester:** Alexei  
**Environment:** Public Test API  
**Status:** In Progress

This project demonstrates practical API testing skills by testing REST API endpoints and validating responses, status codes, response bodies, and error handling.

---

## 2. Objectives

The objectives of this project are to:

- Test REST API endpoints manually
- Understand HTTP request methods
- Validate HTTP status codes
- Validate JSON response data
- Test positive and negative scenarios
- Check required parameters and request bodies
- Document test results
- Collect evidence
- Report defects if unexpected behaviour is found

---

## 3. Testing Scope

The following HTTP methods will be tested:

| Method | Purpose |
|---|---|
| GET | Retrieve data |
| POST | Create data |
| PUT | Update data |
| DELETE | Delete data |

Testing will include:

- Valid requests
- Invalid requests
- Response status codes
- JSON response structure
- Response values
- Required fields
- Invalid IDs
- Missing data
- Error handling
- Response time observation

---

## 4. Test Approach

Manual black-box API testing will be used.

Each test will follow this workflow:

**Request → Send → Response → Validate → Pass/Fail → Evidence**

For every test, the following will be checked:

1. HTTP method
2. Endpoint
3. Request parameters/body
4. HTTP status code
5. Response body
6. Expected result
7. Actual result
8. Test status

---

## 5. Planned Test Cases

| ID | Test Scenario | Type | Status |
|---|---|---|---|
| API-001 | Get list of resources | Positive | Not Tested |
| API-002 | Get single resource | Positive | Not Tested |
| API-003 | Request invalid resource ID | Negative | Not Tested |
| API-004 | Create new resource | Positive | Not Tested |
| API-005 | Create resource with invalid/missing data | Negative | Not Tested |
| API-006 | Update existing resource | Positive | Not Tested |
| API-007 | Update invalid resource | Negative | Not Tested |
| API-008 | Delete resource | Positive | Not Tested |
| API-009 | Test invalid endpoint | Negative | Not Tested |
| API-010 | Validate JSON response structure | Validation | Not Tested |

**Planned Test Cases: 10**

---

## 6. Entry Criteria

Testing can begin when:

- The API is available
- The API documentation is accessible
- The API testing tool is ready
- Test scenarios are defined

---

## 7. Exit Criteria

Testing is complete when:

- All planned test cases have been executed
- Actual results have been documented
- Pass/Fail status has been assigned
- Evidence has been collected
- Identified defects have been documented
- Final QA report has been prepared

---

## 8. Deliverables

The project will contain:

- `TEST_PLAN.md`
- `API_TEST_CASES.md`
- `API_QA_CHECKLIST.md`
- `BUG_REPORTS.md`
- `API_QA_REPORT.md`
- `README.md`
- `evidence/`

---

## 9. Tools

- API testing client
- Visual Studio Code
- Git
- GitHub
- Markdown

---

## 10. Skills Demonstrated

- REST API testing
- Manual API testing
- HTTP methods
- HTTP status codes
- JSON validation
- Positive testing
- Negative testing
- Test case design
- Test execution
- Defect reporting
- Evidence collection
- QA documentation

---

## 11. Project Status

**Current Status:** 🟡 In Progress

Testing results will be recorded only after actual execution.

---

**Author:** Alexei  
**Portfolio Project:** API Testing