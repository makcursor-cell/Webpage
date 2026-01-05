import os
import logging
import re
from flask import Flask, request, send_from_directory, abort, render_template

# Updated imports to match your folder structure
from backend.backend_timing import run_chip  # Timing dashboard
from backend.backend_power import run_power  # Power dashboard
from config import Config

app = Flask(__name__)

# Initialize configuration
Config.ensure_directories()
Config.validate_paths()

# --------------------------------------------------
# Logging
# --------------------------------------------------
logging.basicConfig(
    filename=Config.LOGFILE,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s"
)
logger = logging.getLogger(__name__)

# --------------------------------------------------
# Helpers
# --------------------------------------------------
def sanitize_input(value: str, max_length: int = 200) -> str:
    """Sanitize user input to prevent path traversal and other attacks."""
    if not value:
        return ""
    # Remove any path separators and dangerous characters
    value = re.sub(r'[<>:"|?*\x00-\x1f]', '', value)
    # Limit length
    value = value[:max_length].strip()
    return value


def validate_design_name(design: str) -> bool:
    """Validate that design name is safe."""
    if not design:
        return False
    # Check length
    if len(design) > Config.MAX_DESIGN_NAME_LENGTH:
        return False
    # Check for path traversal attempts
    if '..' in design or '/' in design or '\\' in design:
        return False
    return True


def list_designs(cwd):
    """List all directories in cwd"""
    try:
        if not os.path.isdir(cwd):
            logger.warning(f"Directory does not exist: {cwd}")
            return []
        dirs = [d for d in os.listdir(cwd) 
                if os.path.isdir(os.path.join(cwd, d)) and validate_design_name(d)]
        return sorted(dirs)
    except PermissionError:
        logger.error(f"Permission denied accessing directory: {cwd}")
        return []
    except Exception as e:
        logger.error(f"Error listing designs in {cwd}: {e}", exc_info=True)
        return []

# --------------------------------------------------
# Index page (multi-select form)
# --------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    designs_timing = list_designs(Config.CWD_BASE_TIMING)
    designs_power  = list_designs(Config.CWD_BASE_POWER)

    if request.method == "POST":
        selected_designs = request.form.getlist("designs")
        die = sanitize_input(request.form.get("die", "").strip(), Config.MAX_DIE_NAME_LENGTH)
        report_type = request.form.get("mode", "timing")

        # Validate inputs
        if not selected_designs:
            abort(400, "At least one design must be selected")
        if not die:
            abort(400, "Die name is required")
        if report_type not in ["timing", "power"]:
            abort(400, "Invalid report type")
        
        # Validate all design names
        for design in selected_designs:
            if not validate_design_name(design):
                logger.warning(f"Invalid design name rejected: {design}")
                abort(400, f"Invalid design name: {design}")

        logger.info(f"Running {report_type} dashboard: designs={selected_designs}, die={die}")

        try:
            if report_type == "timing":
                generated = run_chip(
                    cwd=Config.CWD_BASE_TIMING,
                    die=die,
                    outdir=Config.OUTDIR,
                    designs=selected_designs
                )
            else:  # Power dashboard
                generated = run_power(
                    cwd=Config.CWD_BASE_POWER,
                    outdir=Config.OUTDIR,
                    designs=selected_designs
                )

            if not generated:
                logger.error("No dashboard generated - empty result")
                abort(500, "No dashboard generated")

            return render_template(
                "index.html",
                designs_timing=designs_timing,
                designs_power=designs_power,
                generated=generated,
                comparison=(len(generated) > 1),
                done=True,
                report_type=report_type
            )
        except Exception as e:
            logger.error(f"Error generating dashboard: {e}", exc_info=True)
            abort(500, f"Error generating dashboard: {str(e)}")

    return render_template(
        "index.html",
        designs_timing=designs_timing,
        designs_power=designs_power,
        done=False
    )

# --------------------------------------------------
# Serve generated dashboards
# --------------------------------------------------
@app.route("/files/<path:filename>")
def files(filename):
    """Serve generated HTML files with security checks."""
    # Security: Only allow HTML files
    if not filename.endswith(".html"):
        abort(404)
    
    # Security: Prevent path traversal
    if '..' in filename or '/' in filename or '\\' in filename:
        logger.warning(f"Path traversal attempt detected: {filename}")
        abort(403)
    
    try:
        return send_from_directory(Config.OUTDIR, filename)
    except FileNotFoundError:
        logger.warning(f"File not found: {filename}")
        abort(404)
    except Exception as e:
        logger.error(f"Error serving file {filename}: {e}", exc_info=True)
        abort(500)

# --------------------------------------------------
# Error Handlers
# --------------------------------------------------
@app.errorhandler(400)
def bad_request(error):
    """Handle 400 Bad Request errors."""
    return render_template("index.html", 
                         designs_timing=list_designs(Config.CWD_BASE_TIMING),
                         designs_power=list_designs(Config.CWD_BASE_POWER),
                         done=False,
                         error_message=str(error)), 400


@app.errorhandler(404)
def not_found(error):
    """Handle 404 Not Found errors."""
    return render_template("index.html",
                         designs_timing=list_designs(Config.CWD_BASE_TIMING),
                         designs_power=list_designs(Config.CWD_BASE_POWER),
                         done=False,
                         error_message="File not found"), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 Internal Server Error."""
    logger.error(f"Internal server error: {error}", exc_info=True)
    return render_template("index.html",
                         designs_timing=list_designs(Config.CWD_BASE_TIMING),
                         designs_power=list_designs(Config.CWD_BASE_POWER),
                         done=False,
                         error_message="An internal error occurred. Please check the logs."), 500


# --------------------------------------------------
# Main
# --------------------------------------------------
if __name__ == "__main__":
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)

