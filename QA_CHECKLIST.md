# QA Checklist — Website Pre-Launch

## Environment setup
- Confirm staging URL and build version
- Note browser (name + version) and OS for each session
- Record device or viewport size (e.g., 375x812 for iPhone X)
- Ensure test accounts or steps to create accounts are available

## Smoke / Sanity
- Load homepage and main landing pages
- Ensure no 500/502/503 errors on load
- Check primary navigation links load

## Registration & Login
- Create new account (if allowed): success flow, email confirmation
- Login with valid credentials: success flow
- Incorrect credentials: proper error messages
- Session/cookie behavior: logout, remember-me, password reset flows
- Form validation: required fields, client-side and server-side errors

## Forms (all important forms)
- Field validation: required, format (email, phone), constraints
- Error messages: clear and actionable
- File uploads (if any): size/type rejection and messages
- Duplicate/submission handling: idempotency, success page

## Mobile Responsiveness
- Test common viewports: phone (360x800), tablet (768x1024), iPad sizes
- Check header/menu behavior and visibility of CTAs
- Forms render and are usable on touch devices
- No overlapping elements, cut-off text, or horizontal scroll

## Broken Links & Navigation
- Click main CTAs and primary nav links
- Crawl footer and sitemap pages for 404s
- Verify external links open in correct target/context

## Usability & Basic UX
- Clarity of primary CTAs and labels
- Readability and visual hierarchy on core pages
- Form UX: helpful placeholders, validation messages, focus order
- Error states are recoverable and informative

## Visual & Content Checks
- Important images load and have alt text (note missing alt)
- No placeholder copy like "Lorem ipsum"
- Consistent branding and styles across pages

## Accessibility (basic)
- Keyboard navigation for core flows (tab order)
- Color contrast issues for key text/buttons (note possible issues)

## Reporting Standards
- For each issue capture: title, URL, steps to reproduce, expected/actual, screenshot, browser/viewport, severity
- Use severity: Critical / Major / Minor / Trivial
- Include reproduction rate (always / sometimes / rare)

## Artifacts to deliver
- Screenshots named with page and step (e.g., login-error-375x812.png)
- Consolidated bug report (Markdown/PDF)
- Optional CSV of issues for import

---
*Checklist derived from JOB.md and PROFILE.md — tailored to manual QA strengths*