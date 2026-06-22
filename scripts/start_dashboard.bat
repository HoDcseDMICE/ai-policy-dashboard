@echo off
REM Wrapper to run PowerShell start script
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0\start_dashboard.ps1"
