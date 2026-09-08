# 🧪 SauceDemo — Manual Test Cases

## Test Case Summary

| ID | Area | Test Case | Priority |
|---|---|---|---|
| TC-001 | Login | Login with valid credentials | High |
| TC-002 | Login | Login with invalid password | High |
| TC-003 | Login | Login with empty fields | High |
| TC-004 | Login | Login as locked-out user | High |
| TC-005 | Products | Verify product catalogue | High |
| TC-006 | Products | Sort products by price | Medium |
| TC-007 | Cart | Add product to cart | High |
| TC-008 | Cart | Add multiple products | High |
| TC-009 | Cart | Remove product from cart | High |
| TC-010 | Checkout | Checkout with empty information | High |
| TC-011 | Checkout | Checkout without postal code | Medium |
| TC-012 | Checkout | Complete successful purchase | Critical |
| TC-013 | Navigation | Logout | High |
| TC-014 | Navigation | Reset application state | Medium |
| TC-015 | UI | Keyboard navigation | Medium |

---

# Detailed Test Cases

## TC-001 — Login with valid credentials

**Priority:** High  
**Type:** Positive / Functional

### Preconditions
- SauceDemo login page is open.

### Steps
1. Enter a valid username.
2. Enter a valid password.
3. Click **Login**.

### Expected Result
The user is successfully logged in and the product catalogue is displayed.

**Status:** ✅ Passed

---

## TC-002 — Login with invalid password

**Priority:** High  
**Type:** Negative

### Steps
1. Enter a valid username.
2. Enter an invalid password.
3. Click **Login**.

### Expected Result
Login is rejected and an appropriate error message is displayed.

**Status:** ✅ Passed

---

## TC-003 — Login with empty fields

**Priority:** High  
**Type:** Validation

### Steps
1. Leave username empty.
2. Leave password empty.
3. Click **Login**.

### Expected Result
Login is rejected and a validation/error message is displayed.

**Status:** ✅ Passed

---

## TC-004 — Login as locked-out user

**Priority:** High  
**Type:** Negative

### Steps
1. Enter credentials for the locked-out test user.
2. Click **Login**.

### Expected Result
Access is denied and the application explains that the user is locked out.

**Status:** ✅ Passed

---

## TC-005 — Verify product catalogue

**Priority:** High  
**Type:** Functional / UI

### Preconditions
- User is logged in.

### Steps
1. Open the Products page.
2. Inspect the product catalogue.

### Expected Result
Products display their name, image, description, price and action button correctly.

**Status:** ✅ Passed

---

## TC-006 — Sort products by price

**Priority:** Medium  
**Type:** Functional

### Steps
1. Open the product sorting control.
2. Select **Price (low to high)**.
3. Review the product order.

### Expected Result
Products are displayed from the lowest price to the highest price.

**Status:** ✅ Passed

---

## TC-007 — Add product to cart

**Priority:** High  
**Type:** Functional

### Steps
1. Select a product.
2. Click **Add to cart**.
3. Open the shopping cart.

### Expected Result
The selected product appears in the cart and the cart counter is updated.

**Status:** ✅ Passed
---

## TC-008 — Add multiple products

**Priority:** High  
**Type:** Functional

### Steps
1. Add two or more products.
2. Open the shopping cart.

### Expected Result
All selected products appear in the cart and the counter shows the correct quantity.

**Status:** ✅ Passed

---

## TC-009 — Remove product from cart

**Priority:** High  
**Type:** Functional

### Preconditions
- At least one product is in the cart.

### Steps
1. Open the cart.
2. Remove a product.

### Expected Result
The product disappears from the cart and the cart counter is updated.

**Status:** ✅ Passed

---

## TC-010 — Checkout with empty information

**Priority:** High  
**Type:** Negative / Validation

### Steps
1. Add a product to the cart.
2. Start checkout.
3. Leave all customer fields empty.
4. Click **Continue**.

### Expected Result
Checkout does not continue and a validation message is displayed.

**Status:** ✅ Passed

---

## TC-011 — Checkout without postal code

**Priority:** Medium  
**Type:** Negative / Validation

### Steps
1. Enter first name.
2. Enter last name.
3. Leave postal code empty.
4. Click **Continue**.

### Expected Result
Checkout is blocked and a postal-code validation message is displayed.

**Status:** ✅ Passed

---

## TC-012 — Complete successful purchase

**Priority:** Critical  
**Type:** End-to-End / Positive

### Steps
1. Log in.
2. Add a product to the cart.
3. Open the cart.
4. Start checkout.
5. Enter valid customer information.
6. Continue to the order overview.
7. Click **Finish**.

### Expected Result
The order is completed successfully and an order confirmation is displayed.

**Status:** ✅ Passed

---

## TC-013 — Logout

**Priority:** High  
**Type:** Functional

### Steps
1. Log in.
2. Open the application menu.
3. Click **Logout**.

### Expected Result
The user is returned to the login page.

**Status:** ✅ Passed

---

## TC-014 — Reset application state

**Priority:** Medium  
**Type:** Functional

### Steps
1. Add products to the cart.
2. Open the application menu.
3. Select **Reset App State**.

### Expected Result
The application state is reset according to the expected demo behaviour.

**Status:** ✅ Passed

---

## TC-015 — Keyboard navigation

**Priority:** Medium  
**Type:** Accessibility / Usability

### Steps
1. Open the login page.
2. Use the **Tab** key to navigate.
3. Continue through interactive controls.

### Expected Result
Interactive elements can be reached in a logical order and keyboard focus is visible.

**Status:** ❌ Failed

---

# 📊 Execution Summary

| Status     | Count |
|------------|-------|
| Passed     | 14    |
| Failed     | 1     |
| Blocked    | 0     |
| Not Tested | 0     |
Total Test Cases: 15
Passed: 14
Failed: 1
Pass Rate: 93.3%

> Test results will be updated only after actual execution.
