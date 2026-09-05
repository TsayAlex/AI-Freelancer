const fs = require('fs');
const path = require('path');

// ==================================================
// PATHS
// ==================================================

const projectRoot = path.resolve(__dirname, '..');

const logPath = path.join(
  projectRoot,
  'QA_RUN_OUTPUT_NEW.txt'
);

const markdownReportPath = path.join(
  projectRoot,
  'QA_TEST_REPORT.md'
);

const htmlReportPath = path.join(
  projectRoot,
  'QA_TEST_REPORT.html'
);

// ==================================================
// READ LOG
// ==================================================

function readLog(filePath) {
  if (!fs.existsSync(filePath)) {
    throw new Error(`QA log not found: ${filePath}`);
  }

  const buffer = fs.readFileSync(filePath);

  let text;

  // UTF-16 LE
  if (
    buffer.length >= 2 &&
    buffer[0] === 0xff &&
    buffer[1] === 0xfe
  ) {
    text = buffer
      .slice(2)
      .toString('utf16le');
  }

  // UTF-16 BE
  else if (
    buffer.length >= 2 &&
    buffer[0] === 0xfe &&
    buffer[1] === 0xff
  ) {
    const swapped = Buffer.alloc(
      buffer.length - 2
    );

    for (
      let i = 2;
      i < buffer.length;
      i += 2
    ) {
      swapped[i - 2] =
        buffer[i + 1] || 0;

      swapped[i - 1] =
        buffer[i];
    }

    text = swapped.toString('utf16le');
  }

  // UTF-8
  else {
    text = buffer.toString('utf8');
  }

  return text.replace(/\0/g, '');
}

// ==================================================
// PARSE ISSUES
// ==================================================

function parseIssues(logText) {
  const normalized =
    logText.replace(/\r\n/g, '\n');

  const blocks =
    normalized.split(/\nISSUE:\s*\n/);

  const issues = [];

  for (let i = 1; i < blocks.length; i++) {
    const block = blocks[i];

    const id =
      block.match(/^ID:\s*(.+)$/m)?.[1]?.trim();

    if (!id) {
      continue;
    }

    const area =
      block.match(/^Area:\s*(.+)$/m)?.[1]?.trim() ||
      'Unknown';

    const severity =
      block.match(/^Severity:\s*(.+)$/m)?.[1]?.trim() ||
      'Unknown';

    const expected =
      block.match(/^Expected:\s*(.+)$/m)?.[1]?.trim() ||
      'Not recorded';

    const actual =
      block.match(/^Actual:\s*(.+)$/m)?.[1]?.trim() ||
      'Not recorded';

    const steps =
      block.match(
        /^Reproduction steps:\s*(.+)$/m
      )?.[1]?.trim() ||
      'Not recorded';

    const evidence =
      block.match(/^Evidence:\s*(.+)$/m)?.[1]?.trim() ||
      'Not recorded';

    issues.push({
      id,
      area,
      severity,
      expected,
      actual,
      steps,
      evidence,
    });
  }

  return Array.from(
    new Map(
      issues.map((issue) => [
        issue.id,
        issue,
      ])
    ).values()
  );
}

// ==================================================
// FRIENDLY TITLES
// ==================================================

function getFinding(issue) {
  if (issue.id === 'BUG-001') {
    return 'About link points to a missing page';
  }

  if (issue.id === 'BUG-002') {
    return 'Missing Page link points to a missing page';
  }

  if (issue.id === 'BUG-003') {
    return 'Malformed email is accepted';
  }

  return issue.actual;
}

// ==================================================
// REPRODUCTION STEPS
// ==================================================

function getSteps(issue) {
  if (issue.id === 'BUG-001') {
    return [
      'Open the main page.',
      'Click About.',
      'Observe the navigation failure.',
    ];
  }

  if (issue.id === 'BUG-002') {
    return [
      'Open the main page.',
      'Click Missing Page.',
      'Observe the navigation failure.',
    ];
  }

  if (issue.id === 'BUG-003') {
    return [
      'Open the registration form.',
      'Enter not-an-email.',
      'Submit the form.',
      'Observe that the malformed email is accepted.',
    ];
  }

  return [issue.steps];
}

// ==================================================
// SEVERITY
// ==================================================

