import logging
import os
from appdirs import user_log_dir

# Check if logging is enabled
logging_enabled = os.getenv("LOGGING", "1") == "1"

# Get custom log directory from environment or use platform-specific default
default_log_dir = user_log_dir(appname="subdeloc_tools", appauthor="delocalizer")
log_dir = os.getenv("LOG_DIR", default_log_dir)

# Ensure the log directory exists
os.makedirs(log_dir, exist_ok=True)

# Define the log file path
log_file = os.path.join(log_dir, "debug.log")

if logging_enabled:
    # Get the logging level from the .env file (default to DEBUG if not set)
    log_level = os.getenv("LOG_LEVEL", "DEBUG").upper()

    # Configure the logger
    logging.basicConfig(
        filename=log_file,  # Log to a file
        level=getattr(logging, log_level, logging.DEBUG),  # Set level dynamically
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Log format
    )

    # Create a logger instance
    logger = logging.getLogger("my_project_logger")
else:
    # Create a dummy logger that does nothing
    class DummyLogger:
        def debug(self, *args, **kwargs): pass
        def info(self, *args, **kwargs): pass
        def warning(self, *args, **kwargs): pass
        def error(self, *args, **kwargs): pass
        def critical(self, *args, **kwargs): pass

    logger = DummyLogger()
