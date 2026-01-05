"""
Configuration management for the Dashboard application.
Supports environment variables with fallback to defaults.
"""
import os
from pathlib import Path


class Config:
    """Application configuration."""
    
    # Base paths - can be overridden via environment variables
    CWD_BASE_TIMING = os.getenv("CWD_BASE_TIMING", "/asic_work/ewang/esf/old_work_areas")
    CWD_BASE_POWER = os.getenv("CWD_BASE_POWER", "/asic_work/jchang/esf/power_released/")
    OUTDIR = os.getenv("OUTDIR", "/asic_work/mkhan/website/tempo")
    LOGFILE = os.getenv("LOGFILE", "/asic_work/mkhan/website/logs/timing.log")
    
    # Flask settings
    HOST = os.getenv("FLASK_HOST", "127.0.0.1")
    PORT = int(os.getenv("FLASK_PORT", "8080"))
    DEBUG = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    
    # Security settings
    MAX_DESIGN_NAME_LENGTH = 200
    MAX_DIE_NAME_LENGTH = 50
    
    @classmethod
    def ensure_directories(cls):
        """Ensure required directories exist."""
        os.makedirs(cls.OUTDIR, exist_ok=True)
        log_dir = os.path.dirname(cls.LOGFILE)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
    
    @classmethod
    def validate_paths(cls):
        """Validate that configured paths exist (warn if not)."""
        import logging
        logger = logging.getLogger(__name__)
        
        if not os.path.isdir(cls.CWD_BASE_TIMING):
            logger.warning(f"Timing base directory does not exist: {cls.CWD_BASE_TIMING}")
        if not os.path.isdir(cls.CWD_BASE_POWER):
            logger.warning(f"Power base directory does not exist: {cls.CWD_BASE_POWER}")

