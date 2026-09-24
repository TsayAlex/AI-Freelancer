# Project 5 — Mobile Web Testing

## Product
SauceDemo — mobile web e-commerce demo application.

## Testing Goal
Evaluate the core user journey on a mobile device, including responsive UI, authentication, product interaction, cart, checkout validation, orientation changes, and end-to-end order completion.

## Test Approach
- Functional Testing
- Mobile Web Testing
- Responsive Testing
- Positive Testing
- Negative Testing
- Validation Testing
- Exploratory Testing
- Orientation Testing
- End-to-End Testing
- Retesting

## Core Flow Verified

Login → Products → Add to Cart → Cart → Checkout → Validation → Overview → Finish → Order Complete

**Result: PASS**

## Key Results
- Mobile login: PASS
- Product page: PASS
- Vertical scrolling: PASS
- Product sorting menu: PASS
- Add to cart: PASS
- Cart: PASS
- Portrait/Landscape state persistence: PASS
- Required field validation: PASS
- Checkout overview: PASS
- End-to-end purchase: PASS

## Exploratory Findings

### Browser translation behavior
A blank page was repeatedly observed while entering checkout information when browser translation was active.

After browser translation was disabled, the checkout form worked correctly.

**Conclusion:** environment-dependent behavior; not confirmed as a SauceDemo application defect.

### Intermittent checkout session behavior
During one checkout attempt, tapping Finish redirected the user to Login with an authentication error.

A direct retest of the complete flow succeeded and displayed the order confirmation page.

**Reproducibility:** Once  
**Status:** Needs further investigation.

## Evidence
Screenshots collected during real mobile testing are stored in the `evidence` directory.

## Final Result
The primary mobile purchase journey was successfully completed.

**Release assessment for tested scope: CONDITIONAL GO**

Reason: the critical E2E flow passed, but an intermittent session-related observation remains unconfirmed and requires additional investigation.
