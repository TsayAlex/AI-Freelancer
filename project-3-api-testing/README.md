# REST API Testing Portfolio Project

## Overview

This project demonstrates practical **Manual REST API Testing** skills using **Postman** and the **JSONPlaceholder REST API**.

The project was created as part of my QA portfolio to demonstrate my ability to design API test cases, execute HTTP requests, validate responses, perform positive and negative testing, and document test results.

---

## Test Results

| Metric | Result |
|---|---:|
| Total Test Cases | 10 |
| Passed | 10 |
| Failed | 0 |
| Pass Rate | 100% |
| Overall Result | PASS |

All 10 planned API test cases were manually executed in Postman.

---

## API Tested

JSONPlaceholder REST API

Main resource tested:

`/posts`

---

## HTTP Methods Tested

- GET
- POST
- PUT
- PATCH
- DELETE

---

## Test Scenarios

The project includes testing of:

1. Retrieving all posts
2. Retrieving a specific post
3. Requesting a non-existing resource
4. Creating a new resource
5. Creating a resource with an empty JSON body
6. Updating a complete resource
7. Partially updating a resource
8. Deleting a resource
9. Filtering resources with a valid query parameter
10. Filtering resources with a non-existing user ID

---

## HTTP Status Codes Verified

| Status | Meaning |
|---|---|
| 200 OK | Successful request |
| 201 Created | Resource creation accepted |
| 404 Not Found | Resource does not exist |

---

## Example Requests

### GET

`GET /posts/1`

Expected result:

`200 OK`

### POST

`POST /posts`

Example JSON body:

```json
{
  "title": "QA API Test",
  "body": "This post was created during API testing",
  "userId": 1
}