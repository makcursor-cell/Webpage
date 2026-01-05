# Dashboard Application

A Flask-based web application for generating timing and power dashboards from ASIC design reports.

## Features

- **Timing Dashboard**: Parse and visualize timing reports with setup/hold violations
- **Power Dashboard**: Parse and visualize power consumption reports
- **Multi-Design Comparison**: Compare multiple designs side-by-side
- **Modern UI**: Clean, responsive interface with search and filtering

## Setup

### Prerequisites

- Python 3.8 or higher
- Access to the report directories

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure paths (optional):
   - Set environment variables, or
   - Edit `config.py` directly

### Environment Variables

You can override default paths using environment variables:

```bash
export CWD_BASE_TIMING="/path/to/timing/reports"
export CWD_BASE_POWER="/path/to/power/reports"
export OUTDIR="/path/to/output/directory"
export LOGFILE="/path/to/logfile.log"
export FLASK_HOST="127.0.0.1"
export FLASK_PORT="8080"
export FLASK_DEBUG="False"
```

### Running the Application

```bash
python app.py
```

The application will be available at `http://127.0.0.1:8080`

## Usage

1. Select dashboard type (Timing or Power)
2. Search and select one or more designs
3. Enter the Die name
4. Click "Run Dashboard"
5. View generated dashboards and comparison reports

## Project Structure

```
Dashboard/
├── app.py                 # Main Flask application
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── backend/
│   ├── __init__.py
│   ├── backend_timing.py  # Timing report processing
│   └── backend_power.py  # Power report processing
└── templates/
    └── index.html         # Web interface
```

## Security Features

- Input sanitization to prevent path traversal attacks
- Design name validation
- Secure file serving with path checks

## Error Handling

- Comprehensive error logging
- User-friendly error messages
- Graceful handling of missing files

## Recent Improvements

- ✅ Configuration management via environment variables
- ✅ Improved error handling with specific exception types
- ✅ Input validation and security enhancements
- ✅ File encoding fixes (UTF-8)
- ✅ Removed duplicate/unused code
- ✅ Added requirements.txt
- ✅ Enhanced logging

## License

Internal use only.

