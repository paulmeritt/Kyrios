@echo off
:: Batch file to set up and run Kyrios

:: Set environment variables
echo Setting environment variables...
set KYRIOS_API_KEY=your_api_key
set KYRIOS_NODE_ID=your_node_id

:: Check if Python is installed
echo Checking Python installation...
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Please install Python 3.8 or higher.
    exit /b 1
)

:: Install required Python packages
echo Installing required Python packages...
pip install -r requirements.txt

:: Run Kyrios
echo Starting Kyrios agent system...
python core/main.py

pause
