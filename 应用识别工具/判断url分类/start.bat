@echo off
setlocal enabledelayedexpansion

set "path=%~dp0"
echo current path: %path%

E:\python310\python.exe "%path%\test.py"

endlocal
pause