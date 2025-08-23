@echo off
echo ===================================
echo SLETTER ALLE TESTFILER I WORKSPACE
echo ===================================

REM Sletter alle test*.py filer i root
for %%f in (test*.py) do (
    if exist "%%f" (
        echo Sletter: %%f
        del "%%f"
    )
)

REM Sletter alle test*.json filer
for %%f in (test*.json) do (
    if exist "%%f" (
        echo Sletter: %%f
        del "%%f"
    )
)

REM Sletter alle test*.html filer  
for %%f in (test*.html) do (
    if exist "%%f" (
        echo Sletter: %%f
        del "%%f"
    )
)

REM Sletter alle test*.txt filer
for %%f in (test*.txt) do (
    if exist "%%f" (
        echo Sletter: %%f
        del "%%f"
    )
)

REM Sletter alle test*.log filer
for %%f in (test*.log) do (
    if exist "%%f" (
        echo Sletter: %%f
        del "%%f"
    )
)

REM Sletter alle endpoint_test* filer
for %%f in (endpoint_test*) do (
    if exist "%%f" (
        echo Sletter: %%f
        del "%%f"
    )
)

REM Sletter spesifikke filer
if exist "test_user.json" del "test_user.json"
if exist "test_user_instance.json" del "test_user_instance.json"
if exist "subscription_test.log" del "subscription_test.log"
if exist "auth_test.log" del "auth_test.log"
if exist "navigation-test.html" del "navigation-test.html"
if exist "style_test.html" del "style_test.html"
if exist "styling_test.html" del "styling_test.html"
if exist "contrast_test.html" del "contrast_test.html"

REM Sletter testfiler i app directory
cd app
echo Sletter testfiler i app/...

for %%f in (test*.py) do (
    if exist "%%f" (
        echo Sletter: app/%%f
        del "%%f"
    )
)

for %%f in (*test.py) do (
    if exist "%%f" (
        echo Sletter: app/%%f
        del "%%f"
    )
)

for %%f in (test*.txt) do (
    if exist "%%f" (
        echo Sletter: app/%%f
        del "%%f"
    )
)

REM Sletter testfiler i app/tests hvis det finnes
if exist "tests" (
    cd tests
    echo Sletter testfiler i app/tests/...
    for %%f in (test*.py) do (
        if exist "%%f" (
            echo Sletter: app/tests/%%f
            del "%%f"
        )
    )
    cd ..
)

cd ..

echo =============================
echo TESTFIL CLEANUP FERDIG!
echo =============================
pause
