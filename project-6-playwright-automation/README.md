# Project 6 — Playwright Test Automation

## Overview

This project demonstrates automated end-to-end testing of the SauceDemo web application using Playwright and JavaScript.

The automation suite covers critical user flows including authentication, negative login validation, shopping cart functionality, checkout information, and the complete purchase journey.

## Application Under Test

SauceDemo

Test environment:
https://www.saucedemo.com/

## Tech Stack

- Playwright
- JavaScript
- Node.js
- Google Chrome
- VS Code
- Git
- GitHub

## Automated Test Scenarios

| ID | Test Scenario | Type |
|---|---|---|
| TC-AUTO-001 | Successful login | Positive |
| TC-AUTO-002 | Login with invalid credentials | Negative |
| TC-AUTO-003 | Login with empty username | Negative |
| TC-AUTO-004 | Login with empty password | Negative |
| TC-AUTO-005 | Add product to cart | Functional |
| TC-AUTO-006 | Checkout information | Functional |
| TC-AUTO-007 | Complete purchase E2E | End-to-End |

## Test Coverage

The automation suite currently covers:

- Valid authentication
- Invalid authentication
- Required field validation
- Product selection
- Add to cart
- Shopping cart verification
- Checkout navigation
- Customer information entry
- Checkout overview
- Purchase completion
- Final confirmation validation

## Test Design

The automated scenarios include:

- Positive Testing
- Negative Testing
- Functional Testing
- Validation Testing
- End-to-End Testing

## Running the Tests

Run all tests:

```bash
npx playwright test