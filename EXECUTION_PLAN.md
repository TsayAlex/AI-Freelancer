# Execution Plan for Website QA

## Objective
Perform manual QA for the pre-launch website to verify registration, login, forms, mobile responsiveness, broken links, and basic usability; produce a clear bug report with screenshots and repro steps.

## Prerequisites (ask client)
- Staging/pre-launch URL
- Any test accounts or instructions to create them
- Priority pages or flows (if any)
- Preferred browsers/devices and viewports
- Access window and expected turnaround

## Scope
- Functional testing: registration, login, forms, error handling
- Responsive testing: phone/tablet viewport checks for primary pages
- Broken links and navigation sanity
- Basic usability review (clarity, CTA behavior, form hints)
- Deliverable: consolidated bug report with screenshots, reproduction steps, severity labels

## Out of Scope (unless requested)
- Automated cross-browser regression across large matrices
- Performance, load, penetration/security testing
- Full accessibility (WCAG) audit (can be offered as add-on)

## Timeline (estimate)
- Confirm scope & access: 0.5h
- Smoke check: 0.5h
- Functional flows: 2–3h
- Responsive checks: 1–1.5h
- Broken links/navigation: 0.5–1h
- Usability review & compile report: 1–1.5h
Total estimate: 6–8 hours (single tester)

## Detailed Steps
1. Confirm access, environment, and priority pages.
2. Perform smoke check to ensure staging is stable.
3. Execute functional tests for registration, login, and forms; capture screenshots at each failure or important step.
4. Run responsive checks across target viewports (mobile/tablet) for core pages.
5. Manually crawl key navigation and check links; note broken links.
6. Evaluate basic usability heuristics and note suggestions.
7. Compile bug report using the BUG_REPORT_TEMPLATE.md format.
8. Deliver report and await client feedback; perform one retest round if requested (additional time may apply).

## Deliverables
- Consolidated bug report (Markdown/PDF) with screenshots and repro steps
- Optional CSV/TSV of issues for import to trackers
- Short cover note for the client (CLIENT_DELIVERY_TEMPLATE.md)

## Communication and Handover
- All client-facing messages in English will be drafted and must be approved before sending.
- After delivery, provide retest notes and final sign-off checklist.

## Pricing note
- I can complete the above within the $80 fixed-price only if scope is limited to one environment (one desktop browser + common mobile viewport set) and one round of testing. Broader device/browser coverage or multiple retest rounds require scope discussion and additional fees.

---
*Prepared based on JOB.md and PROFILE.md*