function countSeverity(issues) {
  const counts = {
    Critical: 0,
    Major: 0,
    Minor: 0,
    Trivial: 0,
  };

  for (const issue of issues) {
    if (
      Object.prototype.hasOwnProperty.call(
        counts,
        issue.severity
      )
    ) {
      counts[issue.severity]++;
    }
  }

  return counts;
}

// ==================================================
// STATUS
// ==================================================

function getStatus(issues, severity) {
  if (
    severity.Critical > 0 ||
    severity.Major > 0
  ) {
    return 'FAIL';
  }

  if (issues.length > 0) {
    return 'PASS WITH ISSUES';
  }

  return 'PASS';
}

// ==================================================
// ESCAPE HTML
// ==================================================

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

// ==================================================
// MARKDOWN REPORT
// ==================================================

function generateMarkdown(
  issues,
  severity,
  status
) {
  const today =
    new Date()
      .toISOString()
      .split('T')[0];

  const summaryRows =
    issues
      .map(
        (issue) =>
          `| ${issue.id} | ${issue.area} | ${issue.severity} | ${getFinding(issue)} |`
      )
      .join('\n');

  const detailed =
    issues
      .map((issue) => {
        const steps =
          getSteps(issue)
            .map(
              (step, index) =>
                `${index + 1}. ${step}`
            )
            .join('\n');

        const image =
          issue.evidence
            .toLowerCase()
            .endsWith('.png')
            ? `![${issue.id} screenshot](${issue.evidence.replace(/\\/g, '/')})`
            : `\`${issue.evidence}\``;

        return `## ${issue.id}

**Area:** ${issue.area}  
**Severity:** ${issue.severity}

### Finding

${getFinding(issue)}

### Expected

${issue.expected}

### Actual

${issue.actual}

### Reproduction Steps

${steps}

### Evidence

**Screenshot:** \`${issue.evidence}\`

${image}

---`;
      })
      .join('\n\n');

  return `# QA Test Report

## Test Information

| Field | Value |
|---|---|
| Date | ${today} |
| Project | AI-Freelancer |
| Test type | Automated Black-box QA |
| Framework | Playwright |
| Issues found | ${issues.length} |
| Overall result | **${status}** |

---

## Executive Summary

**Total unique issues detected: ${issues.length}**

### Severity Breakdown

| Severity | Count |
|---|---:|
| Critical | ${severity.Critical} |
| Major | ${severity.Major} |
| Minor | ${severity.Minor} |
| Trivial | ${severity.Trivial} |

---

## Issue Summary

| ID | Area | Severity | Finding |
|---|---|---|---|
${summaryRows || '| — | — | — | No issues detected |'}

---

# Detailed Findings

${detailed || 'No defects detected.'}

# Final Assessment

**Overall QA Status: ${status}**

---

*Generated automatically by the AI-Freelancer QA workflow.*
`;
}

// ==================================================
// HTML REPORT
// ==================================================

