"""
Logging configuration for Skrunkly Draw application.

Usage:
    from utils.logger import get_logger
    
    logger = get_logger(__name__)
    logger.info("User logged in successfully")
    logger.debug("Debug information")
    logger.error("An error occurred")

Enable debug mode with environment variable:
    export SKRUNKLY_LOG_LEVEL=DEBUG
    
Default log levels:
    - INFO (production)
    - DEBUG (development with SKRUNKLY_LOG_LEVEL=DEBUG)

Log file location:
    .streamlit/logs/app.log
"""

import logging
import logging.handlers
import os
from pathlib import Path

# Create logs directory if it doesn't exist
LOGS_DIR = Path(__file__).parent.parent / ".streamlit" / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# Log file path
LOG_FILE = LOGS_DIR / "app.log"

# Get log level from environment variable (default: INFO)
LOG_LEVEL = os.getenv("SKRUNKLY_LOG_LEVEL", "INFO").upper()

# Validate log level
VALID_LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
if LOG_LEVEL not in VALID_LEVELS:
    LOG_LEVEL = "INFO"


def get_logger(name: str) -> logging.Logger:
    """
    Get a configured logger instance.
    
    Args:
        name: Logger name (typically __name__ of the calling module)
        
    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Only configure if not already configured
    if not logger.handlers:
        # Set log level
        logger.setLevel(LOG_LEVEL)
        
        # Create formatters
        detailed_formatter = logging.Formatter(
            '[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # File handler with rotation
        file_handler = logging.handlers.RotatingFileHandler(
            LOG_FILE,
            maxBytes=10*1024*1024,  # 10 MB
            backupCount=5
        )
        file_handler.setLevel(LOG_LEVEL)
        file_handler.setFormatter(detailed_formatter)
        logger.addHandler(file_handler)
        
        # Console handler (optional - add to stderr)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(LOG_LEVEL)
        console_handler.setFormatter(detailed_formatter)
        
        # Only add console handler if DEBUG is enabled
        if LOG_LEVEL == "DEBUG":
            logger.addHandler(console_handler)
    
    return logger


def log_event(category: str, event: str, details: dict = None, level: str = "INFO") -> None:
    """
    Log an event with category and details.
    
    Args:
        category: Event category (e.g., "AUTH", "NAV", "STATE")
        event: Event description
        details: Optional dictionary of additional details
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    logger = get_logger(__name__)
    
    if details:
        message = f"[{category}] {event} - {details}"
    else:
        message = f"[{category}] {event}"
    
    log_method = getattr(logger, level.lower(), logger.info)
    log_method(message)


def log_auth_event(event: str, user_email: str = None, status: str = None) -> None:
    """
    Log authentication events.
    
    Args:
        event: Event description (e.g., "Login attempt")
        user_email: User's email (optional, for privacy: can be masked)
        status: Status (e.g., "success", "error")
    """
    details = {}
    if user_email:
        details["email"] = user_email
    if status:
        details["status"] = status
    
    log_event("AUTH", event, details if details else None)


def log_navigation_event(event: str, page: str = None, logged_in: bool = None) -> None:
    """
    Log navigation events.
    
    Args:
        event: Event description (e.g., "Page access")
        page: Page name (e.g., "feed", "draw")
        logged_in: Whether user is logged in
    """
    details = {}
    if page:
        details["page"] = page
    if logged_in is not None:
        details["logged_in"] = logged_in
    
    log_event("NAV", event, details if details else None)


def log_session_change(key: str, value: str = None, level: str = "DEBUG") -> None:
    """
    Log session state changes.
    
    Args:
        key: Session key that changed
        value: New value (optional, for sensitive data use generic placeholder)
        level: Log level (default: DEBUG)
    """
    details = {"key": key}
    if value:
        details["value"] = value
    
    log_event("STATE", "Session change", details if details else None, level=level)


def log_redirect(from_page: str, to_page: str, reason: str = None) -> None:
    """
    Log page redirects.
    
    Args:
        from_page: Source page
        to_page: Destination page
        reason: Reason for redirect (e.g., "unauthorized", "login_complete")
    """
    details = {"from": from_page, "to": to_page}
    if reason:
        details["reason"] = reason
    
    log_event("REDIRECT", "Page redirect", details)


def log_error(category: str, error: str, exception: Exception = None) -> None:
    """
    Log error events.
    
    Args:
        category: Error category
        error: Error description
        exception: Optional exception object
    """
    logger = get_logger(__name__)
    
    if exception:
        logger.error(f"[{category}] {error}", exc_info=exception)
    else:
        logger.error(f"[{category}] {error}")


def get_log_file_path() -> str:
    """Get the path to the log file."""
    return str(LOG_FILE)


def is_debug_enabled() -> bool:
    """Check if debug logging is enabled."""
    return LOG_LEVEL == "DEBUG"
