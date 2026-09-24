const { test, expect } = require('@playwright/test');

test.use({
  channel: 'chrome',
});

test('TC-AUTO-001 - Successful login', async ({ page }) => {
  await page.goto('https://www.saucedemo.com/');

  await page.locator('[data-test="username"]').fill('standard_user');
  await page.locator('[data-test="password"]').fill('secret_sauce');
  await page.locator('[data-test="login-button"]').click();

  await expect(page).toHaveURL(/inventory/);
  await expect(page.locator('.title')).toHaveText('Products');
});
test('TC-AUTO-002 - Login with invalid credentials', async ({ page }) => {

  await page.goto('https://www.saucedemo.com/');

  await page.locator('[data-test="username"]').fill('wrong_user');
  await page.locator('[data-test="password"]').fill('wrong_password');

  await page.locator('[data-test="login-button"]').click();

  await expect(page.locator('[data-test="error"]'))
    .toContainText('Username and password do not match');

});
test('TC-AUTO-003 - Login with empty username', async ({ page }) => {

  await page.goto('https://www.saucedemo.com/');

  await page.locator('[data-test="password"]').fill('secret_sauce');

  await page.locator('[data-test="login-button"]').click();

  await expect(page.locator('[data-test="error"]'))
    .toContainText('Username is required');

});
test('TC-AUTO-004 - Login with empty password', async ({ page }) => {

  await page.goto('https://www.saucedemo.com/');

  await page.locator('[data-test="username"]').fill('standard_user');

  await page.locator('[data-test="login-button"]').click();

  await expect(page.locator('[data-test="error"]'))
    .toContainText('Password is required');

});
test('TC-AUTO-005 - Add product to cart', async ({ page }) => {
  // Open SauceDemo
  await page.goto('https://www.saucedemo.com/');

  // Login
  await page.locator('[data-test="username"]').fill('standard_user');
  await page.locator('[data-test="password"]').fill('secret_sauce');
  await page.locator('[data-test="login-button"]').click();

  // Verify Products page
  await expect(page).toHaveURL(/inventory/);
  await expect(page.locator('.title')).toHaveText('Products');

  // Add Sauce Labs Backpack to cart
  await page
    .locator('[data-test="add-to-cart-sauce-labs-backpack"]')
    .click();

  // Verify cart badge
  await expect(page.locator('.shopping_cart_badge')).toHaveText('1');

  // Open cart
  await page.locator('.shopping_cart_link').click();

  // Verify Cart page
  await expect(page).toHaveURL(/cart/);
  await expect(page.locator('.title')).toHaveText('Your Cart');

  // Verify selected product
  await expect(page.locator('.inventory_item_name'))
    .toHaveText('Sauce Labs Backpack');
});
test('TC-AUTO-006 - Checkout information', async ({ page }) => {
  // Open SauceDemo
  await page.goto('https://www.saucedemo.com/');

  // Login
  await page.locator('[data-test="username"]').fill('standard_user');
  await page.locator('[data-test="password"]').fill('secret_sauce');
  await page.locator('[data-test="login-button"]').click();

  // Add product to cart
  await page
    .locator('[data-test="add-to-cart-sauce-labs-backpack"]')
    .click();

  // Open cart
  await page.locator('.shopping_cart_link').click();

  // Start checkout
  await page.locator('[data-test="checkout"]').click();

  // Verify Checkout Information page
  await expect(page).toHaveURL(/checkout-step-one/);
  await expect(page.locator('.title'))
    .toHaveText('Checkout: Your Information');

  // Fill customer information
  await page.locator('[data-test="firstName"]').fill('Alex');
  await page.locator('[data-test="lastName"]').fill('Tester');
  await page.locator('[data-test="postalCode"]').fill('12345');

  // Continue checkout
  await page.locator('[data-test="continue"]').click();

  // Verify Checkout Overview
  await expect(page).toHaveURL(/checkout-step-two/);
  await expect(page.locator('.title'))
    .toHaveText('Checkout: Overview');

  // Verify product is still in the order
  await expect(page.locator('.inventory_item_name'))
    .toHaveText('Sauce Labs Backpack');
});
test('TC-AUTO-007 - Complete purchase E2E', async ({ page }) => {
  // 1. Open SauceDemo
  await page.goto('https://www.saucedemo.com/');

  // 2. Login
  await page.locator('[data-test="username"]').fill('standard_user');
  await page.locator('[data-test="password"]').fill('secret_sauce');
  await page.locator('[data-test="login-button"]').click();

  // Verify Products page
  await expect(page).toHaveURL(/inventory/);
  await expect(page.locator('.title')).toHaveText('Products');

  // 3. Add product to cart
  await page
    .locator('[data-test="add-to-cart-sauce-labs-backpack"]')
    .click();

  // Verify cart badge
  await expect(page.locator('.shopping_cart_badge')).toHaveText('1');

  // 4. Open cart
  await page.locator('.shopping_cart_link').click();

  // Verify product in cart
  await expect(page.locator('.inventory_item_name'))
    .toHaveText('Sauce Labs Backpack');

  // 5. Start checkout
  await page.locator('[data-test="checkout"]').click();

  // 6. Fill customer information
  await page.locator('[data-test="firstName"]').fill('Alex');
  await page.locator('[data-test="lastName"]').fill('Tester');
  await page.locator('[data-test="postalCode"]').fill('12345');

  await page.locator('[data-test="continue"]').click();

  // 7. Verify Checkout Overview
  await expect(page).toHaveURL(/checkout-step-two/);
  await expect(page.locator('.title'))
    .toHaveText('Checkout: Overview');

  await expect(page.locator('.inventory_item_name'))
    .toHaveText('Sauce Labs Backpack');

  // 8. Finish order
  await page.locator('[data-test="finish"]').click();

  // 9. Verify successful order
  await expect(page).toHaveURL(/checkout-complete/);

  await expect(page.locator('.title'))
    .toHaveText('Checkout: Complete!');

  await expect(page.locator('.complete-header'))
    .toHaveText('Thank you for your order!');
});