function generateHtml(
  issues,
  severity,
  status
) {
  const today =
    new Date()
      .toISOString()
      .split('T')[0];

  const statusClass =
    status === 'FAIL'
      ? 'status-fail'
      : status === 'PASS'
        ? 'status-pass'
        : 'status-warning';

  const cards =
    issues
      .map((issue) => {
        const steps =
          getSteps(issue)
            .map(
              (step) =>
                `<li>${escapeHtml(step)}</li>`
            )
            .join('');

        const evidencePath =
          issue.evidence.replace(/\\/g, '/');

        const image =
          issue.evidence
            .toLowerCase()
            .endsWith('.png')
            ? `
              <div class="evidence-block">
                <div class="section-label">Screenshot Evidence</div>
                <img
                  src="${escapeHtml(evidencePath)}"
                  alt="${escapeHtml(issue.id)} screenshot"
                  class="evidence-image"
                />
              </div>
            `
            : '';

        return `
          <article class="bug-card">

            <div class="bug-header">
              <div>
                <div class="bug-id">
                  ${escapeHtml(issue.id)}
                </div>

                <h2>
                  ${escapeHtml(getFinding(issue))}
                </h2>

                <div class="bug-area">
                  ${escapeHtml(issue.area)}
                </div>
              </div>

              <div class="severity severity-major">
                ${escapeHtml(issue.severity)}
              </div>
            </div>

            <div class="details-grid">

              <div class="detail-box">
                <div class="section-label">
                  Expected
                </div>

                <p>
                  ${escapeHtml(issue.expected)}
                </p>
              </div>

              <div class="detail-box actual-box">
                <div class="section-label">
                  Actual
                </div>

                <p>
                  ${escapeHtml(issue.actual)}
                </p>
              </div>

            </div>

            <div class="steps-block">

              <div class="section-label">
                Reproduction Steps
              </div>

              <ol>
                ${steps}
              </ol>

            </div>

            ${image}

          </article>
        `;
      })
      .join('');

  return `<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">

<meta
  name="viewport"
  content="width=device-width, initial-scale=1.0"
>

<title>
  AI-Freelancer QA Report
</title>

<style>

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  background: #f4f7fb;
  color: #18212f;
  font-family:
    Inter,
    Segoe UI,
    Arial,
    sans-serif;
}

.container {
  width: min(1200px, 94%);
  margin: 0 auto;
  padding: 40px 0 80px;
}

.hero {
  background:
    linear-gradient(
      135deg,
      #172033,
      #273b63
    );

  color: white;

  border-radius: 20px;

  padding: 34px;

  box-shadow:
    0 18px 50px
    rgba(14, 28, 51, 0.18);

  margin-bottom: 28px;
}

.hero-top {
  display: flex;
  justify-content: space-between;
  gap: 24px;
  align-items: flex-start;
}

.hero h1 {
  margin: 0 0 10px;
  font-size: 34px;
}

.hero p {
  margin: 0;
  color: #cbd5e1;
  font-size: 16px;
}

.status {
  min-width: 120px;
  text-align: center;
  padding: 12px 18px;
  border-radius: 999px;
  font-weight: 800;
  letter-spacing: 0.6px;
}

.status-fail {
  background: #fee2e2;
  color: #b91c1c;
}

.status-pass {
  background: #dcfce7;
  color: #166534;
}

.status-warning {
  background: #fef3c7;
  color: #92400e;
}

.metrics {
  display: grid;
  grid-template-columns:
    repeat(4, 1fr);

  gap: 16px;

  margin: 26px 0;
}

.metric {
  background: white;

  border-radius: 16px;

  padding: 22px;

  box-shadow:
    0 8px 28px
    rgba(21, 34, 50, 0.08);
}

.metric-label {
  font-size: 13px;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.7px;
}

.metric-value {
  margin-top: 8px;
  font-size: 28px;
  font-weight: 800;
}

.section-title {
  margin: 38px 0 18px;
  font-size: 24px;
}

.bug-card {
  background: white;

  border-radius: 18px;

  padding: 28px;

  margin-bottom: 26px;

  box-shadow:
    0 10px 32px
    rgba(21, 34, 50, 0.08);

  border:
    1px solid #e5eaf1;
}

.bug-header {
  display: flex;

  justify-content:
    space-between;

  align-items:
    flex-start;

  gap: 20px;

  padding-bottom: 20px;

  border-bottom:
    1px solid #e5eaf1;
}

.bug-id {
  font-size: 13px;
  font-weight: 800;
  color: #dc2626;
  letter-spacing: 0.7px;
}

.bug-header h2 {
  margin:
    6px 0 6px;

  font-size:
    24px;
}

.bug-area {
  color:
    #64748b;
}

.severity {
  padding:
    8px 14px;

  border-radius:
    999px;

  font-size:
    13px;

  font-weight:
    800;
}

.severity-major {
  background:
    #fee2e2;

  color:
    #b91c1c;
}

.details-grid {
  display: grid;

  grid-template-columns:
    1fr 1fr;

  gap:
    18px;

  margin-top:
    22px;
}

.detail-box {
  background:
    #f8fafc;

  border-radius:
    12px;

  padding:
    18px;

  border:
    1px solid #e5eaf1;
}

.actual-box {
  border-left:
    4px solid #dc2626;
}

.section-label {
  font-size:
    12px;

  font-weight:
    800;

  text-transform:
    uppercase;

  letter-spacing:
    0.7px;

  color:
    #64748b;

  margin-bottom:
    8px;
}

.detail-box p {
  margin:
    0;

  line-height:
    1.6;
}

.steps-block {
  margin-top:
    22px;
}

.steps-block ol {
  margin:
    8px 0 0;

  padding-left:
    22px;

  line-height:
    1.8;
}

.evidence-block {
  margin-top:
    24px;
}

.evidence-image {
  display:
    block;

  width:
    100%;

  max-height:
    680px;

  object-fit:
    contain;

  background:
    #f8fafc;

  border:
    1px solid #dbe3ec;

  border-radius:
    14px;

  margin-top:
    10px;
}

.footer {
  margin-top:
    40px;

  text-align:
    center;

  color:
    #64748b;

  font-size:
    14px;
}

.meta {
  margin-top:
    16px;

  color:
    #94a3b8;

  font-size:
    13px;
}

@media (
  max-width: 800px
) {

  .metrics {
    grid-template-columns:
      1fr 1fr;
  }

  .details-grid {
    grid-template-columns:
      1fr;
  }

  .hero-top {
    flex-direction:
      column;
  }
}

@media (
  max-width: 520px
) {

  .metrics {
    grid-template-columns:
      1fr;
  }

  .container {
    width:
      92%;
  }

  .hero {
    padding:
      24px;
  }

  .bug-card {
    padding:
      20px;
  }

}

</style>

</head>

<body>

<div class="container">

  <section class="hero">

    <div class="hero-top">

      <div>

        <h1>
          AI-Freelancer QA Report
        </h1>

        <p>
          Automated Black-box QA • Playwright
        </p>

        <div class="meta">
          Generated: ${today}
        </div>

      </div>

      <div class="status ${statusClass}">
        ${escapeHtml(status)}
      </div>

    </div>

  </section>

  <section class="metrics">

    <div class="metric">

      <div class="metric-label">
        Total Issues
      </div>

      <div class="metric-value">
        ${issues.length}
      </div>

    </div>

    <div class="metric">

      <div class="metric-label">
        Major
      </div>

      <div class="metric-value">
        ${severity.Major}
      </div>

    </div>

    <div class="metric">

      <div class="metric-label">
        Critical
      </div>

      <div class="metric-value">
        ${severity.Critical}
      </div>

    </div>

    <div class="metric">

      <div class="metric-label">
        QA Status
      </div>

      <div class="metric-value">
        ${escapeHtml(status)}
      </div>

    </div>

  </section>

  <h2 class="section-title">
    Detailed Findings
  </h2>

  ${cards || '<p>No defects detected.</p>'}

  <div class="footer">

    Generated automatically by
    <strong>AI-Freelancer QA Automation</strong>

  </div>

</div>

</body>
</html>`;
}

