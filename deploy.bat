@echo off
REM Deploy Fertilizer Prediction System to GitHub & Render
REM For: dahi2003

setlocal enabledelayedexpansion

set DEPLOY_DIR=c:\Users\ASUS\Downloads\mlcsjm\fertilizer_prediction_deployment

cd /d "%DEPLOY_DIR%" || (
    echo ERROR: Cannot change to deployment directory
    echo Expected: %DEPLOY_DIR%
    pause
    exit /b 1
)

echo.
echo =============================================
echo  Fertilizer Prediction Deployment Setup
echo  GitHub User: dahi2003
echo =============================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git is not installed or not in PATH
    echo Please install Git from: https://git-scm.com/download/win
    pause
    exit /b 1
)

echo [1/4] Initializing Git Repository...
git init
if errorlevel 1 goto error

git config user.email "dahi2003@example.com"
git config user.name "dahi2003"

echo [2/4] Adding all files to git...
git add .
if errorlevel 1 goto error

echo [3/4] Creating initial commit...
git commit -m "Initial commit: Fertilizer Prediction System deployment package"
if errorlevel 1 goto error

echo.
echo [4/4] Git Status
echo =============================================
git log --oneline -1
git status

echo.
echo =============================================
echo  SUCCESS! Ready to deploy
echo =============================================
echo.
echo NEXT STEPS:
echo.
echo 1. Create GitHub Repository
echo    Go to: https://github.com/new
echo    Name: fertilizer-prediction
echo    Do NOT initialize with README
echo.
echo 2. Connect Local Repo to GitHub
echo    git remote add origin https://github.com/dahi2003/fertilizer-prediction.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo 3. Deploy on Render
echo    Go to: https://render.com
echo    Click: New Web Service
echo    Select: dahi2003/fertilizer-prediction
echo    Deploy!
echo.
echo App will be live at: https://fertilizer-prediction-xxxxx.onrender.com
echo.
pause
exit /b 0

:error
echo.
echo ERROR: Deployment setup failed!
echo Please check the error message above and try again.
echo.
pause
exit /b 1
