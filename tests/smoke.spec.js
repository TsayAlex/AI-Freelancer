const { test, expect } = require('@playwright/test');

test('local browser smoke test', async ({ page }) => {

  await page.setContent(`
    <!DOCTYPE html>
    <html>
      <head>
        <title>AI Freelancer QA Test</title>
      </head>
      <body>
        <h1>AI Freelancer Browser Test</h1>
        <button id="testButton">Test Button</button>
      </body>
    </html>
  `);

  await expect(page).toHaveTitle('AI Freelancer QA Test');

  await expect(
    page.getByRole('heading', { name: 'AI Freelancer Browser Test' })
  ).toBeVisible();

  await expect(
    page.getByRole('button', { name: 'Test Button' })
  ).toBeVisible();

  console.log('Browser launched successfully');
  console.log('Title:', await page.title());
});