// ==================================================
// MAIN
// ==================================================

try {
  const logText =
    readLog(logPath);

  const issues =
    parseIssues(logText);

  const severity =
    countSeverity(issues);

  const status =
    getStatus(
      issues,
      severity
    );

  const markdown =
    generateMarkdown(
      issues,
      severity,
      status
    );

  const html =
    generateHtml(
      issues,
      severity,
      status
    );

  fs.writeFileSync(
    markdownReportPath,
    markdown,
    'utf8'
  );

  fs.writeFileSync(
    htmlReportPath,
    html,
    'utf8'
  );

  console.log('');
  console.log('QA REPORT GENERATED');

  console.log(
    `Issues found: ${issues.length}`
  );

  console.log(
    `Critical: ${severity.Critical}`
  );

  console.log(
    `Major: ${severity.Major}`
  );

  console.log(
    `Minor: ${severity.Minor}`
  );

  console.log(
    `Trivial: ${severity.Trivial}`
  );

  console.log(
    `Status: ${status}`
  );

  console.log('');

  console.log(
    `Markdown: ${markdownReportPath}`
  );

  console.log(
    `HTML: ${htmlReportPath}`
  );

  console.log('');

  console.log('DETECTED ISSUES');

  console.log('');

  for (const issue of issues) {
    console.log(
      `${issue.id} | ${issue.area} | ${issue.severity}`
    );

    console.log(
      `Finding: ${getFinding(issue)}`
    );

    console.log(
      `Evidence: ${issue.evidence}`
    );

    console.log('');
  }
} catch (error) {
  console.error('');
  console.error(
    'REPORT GENERATION FAILED'
  );

  console.error(
    error.message
  );

  process.exitCode = 1;
}