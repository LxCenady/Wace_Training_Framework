@echo off
rem Double-click to start. Uses the bundled venv if present, else the Python launcher.
set "HERE=%~dp0"
if exist "%HERE%..\.venv\Scripts\pythonw.exe" (
  start "" "%HERE%..\.venv\Scripts\pythonw.exe" "%HERE%main.py"
) else (
  start "" pyw -3 "%HERE%main.py"
)
