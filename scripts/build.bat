@echo off
if "%1"=="--with-key" (
    powershell -ExecutionPolicy Bypass -File "%~dp0build.ps1" -WithKey
) else (
    powershell -ExecutionPolicy Bypass -File "%~dp0build.ps1"
)
pause
