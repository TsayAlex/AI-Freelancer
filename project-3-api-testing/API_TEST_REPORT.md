# REST API Testing Report

## Project Information

| Field | Value |
|---|---|
| Project | REST API Testing |
| API | JSONPlaceholder |
| Tool | Postman |
| Test Type | Manual API Testing |
| Tester | Alexei |
| Total Test Cases | 10 |
| Passed | 10 |
| Failed | 0 |
| Pass Rate | 100% |
| Overall Result | PASS |

---

# Executive Summary

Manual REST API testing was performed using Postman against the JSONPlaceholder API.

The purpose of the project was to verify common REST API operations, HTTP status codes, JSON response structures, resource handling, and query parameter behaviour.

A total of **10 API test cases** were executed.

**All 10 test cases passed.**

Overall pass rate: **100%**

Overall result: **PASS**

---

# API Operations Tested

The following HTTP methods and API scenarios were tested:

- GET — retrieve all resources
- GET — retrieve a specific resource
- GET — request a non-existing resource
- POST — create a resource
- POST — create a resource with an empty JSON body
- PUT — update a complete resource
- PATCH — partially update a resource
- DELETE — delete a resource
- GET — filter resources using a valid query parameter
- GET — filter resources using a non-existing user ID

---

# Test Execution Results

| ID | Method | Scenario | Expected Status | Actual Status | Result |
|---|---|---|---:|---:|---|
| API-001 | GET | Get all posts | 200 | 200 | PASS |
| API-002 | GET | Get post ID 1 | 200 | 200 | PASS |
| API-003 | GET | Get non-existing post ID 9999 | 404 | 404 | PASS |
| API-004 | POST | Create new post | 201 | 201 | PASS |
| API-005 | POST | Create post with empty JSON body | 201 | 201 | PASS |
| API-006 | PUT | Update post ID 1 | 200 | 200 | PASS |
| API-007 | PATCH | Partially update post ID 1 | 200 | 200 | PASS |
| API-008 | DELETE | Delete post ID 1 | 200 | 200 | PASS |
| API-009 | GET | Filter posts by userId=1 | 200 | 200 | PASS |
| API-010 | GET | Filter posts by userId=9999 | 200 | 200 | PASS |

---

# Detailed Observations

## GET Requests

The API successfully returned collections and individual resources.

A request for:

`/posts/1`

returned HTTP status:

`200 OK`

A request for a non-existing resource:

`/posts/9999`

returned:

`404 Not Found`

This matched the expected behaviour.

---

## POST Requests

A new resource was created using:

`POST /posts`

The API returned:

`201 Created`

The response contained the submitted data and a generated resource ID.

An additional POST request with an empty JSON object was also tested.

The API returned:

`201 Created`

with a generated ID.

---

## PUT Request

A complete update was performed using:

`PUT /posts/1`

The API returned:

`200 OK`

The response contained the updated resource data.

---

## PATCH Request

A partial update was performed using:

`PATCH /posts/1`

Only the `title` field was supplied in the request.

The API returned:

`200 OK`

and the response reflected the updated title.

---

## DELETE Request

A DELETE request was sent to:

`DELETE /posts/1`

The API returned:

`200 OK`

with an empty JSON response.

---

## Query Parameter Testing

Filtering was tested using:

`GET /posts?userId=1`

The API returned:

`200 OK`

and resources associated with `userId=1`.

A negative filtering scenario was also tested:

`GET /posts?userId=9999`

The API returned:

`200 OK`

with an empty array:

`[]`

This was the expected result because no matching resources exist.

---

# HTTP Status Codes Verified

| Status Code | Meaning | Verified |
|---|---|---|
| 200 | OK | Yes |
| 201 | Created | Yes |
| 404 | Not Found | Yes |

---

# Final Test Summary

| Status | Count |
|---|---:|
| Passed | 10 |
| Failed | 0 |
| Blocked | 0 |
| Not Tested | 0 |
| **Total** | **10** |

**Pass Rate: 100%**

**Overall Result: PASS**

---

# Skills Demonstrated

This project demonstrates practical experience with:

- REST API testing
- Postman
- HTTP methods
- GET requests
- POST requests
- PUT requests
- PATCH requests
- DELETE requests
- Positive testing
- Negative testing
- HTTP status code validation
- JSON request bodies
- JSON response validation
- Query parameter testing
- API test case design
- Manual test execution
- QA documentation

---

# Project Artifacts

- `TEST_PLAN.md` — API testing plan
- `API_TEST_CASES.md` — API test cases and execution results
- `API_TEST_REPORT.md` — final API testing report

---

# Conclusion

The tested JSONPlaceholder API scenarios behaved according to the expected results defined in the test cases.

All **10 of 10 test cases passed**, resulting in a **100% pass rate**.

No defects were recorded during this test execution.

---

**Tester:** Alexei  
**Portfolio Project:** REST API Testing