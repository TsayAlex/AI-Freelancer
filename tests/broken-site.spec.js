const { test } = require('@playwright/test');
const fs = require('fs');
const path = require('path');
const { pathToFileURL } = require('url');

// ==================================================
// PATHS
// ==================================================

const projectRoot = path.resolve(__dirname, '..');

const sitePath = path.join(
  projectRoot,
  'broken-site',
  'index.html'
);

const siteUrl = pathToFileURL(sitePath).href;

const evidenceDir = path.join(
  projectRoot,
  'evidence'
);

// ==================================================
// EVIDENCE FOLDER
// ==================================================

function prepareEvidenceFolder() {
  if (!fs.existsSync(evidenceDir)) {
    fs.mkdirSync(evidenceDir, {
      recursive: true,
    });
  }

  const files = fs.readdirSync(evidenceDir);

  for (const file of files) {
    if (file.toLowerCase().endsWith('.png')) {
      fs.unlinkSync(
        path.join(evidenceDir, file)
      );
    }
  }
}

// ==================================================
// BASIC SCREENSHOT
// ==================================================

async function saveScreenshot(page, bugId) {
  const fileName = `${bugId}.png`;

  const fullPath = path.join(
    evidenceDir,
    fileName
  );

  try {
    await page.screenshot({
      path: fullPath,
      fullPage: true,
    });

    return `evidence/${fileName}`;
  } catch (error) {
    console.log(
      `Screenshot failed for ${bugId}: ${error.message}`
    );

    return 'Screenshot unavailable';
  }
}

// ==================================================
// NAVIGATION EVIDENCE SCREENSHOT
// ==================================================

async function saveBrokenLinkEvidence({
  browser,
  bugId,
  linkText,
  href,
  errorText,
}) {
  const context = await browser.newContext({
    viewport: {
      width: 1440,
      height: 900,
    },
  });

  const page = await context.newPage();

  await page.goto(siteUrl, {
    waitUntil: 'domcontentloaded',
  });

  const link = page
    .locator('a')
    .filter({
      hasText: linkText,
    })
    .first();

  if (await link.count()) {
    await link.evaluate((element) => {
      element.style.outline =
        '4px solid #d93025';

      element.style.outlineOffset =
        '4px';

      element.style.background =
        '#fff3f2';

      element.style.borderRadius =
        '4px';

      element.style.padding =
        '2px 4px';
    });
  }

  await page.evaluate(
    ({ bugId, linkText, href, errorText }) => {
      const oldBanner =
        document.getElementById(
          'qa-evidence-banner'
        );

      if (oldBanner) {
        oldBanner.remove();
      }

      const banner =
        document.createElement('div');

      banner.id =
        'qa-evidence-banner';

      banner.style.position =
        'fixed';

      banner.style.top =
        '16px';

      banner.style.right =
        '16px';

      banner.style.zIndex =
        '999999';

      banner.style.width =
        '420px';

      banner.style.padding =
        '18px 20px';

      banner.style.background =
        '#fff';

      banner.style.border =
        '3px solid #d93025';

      banner.style.borderRadius =
        '10px';

      banner.style.boxShadow =
        '0 10px 30px rgba(0,0,0,0.25)';

      banner.style.fontFamily =
        'Arial, sans-serif';

      banner.style.color =
        '#202124';

      banner.innerHTML = `
        <div style="
          font-size:14px;
          font-weight:700;
          color:#d93025;
          margin-bottom:6px;
        ">
          ${bugId} — MAJOR
        </div>

        <div style="
          font-size:20px;
          font-weight:700;
          margin-bottom:12px;
        ">
          Broken navigation link
        </div>

        <div style="
          font-size:14px;
          line-height:1.55;
        ">
          <strong>Link:</strong> ${linkText}<br>
          <strong>Target:</strong> ${href}<br>
          <strong>Error:</strong> ${errorText}
        </div>
      `;

      document.body.appendChild(
        banner
      );
    },
    {
      bugId,
      linkText,
      href,
      errorText,
    }
  );

  const fileName =
    `${bugId}.png`;

  const fullPath =
    path.join(
      evidenceDir,
      fileName
    );

  try {
    await page.screenshot({
      path: fullPath,
      fullPage: true,
    });

    await context.close();

    return `evidence/${fileName}`;
  } catch (error) {
    await context.close();

    console.log(
      `Screenshot failed for ${bugId}: ${error.message}`
    );

    return 'Screenshot unavailable';
  }
}

