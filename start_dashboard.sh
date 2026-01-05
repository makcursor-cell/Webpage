#!/bin/bash

# --- CONFIGURATION ---
VENV_PYTHON="/asic_work/mkhan/website/timing_env/bin/python3"
APP_DIR="/asic_work/mkhan/website/timing_dashboard_flask"
APP_FILE="$APP_DIR/app.py"
URL="http://127.0.0.1:8080"

echo "------------------------------------------------"
echo "1. Cleaning up Port 8080..."
# Attempt to kill any old process on this port
fuser -k 8080/tcp > /dev/null 2>&1
sleep 1

echo "2. Starting Timing Dashboard..."
cd $APP_DIR
# Launch in background
$VENV_PYTHON $APP_FILE &
APP_PID=$!

echo "3. Waiting for Flask to initialize (15 seconds)..."
# We use a fixed sleep here because network file systems can make 
# startup checks unreliable

sleep 15

# Check if the process is still alive after the sleep
if ! kill -0 $APP_PID 2>/dev/null; then
    echo "Error: Python process died during startup."
    exit 1
fi

echo "4. Launching browser..."
if command -v xdg-open > /dev/null; then
    # Launch browser and detach it from the terminal
    xdg-open $URL > /dev/null 2>&1 &
elif command -v open > /dev/null; then
    open $URL
else
    echo "Please open browser manually: $URL"
fi

echo "------------------------------------------------"
echo "Dashboard is LIVE at $URL"
echo "PID: $APP_PID"
echo "Press Ctrl+C to stop the server."
echo "------------------------------------------------"

# This ensures that when you Ctrl+C, the Python background process dies too
trap "kill $APP_PID; echo -e '\nServer stopped.'; exit" INT
wait $APP_PID

