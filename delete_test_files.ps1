# PowerShell script for å slette testfiler
Write-Host "🗑️ SLETTER TESTFILER MED POWERSHELL"
Write-Host "=" * 50

$testFiles = @(
    "test_500_errors_comprehensive.py",
    "test_500_fixes.py", 
    "test_500_fixes_verification.py",
    "test_access_control.py",
    "test_all_fixes.py",
    "test_endpoints.py",
    "test_user.json",
    "test_user_instance.json",
    "auth_test.log",
    "subscription_test.log",
    "contrast_test.html",
    "style_test.html",
    "styling_test.html",
    "navigation-test.html"
)

$deletedCount = 0

foreach ($file in $testFiles) {
    if (Test-Path $file) {
        try {
            Remove-Item $file -Force
            Write-Host "✅ Slettet: $file" -ForegroundColor Green
            $deletedCount++
        }
        catch {
            Write-Host "❌ Kunne ikke slette $file : $($_.Exception.Message)" -ForegroundColor Red
        }
    }
    else {
        Write-Host "⚪ Ikke funnet: $file" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "🎉 Slettet $deletedCount testfiler!" -ForegroundColor Green
