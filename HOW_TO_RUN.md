# How to Execute the Dashboard Application

This guide provides step-by-step instructions to set up and run the Dashboard application.

## Prerequisites

- **Python 3.8 or higher** (check with `python --version` or `python3 --version`)
- **pip** (Python package installer)
- **Access to the report directories** (timing and power reports)

## Step 0: Set Up Virtual Environment (Recommended for Linux)

Using a virtual environment is recommended to isolate dependencies:

### Create Virtual Environment

```bash
# Navigate to your project directory
cd /asic_work/mkhan/website

# Create virtual environment
python3 -m venv timing_env

# Or if you already have one:
# cd timing_env
```

### Activate Virtual Environment

```bash
# Activate the virtual environment
source timing_env/bin/activate

# Your prompt should now show (timing_env)
```

### Deactivate (when done)

```bash
deactivate
```

## Step 1: Install Dependencies

1. Open a terminal/command prompt in the project directory:
   ```bash
   cd path/to/Dashboard
   ```

2. **If using virtual environment**, activate it first:
   ```bash
   source timing_env/bin/activate
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```
   
   Or if you need to use `pip3`:
   ```bash
   pip3 install -r requirements.txt
   ```
   
   **Note**: With virtual environment activated, `pip` will install packages into the venv, not system-wide.

   This will install:
   - Flask (web framework)
   - pandas (data processing)
   - numpy (numerical operations)
   - itables (HTML table generation)

## Step 2: Configure Paths (Optional)

### Option A: Use Environment Variables (Recommended)

Set environment variables before running:

**On Linux/Mac:**
```bash
export CWD_BASE_TIMING="/asic_work/ewang/esf/old_work_areas"
export CWD_BASE_POWER="/asic_work/jchang/esf/power_released/"
export OUTDIR="/asic_work/mkhan/website/tempo"
export LOGFILE="/asic_work/mkhan/website/logs/timing.log"
export FLASK_HOST="127.0.0.1"
export FLASK_PORT="8080"
```

**On Windows (PowerShell):**
```powershell
$env:CWD_BASE_TIMING="C:\path\to\timing\reports"
$env:CWD_BASE_POWER="C:\path\to\power\reports"
$env:OUTDIR="C:\path\to\output"
$env:LOGFILE="C:\path\to\logs\timing.log"
$env:FLASK_HOST="127.0.0.1"
$env:FLASK_PORT="8080"
```

**On Windows (Command Prompt):**
```cmd
set CWD_BASE_TIMING=C:\path\to\timing\reports
set CWD_BASE_POWER=C:\path\to\power\reports
set OUTDIR=C:\path\to\output
set LOGFILE=C:\path\to\logs\timing.log
set FLASK_HOST=127.0.0.1
set FLASK_PORT=8080
```

### Option B: Edit config.py Directly

If you prefer not to use environment variables, edit `config.py`:

```python
class Config:
    CWD_BASE_TIMING = "/your/path/to/timing/reports"
    CWD_BASE_POWER = "/your/path/to/power/reports"
    OUTDIR = "/your/path/to/output"
    LOGFILE = "/your/path/to/logs/timing.log"
    # ... etc
```

## Step 3: Verify Directory Structure

Ensure your report directories exist and contain design folders:

```
/asic_work/ewang/esf/old_work_areas/
  ├── design1/
  ├── design2/
  └── ...

/asic_work/jchang/esf/power_released/
  ├── design1/
  ├── design2/
  └── ...
```

## Step 4: Run the Application

**Important**: Choose one method below. The bash script (Option B) is recommended as it automates most steps.

### Option A: Using Virtual Environment (Manual Method)

**With virtual environment activated:**
```bash
# Activate venv first
source timing_env/bin/activate

# Navigate to app directory
cd /asic_work/mkhan/website/timing_dashboard_flask

# Run the application
python app.py
```

**Or use the full path to venv Python:**
```bash
/asic_work/mkhan/website/timing_env/bin/python3 /asic_work/mkhan/website/timing_dashboard_flask/app.py
```

### Option B: Using Bash Script (Automated - Recommended)

The `start_dashboard.sh` script automates the startup process. **Note**: You still need to complete Steps 0-2 (virtual environment setup, dependencies installation, and configuration) before using the script.

**What the script does automatically:**
- ✅ Uses the virtual environment Python (no need to activate manually)
- ✅ Kills any existing process on port 8080
- ✅ Navigates to the correct directory
- ✅ Starts the Flask app in the background
- ✅ Waits for Flask to initialize
- ✅ Automatically opens your browser
- ✅ Handles Ctrl+C to properly stop the server

**Prerequisites before using the script:**
1. Virtual environment must exist at `/asic_work/mkhan/website/timing_env/`
2. Dependencies must be installed (Step 1)
3. Paths must be configured (Step 2)

**To use the script:**

1. Make sure the script is executable:
   ```bash
   chmod +x start_dashboard.sh
   ```

2. Run the script:
   ```bash
   ./start_dashboard.sh
   ```

3. The script will:
   - Clean up port 8080
   - Start the dashboard
   - Wait 15 seconds for initialization
   - Open your browser automatically
   - Display the server PID

**To stop the server:**
- Press `Ctrl+C` in the terminal where the script is running
- The script will automatically kill the Flask process

**Note**: If you need to modify paths in the script, edit the variables at the top of `start_dashboard.sh`:
```bash
VENV_PYTHON="/asic_work/mkhan/website/timing_env/bin/python3"
APP_DIR="/asic_work/mkhan/website/timing_dashboard_flask"
APP_FILE="$APP_DIR/app.py"
URL="http://127.0.0.1:8080"
```

### Option C: Basic Execution (Without Virtual Environment)

Simply run:
```bash
python app.py
```

