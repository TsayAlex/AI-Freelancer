# 🧪 API Test Cases

## Project Information

**Project:** REST API Testing Portfolio  
**Tester:** Alexei  
**Testing Type:** Manual API Testing  
**Status:** In Progress

---

# API-001 — Get List of Resources

**Method:** GET  
**Type:** Positive Testing  
**Status:** ✅ Passed

## Steps
1. Send a GET request to the resource list endpoint.
2. Check the HTTP status code.
3. Inspect the JSON response body.
4. Verify that a list of resources is returned.

## Expected Result
- Request is successful.
- Expected success status code is returned.
- Response body contains valid JSON.
- Resource data is returned.

---

# API-002 — Get Single Resource

**Method:** GET  
**Type:** Positive Testing  
**Status:** ✅ Passed

## Steps
1. Send a GET request using a valid resource ID.
2. Check the HTTP status code.
3. Inspect the JSON response.
4. Verify the returned resource.

## Expected Result
The requested resource is returned successfully.

---

# API-003 — Get Invalid Resource ID

**Method:** GET  
**Type:** Negative Testing  
**Status:** ✅ Passed

## Steps
1. Send a GET request using an invalid/non-existing resource ID.
2. Check the HTTP status code.
3. Inspect the response body.

## Expected Result
The API handles the non-existing resource correctly and returns the documented error response.

---

# API-004 — Create Resource

**Method:** POST  
**Type:** Positive Testing  
**Status:** ✅ Passed.

## Steps
1. Prepare a valid JSON request body.
2. Send a POST request.
3. Check the HTTP status code.
4. Inspect the response body.

## Expected Result
The API accepts the valid request and returns the documented successful creation response.

---

# API-005 — Create Resource With Missing or Invalid Data

**Method:** POST  
**Type:** Negative Testing  
**Status:** ✅ Passed.

## Steps
1. Prepare an incomplete or invalid request body.
2. Send the POST request.
3. Check the HTTP status code.
4. Inspect error handling.

## Expected Result
The API responds according to its documented validation rules.

---

# API-006 — Update Resource

**Method:** PUT  
**Type:** Positive Testing  
**Status:** ✅ Passed.

## Steps
1. Select a valid resource.
2. Prepare updated JSON data.
3. Send a PUT request.
4. Inspect the response.

## Expected Result
The API accepts the valid update request and returns the documented successful response.

---

# API-007 — Update Invalid Resource

**Method:** PUT  
**Type:** Negative Testing  
**Status:** ✅ Passed.

## Steps
1. Use an invalid/non-existing resource ID.
2. Send an update request.
3. Check the status code and response.

## Expected Result
The API handles the request according to its documented behaviour for a non-existing resource.

---

# API-008 — Delete Resource

**Method:** DELETE  
**Type:** Positive Testing  
**Status:** ✅ Passed.

## Steps
1. Select a valid resource.
2. Send a DELETE request.
3. Check the HTTP status code.
4. Inspect the response.

## Expected Result
The API returns the documented successful deletion response.

---

# API-009 — Invalid Endpoint

**Method:** GET  
**Type:** Negative Testing  
**Status:** ✅ Passed.


## Steps
1. Send a request to an endpoint that does not exist.
2. Check the HTTP status code.
3. Inspect the response.

## Expected Result
The API returns an appropriate documented error response.

---

# API-010 — Validate JSON Response Structure

**Method:** GET  
**Type:** Validation Testing  
**Status:** ✅ Passed.

## Steps
1. Send a valid GET request.
2. Inspect the response body.
3. Verify the expected JSON structure.
4. Check important fields and data types.

## Expected Result
The JSON response matches the documented response structure.

---

# 📊 Execution Summary

| Status | Count |
|---|---:|
| Passed | 10 |
| Failed | 0 |
| Blocked | 0 |
| Not Tested | 0 |

**Total Test Cases:** 10
Pass Rate: 100%
Overall Result: PASS
> 