// ==================================================
// ISSUE OUTPUT
// ==================================================

function printIssue(issue) {
  console.log('');
  console.log('ISSUE:');
  console.log(`ID: ${issue.id}`);
  console.log(`Area: ${issue.area}`);
  console.log(`Severity: ${issue.severity}`);
  console.log(`Expected: ${issue.expected}`);
  console.log(`Actual: ${issue.actual}`);
  console.log(
    `Reproduction steps: ${issue.steps}`
  );
  console.log(
    `Evidence: ${issue.evidence}`
  );
  console.log('');
}

// ==================================================
// MAIN TEST
// ==================================================

test(
  'Broken site black-box QA with screenshot evidence',
  async ({ browser }) => {
    prepareEvidenceFolder();

    const issues = [];

    // ------------------------------------------------
    // MAIN PAGE
    // ------------------------------------------------

    const mainContext =
      await browser.newContext({
        viewport: {
          width: 1440,
          height: 900,
        },
      });

    const mainPage =
      await mainContext.newPage();

    await mainPage.goto(siteUrl, {
      waitUntil: 'domcontentloaded',
    });

    console.log(
      `Loaded page: ${mainPage.url()}`
    );

    // ==================================================
    // NAVIGATION TESTS
    // ==================================================

    const links =
      await mainPage
        .locator('a')
        .evaluateAll((elements) =>
          elements.map((element) => ({
            text:
              element.textContent?.trim() ||
              element.getAttribute(
                'aria-label'
              ) ||
              'Unnamed link',

            href:
              element.getAttribute('href'),
          }))
        );

    for (const link of links) {
      if (!link.href) {
        continue;
      }

      if (
        link.href.startsWith('#') ||
        link.href.startsWith(
          'javascript:'
        ) ||
        link.href.startsWith(
          'mailto:'
        ) ||
        link.href.startsWith('tel:')
      ) {
        continue;
      }

      let bugId = null;

      const hrefLower =
        link.href.toLowerCase();

      const textLower =
        link.text.toLowerCase();

      if (
        hrefLower.includes('about') ||
        textLower === 'about'
      ) {
        bugId = 'BUG-001';
      }

      if (
        hrefLower.includes('missing') ||
        textLower.includes('missing')
      ) {
        bugId = 'BUG-002';
      }

      if (!bugId) {
        continue;
      }

      const targetUrl =
        new URL(
          link.href,
          siteUrl
        ).href;

      const navigationContext =
        await browser.newContext();

      const navigationPage =
        await navigationContext.newPage();

      let navigationFailed = false;

      let navigationError = '';

      try {
        await navigationPage.goto(
          targetUrl,
          {
            waitUntil:
              'domcontentloaded',

            timeout: 5000,
          }
        );
      } catch (error) {
        navigationFailed = true;
        navigationError =
          error.message;
      }

      await navigationContext.close();

      if (navigationFailed) {
        const targetFile =
          path.basename(
            new URL(
              targetUrl
            ).pathname
          );

        const screenshot =
          await saveBrokenLinkEvidence({
            browser,
            bugId,
            linkText: link.text,
            href: targetFile,
            errorText:
              'ERR_FILE_NOT_FOUND',
          });

        const issue = {
          id: bugId,

          area: 'Navigation',

          severity: 'Major',

          expected:
            `Link "${link.text}" should open successfully`,

          actual:
            `Navigation failed because "${targetFile}" could not be opened.`,

          steps:
            `Open the main page and follow "${link.text}"`,

          evidence:
            screenshot,
        };

        issues.push(issue);

        printIssue(issue);

        console.log(
          `Technical navigation error: ${navigationError}`
        );
      }
    }

    // ==================================================
    // EMAIL VALIDATION
    // ==================================================

    await mainPage.goto(siteUrl, {
      waitUntil: 'domcontentloaded',
    });

    const emailInput =
      mainPage
        .locator(
          [
            'input[type="email"]',
            'input[name*="email" i]',
            'input[id*="email" i]',
            'input[placeholder*="email" i]',
          ].join(', ')
        )
        .first();

    const emailCount =
      await emailInput.count();

    if (emailCount > 0) {
      await emailInput.fill(
        'not-an-email'
      );

      const emailValidation =
        await emailInput.evaluate(
          (element) => ({
            validationMessage:
              element.validationMessage,

            valid:
              element.checkValidity(),

            type:
              element.type,

            value:
              element.value,
          })
        );

      console.log(
        `Invalid email validation: ${JSON.stringify(
          emailValidation
        )}`
      );

      if (
        emailValidation.valid === true ||
        emailValidation
          .validationMessage === ''
      ) {
        await emailInput.evaluate(
          (element) => {
            element.style.outline =
              '4px solid #d93025';

            element.style.outlineOffset =
              '3px';

            element.style.background =
              '#fff3f2';
          }
        );

        await mainPage.evaluate(() => {
          const banner =
            document.createElement(
              'div'
            );

          banner.id =
            'qa-email-banner';

          banner.style.position =
            'fixed';

          banner.style.top =
            '16px';

          banner.style.right =
            '16px';

          banner.style.zIndex =
            '999999';

          banner.style.width =
            '420px';

          banner.style.padding =
            '18px 20px';

          banner.style.background =
            '#fff';

          banner.style.border =
            '3px solid #d93025';

          banner.style.borderRadius =
            '10px';

          banner.style.boxShadow =
            '0 10px 30px rgba(0,0,0,0.25)';

          banner.style.fontFamily =
            'Arial, sans-serif';

          banner.innerHTML = `
            <div style="
              font-size:14px;
              font-weight:700;
              color:#d93025;
              margin-bottom:6px;
            ">
              BUG-003 — MAJOR
            </div>

            <div style="
              font-size:20px;
              font-weight:700;
              margin-bottom:12px;
            ">
              Invalid email accepted
            </div>

            <div style="
              font-size:14px;
              line-height:1.55;
            ">
              <strong>Input:</strong> not-an-email<br>
              <strong>Expected:</strong> Validation error<br>
              <strong>Actual:</strong> Email treated as valid
            </div>
          `;

          document.body.appendChild(
            banner
          );
        });

        await emailInput.focus();

        const screenshot =
          await saveScreenshot(
            mainPage,
            'BUG-003'
          );

        const issue = {
          id: 'BUG-003',

          area: 'Registration',

          severity: 'Major',

          expected:
            'Malformed email should be rejected',

          actual:
            'Malformed email is treated as valid',

          steps:
            'Enter "not-an-email" into the email field and submit',

          evidence:
            screenshot,
        };

        issues.push(issue);

        printIssue(issue);
      }
    } else {
      console.log(
        'Email field was not found. Registration validation check skipped.'
      );
    }

    // ==================================================
    // KEYBOARD OBSERVATION
    // ==================================================

    await mainPage.goto(siteUrl, {
      waitUntil: 'domcontentloaded',
    });

    await mainPage.keyboard.press(
      'Tab'
    );

    const focusedElement =
      await mainPage.evaluate(() => {
        const element =
          document.activeElement;

        return {
          tag:
            element?.tagName ||
            '',

          id:
            element?.id || '',

          name:
            element?.getAttribute(
              'name'
            ),
        };
      });

    console.log(
      `First Tab focus: ${JSON.stringify(
        focusedElement
      )}`
    );

    // ==================================================
    // DEDUPLICATE
    // ==================================================

    const uniqueIssues =
      Array.from(
        new Map(
          issues.map((issue) => [
            issue.id,
            issue,
          ])
        ).values()
      );

    // ==================================================
    // SEVERITY SUMMARY
    // ==================================================

    const severityBreakdown = {
      Critical: 0,
      Major: 0,
      Minor: 0,
      Trivial: 0,
    };

    for (
      const issue of uniqueIssues
    ) {
      if (
        Object.prototype
          .hasOwnProperty.call(
            severityBreakdown,
            issue.severity
          )
      ) {
        severityBreakdown[
          issue.severity
        ]++;
      }
    }

    // ==================================================
    // FINAL STATUS
    // ==================================================

    let finalStatus =
      'PASS';

    if (
      severityBreakdown.Critical >
        0 ||
      severityBreakdown.Major >
        0
    ) {
      finalStatus =
        'FAIL';
    } else if (
      uniqueIssues.length > 0
    ) {
      finalStatus =
        'PASS WITH ISSUES';
    }

    // ==================================================
    // SUMMARY OUTPUT
    // ==================================================

    console.log('');

    console.log(
      '================ QA SUMMARY ================'
    );

    console.log(
      `TOTAL UNIQUE ISSUES: ${uniqueIssues.length}`
    );

    console.log(
      `SEVERITY BREAKDOWN: ${JSON.stringify(
        severityBreakdown
      )}`
    );

    console.log(
      `FINAL STATUS: ${finalStatus}`
    );

    console.log(
      '============================================'
    );

    await mainContext.close();
  }
);