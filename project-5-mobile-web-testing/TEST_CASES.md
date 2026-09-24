# Mobile Web Test Cases

## TC-MOB-001 — Successful Mobile Login
**Preconditions:** SauceDemo login page is open.

**Test Data:** standard_user / secret_sauce

**Steps:**
1. Enter valid username.
2. Enter valid password.
3. Tap Login.

**Expected Result:** Products page opens successfully.

**Actual Result:** Products page opened successfully.

**Status:** PASS  
**Priority:** Critical

---

## TC-MOB-002 — Add Product to Cart
**Preconditions:** User is logged in.

**Steps:**
1. Locate Sauce Labs Backpack.
2. Add the product to cart.

**Expected Result:** Product is added and cart badge displays 1.

**Actual Result:** Cart badge displayed 1 and product state changed to Remove.

**Status:** PASS  
**Priority:** High

---

## TC-MOB-003 — Cart Content
**Preconditions:** One product is in cart.

**Steps:**
1. Open cart.

**Expected Result:** Selected product is displayed with correct quantity.

**Actual Result:** Sauce Labs Backpack was displayed with quantity 1.

**Status:** PASS  
**Priority:** High

---

## TC-MOB-004 — Orientation Change
**Preconditions:** Cart contains one product.

**Steps:**
1. Open cart in portrait mode.
2. Rotate device to landscape.
3. Return to portrait.

**Expected Result:** Layout remains usable and cart state is preserved.

**Actual Result:** Cart state remained available after orientation change.

**Status:** PASS  
**Priority:** Medium

---

## TC-MOB-005 — Empty Checkout Validation
**Preconditions:** Checkout information page is open.

**Steps:**
1. Leave all fields empty.
2. Tap Continue.

**Expected Result:** Checkout is blocked and required-field error is displayed.

**Actual Result:** Error: First Name is required was displayed.

**Status:** PASS  
**Priority:** High

---

## TC-MOB-006 — Missing Last Name Validation
**Test Data:** First Name = Alex

**Steps:**
1. Enter Alex as First Name.
2. Leave Last Name empty.
3. Tap Continue.

**Expected Result:** Last Name validation error is displayed.

**Actual Result:** Error: Last Name is required was displayed.

**Status:** PASS  
**Priority:** High

---

## TC-MOB-007 — Missing Postal Code Validation
**Test Data:** Alex / Tester / empty Postal Code

**Steps:**
1. Enter First Name.
2. Enter Last Name.
3. Leave Postal Code empty.
4. Tap Continue.

**Expected Result:** Postal Code validation error is displayed.

**Actual Result:** Error: Postal Code is required was displayed.

**Status:** PASS  
**Priority:** High

---

## TC-MOB-008 — Valid Checkout Information
**Test Data:** Alex / Tester / 12345

**Steps:**
1. Enter valid checkout information.
2. Tap Continue.

**Expected Result:** Checkout Overview page opens.

**Actual Result:** Checkout Overview opened with product, payment, shipping and price information.

**Status:** PASS  
**Priority:** Critical

---

## TC-MOB-009 — Complete Mobile Purchase
**Preconditions:** Checkout Overview is open.

**Steps:**
1. Review order.
2. Tap Finish.

**Expected Result:** Checkout Complete page is displayed.

**Actual Result:** During retest, Checkout Complete and Thank you for your order were displayed.

**Status:** PASS  
**Priority:** Critical

## Note
One earlier Finish attempt redirected to Login. This was not reproduced during retest and is documented as an exploratory finding rather than a consistently reproducible defect.