Or if you need to use `python3`:
```bash
python3 app.py
```

### Expected Output

You should see something like:
```
 * Serving Flask app 'app'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://127.0.0.1:8080
Press CTRL+C to quit
```

## Step 5: Access the Web Interface

1. Open your web browser
2. Navigate to: `http://127.0.0.1:8080`
3. You should see the Dashboard interface

## Step 6: Generate a Dashboard

1. **Select Dashboard Type**: Click "⏱ Timing" or "🔌 Power"
2. **Search Designs**: Use the search box to filter available designs
3. **Select Designs**: 
   - Click to select one design
   - Hold `Ctrl` (or `Cmd` on Mac) to select multiple
   - Use "[+] Select Visible" to select all filtered designs
4. **Enter Die Name**: Type the die name (e.g., "ESF")
5. **Click "Run Dashboard"**: Wait for processing
6. **View Results**: Click the generated dashboard links

## Troubleshooting

### Port Already in Use

If you see `Address already in use`, change the port:

**Option 1: Environment variable**
```bash
export FLASK_PORT="8081"
python app.py
```

**Option 2: Edit config.py**
```python
PORT = int(os.getenv("FLASK_PORT", "8081"))
```

### Module Not Found Errors

If you see `ModuleNotFoundError`:
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### Permission Denied Errors

If you see permission errors:
- **Linux/Mac**: Check directory permissions with `ls -la`
- **Windows**: Run as Administrator or check folder permissions

### Directory Not Found

If you see warnings about missing directories:
- Verify paths in `config.py` or environment variables
- Ensure directories exist and are accessible
- Check for typos in paths

### No Designs Showing

If the design list is empty:
- Verify the base directories (`CWD_BASE_TIMING`, `CWD_BASE_POWER`) exist
- Check that they contain subdirectories (design folders)
- Review the log file for errors

## Running in Production

For production deployment, use a proper WSGI server:

### Using Gunicorn (Linux/Mac)

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8080 app:app
```

### Using Waitress (Windows/Linux/Mac)

```bash
pip install waitress
waitress-serve --host=0.0.0.0 --port=8080 app:app
```

## Stopping the Application

Press `Ctrl+C` in the terminal where the application is running.

## Logs

Check the log file (configured in `config.py` or `LOGFILE` environment variable) for:
- Application errors
- Processing status
- Warnings about missing directories

## Quick Start (TL;DR)

### Using the Bash Script (Easiest - Recommended)

```bash
# 1. One-time setup: Create virtual environment (if not exists)
cd /asic_work/mkhan/website
python3 -m venv timing_env

# 2. One-time setup: Install dependencies
source timing_env/bin/activate
cd timing_dashboard_flask
pip install -r requirements.txt
deactivate

# 3. (Optional) Configure paths in config.py or set environment variables
export CWD_BASE_TIMING="/asic_work/ewang/esf/old_work_areas"
export CWD_BASE_POWER="/asic_work/jchang/esf/power_released/"
export OUTDIR="/asic_work/mkhan/website/tempo"
export LOGFILE="/asic_work/mkhan/website/logs/timing.log"

# 4. Run the script (every time you want to start)
./start_dashboard.sh
```

### With Virtual Environment (Manual Method)

```bash
# 1. Create and activate virtual environment
cd /asic_work/mkhan/website
python3 -m venv timing_env
source timing_env/bin/activate

# 2. Install dependencies
cd timing_dashboard_flask
pip install -r requirements.txt

# 3. (Optional) Set environment variables
export CWD_BASE_TIMING="/asic_work/ewang/esf/old_work_areas"
export CWD_BASE_POWER="/asic_work/jchang/esf/power_released/"
export OUTDIR="/asic_work/mkhan/website/tempo"
export LOGFILE="/asic_work/mkhan/website/logs/timing.log"

# 4. Run
python app.py

# 5. Open browser to http://127.0.0.1:8080
```

### Without Virtual Environment

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. (Optional) Set environment variables
export CWD_BASE_TIMING="/path/to/timing"
export CWD_BASE_POWER="/path/to/power"
export OUTDIR="/path/to/output"

# 3. Run
python app.py

# 4. Open browser to http://127.0.0.1:8080
```

## Example Session

### First-Time Setup (One-Time Only)

```bash
$ cd /asic_work/mkhan/website
$ python3 -m venv timing_env
$ source timing_env/bin/activate
(timing_env) $ cd timing_dashboard_flask
(timing_env) $ pip install -r requirements.txt
Collecting Flask...
Successfully installed Flask-2.3.0 pandas-1.5.3 ...
(timing_env) $ deactivate
```

### Using the Bash Script (Every Time You Start)

```bash
$ cd /asic_work/mkhan/website
$ ./start_dashboard.sh
------------------------------------------------
1. Cleaning up Port 8080...
2. Starting Timing Dashboard...
3. Waiting for Flask to initialize (15 seconds)...
4. Launching browser...
------------------------------------------------
Dashboard is LIVE at http://127.0.0.1:8080
PID: 12345
Press Ctrl+C to stop the server.
------------------------------------------------
```

### Manual Method (Alternative)

```bash
$ cd /asic_work/mkhan/website
$ source timing_env/bin/activate
(timing_env) $ cd timing_dashboard_flask
(timing_env) $ python app.py
 * Serving Flask app 'app'
 * Running on http://127.0.0.1:8080
```

Then in browser:
1. Go to `http://127.0.0.1:8080`
2. Select "Timing" dashboard
3. Search and select designs
4. Enter die name: "ESF"
5. Click "Run Dashboard"
6. View generated reports

## Need Help?

- Check `README.md` for general information
- Review `IMPROVEMENTS.md` for code improvement suggestions
- Check log files for detailed error messages
- Verify all paths are correct and accessible

