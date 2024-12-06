import logging
import os
from typing import Dict

class LoggerManager:
    def __init__(self, config: Dict):
        """Initialize LoggerManager with the path to the default log directory."""
        self.config = config

        # Set default values for logging configuration if not found
        self.log_level = self._get_log_level(self.config.get("log_level"))
        self.log_path = os.path.abspath(os.path.expanduser(self.config.get("log_path")))
        self.log_file = self.config.get("log_file")

    def _get_log_level(self, level: str) -> int:
        """Convert log level string to logging level constant."""
        log_levels = {
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "FATAL": logging.FATAL, # Default to FATAL if not specified. Its disable the logging
        }
        # Default to FATAL if an invalid level is specified
        return log_levels.get(level.upper(), logging.FATAL)

    def configure_logging(self) -> None:
        """Configure logging based on provided configuration."""
        # Ensure the log path exists
        os.makedirs(self.log_path, exist_ok=True)
        
        log_file_path = os.path.join(self.log_path, self.log_file)

        # Setup the file handler for logging
        handler = logging.FileHandler(log_file_path, mode='a')
        handler.setLevel(self.log_level)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        logger = logging.getLogger()
        logger.setLevel(self.log_level)

        # Remove existing StreamHandler if present (optional, depending on requirements)
        logger.handlers = [h for h in logger.handlers if not isinstance(h, logging.StreamHandler)]
        
        # Add the new file handler
        logger.addHandler(handler)

        logging.info(f"Logging configured with FileHandler at {log_file_path}")
