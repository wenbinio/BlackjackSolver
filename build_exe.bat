@echo off
setlocal

python -m pip install --upgrade pyinstaller
if errorlevel 1 exit /b 1

pyinstaller --clean --noconfirm --onefile --name BlackjackSolver solver.py
if errorlevel 1 exit /b 1

echo.
echo Built: dist\BlackjackSolver.exe
endlocal
