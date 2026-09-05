$ErrorActionPreference = "Continue"

Write-Host ""
Write-Host "========================================"
Write-Host " AI-FREELANCER QA AUTOMATION"
Write-Host "========================================"
Write-Host ""

$Root = $PSScriptRoot
$Npx = Join-Path $Root "tools\node-v24.20.0-win-x64\npx.cmd"
$Log = Join-Path $Root "QA_RUN_OUTPUT_NEW.txt"
$Generator = Join-Path $Root "tests\generate-report.js"

Set-Location $Root

Write-Host "[1/3] Running Playwright QA tests..."
Write-Host ""

if (Test-Path $Npx) {
    & $Npx playwright test tests/broken-site.spec.js --reporter=list 2>&1 |
        Tee-Object -FilePath $Log
}
else {
    npx playwright test tests/broken-site.spec.js --reporter=list 2>&1 |
        Tee-Object -FilePath $Log
}

Write-Host ""
Write-Host "[2/3] Test log saved:"
Write-Host $Log
Write-Host ""

if (-not (Test-Path $Log)) {
    Write-Host "ERROR: QA log was not created."
    exit 1
}

Write-Host "[3/3] Generating professional QA report..."
Write-Host ""

node $Generator

Write-Host ""
Write-Host "========================================"
Write-Host " QA WORKFLOW COMPLETE"
Write-Host "========================================"
Write-Host ""
Write-Host "Raw log:"
Write-Host $Log
Write-Host ""
Write-Host "QA report:"
Write-Host (Join-Path $Root "QA_TEST_REPORT.md")
Write-Host ""