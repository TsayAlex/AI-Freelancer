# Mobile Web Test Plan

## Objective
Validate SauceDemo core functionality and usability in a mobile web environment.

## Scope
- Login
- Product page
- Scrolling
- Product sorting
- Add to cart
- Cart
- Portrait/Landscape orientation
- Checkout form
- Required field validation
- Checkout overview
- Order completion

## Out of Scope
- Native Android/iOS application testing
- Performance/load testing
- Security penetration testing
- Multiple physical devices
- Full cross-browser compatibility
- Accessibility conformance audit

## Test Types
- Functional
- Positive
- Negative
- Responsive
- Exploratory
- Validation
- Orientation
- End-to-End
- Retest

## Test Data
User: standard_user

Product: Sauce Labs Backpack

Checkout:
- First Name: Alex
- Last Name: Tester
- Postal Code: 12345

## Main Risks
1. Mobile layout may break on smaller screens.
2. Mobile keyboard may interfere with forms.
3. Orientation changes may lose application state.
4. Cart state may be lost.
5. Validation may allow incomplete checkout data.
6. Authentication/session state may be lost during checkout.

## Entry Criteria
- SauceDemo accessible from mobile browser.
- Test user available.
- Network connection available.

## Exit Criteria
- Critical E2E flow executed.
- Major observations documented.
- Evidence captured for key scenarios.
- Retest performed for significant unexpected behavior.

## Deliverables
- Mobile Checklist
- Test Cases
- Investigation Notes
- Screenshot Evidence
- Test Report
