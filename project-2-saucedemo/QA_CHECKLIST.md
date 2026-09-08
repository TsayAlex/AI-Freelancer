# ✅ SauceDemo — QA Checklist

## 🔐 Authentication

- [ ] CHK-001 Login with valid username and password
- [ ] CHK-002 Login with invalid username
- [ ] CHK-003 Login with invalid password
- [ ] CHK-004 Login with empty username
- [ ] CHK-005 Login with empty password
- [ ] CHK-006 Login with both fields empty
- [ ] CHK-007 Verify locked-out user behaviour
- [ ] CHK-008 Verify error message for failed login

---

## 🛍️ Product Catalogue

- [ ] CHK-009 Verify product list loads successfully
- [ ] CHK-010 Verify product names are displayed
- [ ] CHK-011 Verify product prices are displayed
- [ ] CHK-012 Verify product images are displayed
- [ ] CHK-013 Open product details
- [ ] CHK-014 Sort products A → Z
- [ ] CHK-015 Sort products Z → A
- [ ] CHK-016 Sort products Price Low → High
- [ ] CHK-017 Sort products Price High → Low

---

## 🛒 Shopping Cart

- [ ] CHK-018 Add one product to cart
- [ ] CHK-019 Verify cart counter updates
- [ ] CHK-020 Add multiple products
- [ ] CHK-021 Verify products appear in cart
- [ ] CHK-022 Remove product from cart
- [ ] CHK-023 Verify cart counter after removing product
- [ ] CHK-024 Continue shopping from cart

---

## 💳 Checkout

- [ ] CHK-025 Start checkout
- [ ] CHK-026 Submit checkout with empty customer information
- [ ] CHK-027 Submit checkout without first name
- [ ] CHK-028 Submit checkout without last name
- [ ] CHK-029 Submit checkout without postal code
- [ ] CHK-030 Complete checkout with valid information
- [ ] CHK-031 Verify checkout overview
- [ ] CHK-032 Verify order completion confirmation

---

## 🧭 Navigation

- [ ] CHK-033 Open application menu
- [ ] CHK-034 Close application menu
- [ ] CHK-035 Verify logout
- [ ] CHK-036 Verify reset application state
- [ ] CHK-037 Verify navigation back to products

---

## 🎨 UI / Usability

- [ ] CHK-038 Check buttons are visible and clickable
- [ ] CHK-039 Check text readability
- [ ] CHK-040 Check product layout consistency
- [ ] CHK-041 Check error messages are understandable
- [ ] CHK-042 Check basic keyboard navigation

---

# 📊 Checklist Summary

| Area | Checks |
|---|---:|
| Authentication | 8 |
| Product Catalogue | 9 |
| Shopping Cart | 7 |
| Checkout | 8 |
| Navigation | 5 |
| UI / Usability | 5 |
| **TOTAL** | **42** |

---

## Status Legend

- [ ] Not tested
- [x] Passed
- ⚠️ Issue found
- ⛔ Blocked