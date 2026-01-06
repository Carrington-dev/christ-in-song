@echo off
REM ============================================================================
REM Christ In Song Hymnal - Quick Build Script for Windows
REM ============================================================================
REM This script builds a standalone executable (.exe) file
REM Save this as: scripts/quick_build.bat
REM ============================================================================

echo.
echo ╔══════════════════════════════════════════════════════════════════════════╗
echo ║              CHRIST IN SONG - QUICK BUILD SCRIPT                         ║
echo ╚══════════════════════════════════════════════════════════════════════════╝
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo ❌ ERROR: Virtual environment not found!
    echo.
    echo Please create it first:
    echo    python -m venv venv
    echo    venv\Scripts\activate
    echo    pip install -r requirements-dev.txt
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
echo 📦 Activating virtual environment...
call venv\Scripts\activate
echo ✅ Virtual environment activated
echo.

REM Clean previous builds
echo 🧹 Cleaning previous builds...
if exist "build" (
    rmdir /s /q build
    echo    ✓ Removed build directory
)
if exist "dist" (
    rmdir /s /q dist
    echo    ✓ Removed dist directory
)
echo ✅ Cleanup complete
echo.

REM Check if spec file exists
if not exist "installer\build_windows.spec" (
    echo ❌ ERROR: PyInstaller spec file not found!
    echo    Expected: installer\build_windows.spec
    echo.
    pause
    exit /b 1
)

REM Run PyInstaller
echo 🔨 Building executable with PyInstaller...
echo    This may take 2-5 minutes...
echo.
pyinstaller --clean installer\build_windows.spec

REM Check if build succeeded
if exist "dist\ChristInSong.exe" (
    echo.
    echo ╔══════════════════════════════════════════════════════════════════════════╗
    echo ║                         BUILD SUCCESSFUL! 🎉                              ║
    echo ╚══════════════════════════════════════════════════════════════════════════╝
    echo.
    echo ✅ Your application has been built!
    echo.
    echo 📁 Location: dist\ChristInSong.exe
    
    REM Get file size
    for %%A in (dist\ChristInSong.exe) do (
        set size=%%~zA
        set /a sizeMB=%%~zA/1048576
    )
    echo 📊 Size: ~%sizeMB% MB
    echo.
    echo 🚀 What's next?
    echo    1. Test the executable: dist\ChristInSong.exe
    echo    2. Copy it to another computer to verify it works standalone
    echo    3. Distribute to users!
    echo.
    echo 💡 Optional: Create a professional installer
    echo    - Install Inno Setup from: https://jrsoftware.org/isdl.php
    echo    - Run: python scripts\build_windows.py
    echo.
) else (
    echo.
    echo ╔══════════════════════════════════════════════════════════════════════════╗
    echo ║                         BUILD FAILED! ❌                                  ║
    echo ╚══════════════════════════════════════════════════════════════════════════╝
    echo.
    echo ❌ The executable was not created.
    echo.
    echo 🔍 Common issues:
    echo    1. Missing dependencies - run: pip install -r requirements-dev.txt
    echo    2. PyInstaller not installed - run: pip install pyinstaller
    echo    3. Syntax errors in Python code
    echo    4. Missing resource files
    echo.
    echo 📋 Check the error messages above for details.
    echo.
)

echo.
echo Press any key to exit...
pause >nul