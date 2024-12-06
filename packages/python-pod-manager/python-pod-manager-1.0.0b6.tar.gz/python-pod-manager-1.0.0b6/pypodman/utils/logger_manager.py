import logging
from pathlib import Path
from typing import Optional, Dict

class LoggerManager:
    def __init__(self, default_path: Optional[str] = None, config: Dict = None):
        """Initialize LoggerManager with the path to the default log directory."""
        self.config = config

        # Set default values for logging configuration if not found
        self.log_level = self._get_log_level(self.config.get("log_level", "FATAL"))
        self.log_path = Path(self.config.get("log_path", default_path or Path.home() / "Pypodmanager/logs"))
        self.log_file = self.config.get("log_file", "Docker_Manager.log")

    def _get_log_level(self, level: str) -> int:
        """Convert log level string to logging level constant."""
        log_levels = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
            "FATAL": logging.FATAL,
        }
        # Default to FATAL if an invalid level is specified
        return log_levels.get(level.upper(), logging.FATAL)

    def configure_logging(self) -> None:
        """Configure logging based on provided configuration."""
        # Ensure the log path exists
        self.log_path.mkdir(parents=True, exist_ok=True)
        
        log_file_path = self.log_path / self.log_file

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
