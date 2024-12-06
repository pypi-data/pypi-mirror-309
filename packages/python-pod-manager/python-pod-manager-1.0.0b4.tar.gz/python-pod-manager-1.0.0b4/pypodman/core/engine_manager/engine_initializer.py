import subprocess
import logging
import shutil
from ...utils.config_loader import ConfigLoader

class EngineInitializer:
    """Initialize and check the status of the container engine."""

    def __init__(self, config_path: str = None):
        self.config_loader = ConfigLoader(config_path)
        self.config = self.config_loader.get_engine_config()
        self.engine_name = self.config.get("name", "docker").lower()

    def initialize_engine(self) -> bool:
        """Initialize the Container Engine based on the configuration."""
        if self.check_engine(self.engine_name):
            logging.info(f"{self.engine_name.capitalize()} is installed and running.")
            return True
        else:
            logging.error(f"{self.engine_name.capitalize()} is not installed or not running.")
            return False

    def check_engine(self, engine_name: str) -> bool:
        """Check if the specified container engine is installed and running."""
        if engine_name not in ["podman", "docker"]:
            logging.error(f"Unsupported engine '{engine_name}' specified.")
            return False

        if shutil.which(engine_name) is None:
            logging.error(f"{engine_name.capitalize()} is not installed.")
            return False

        try:
            result = subprocess.run(
                [engine_name, "--version"], capture_output=True, text=True
            )
            if result.returncode == 0:
                logging.info(f"{engine_name.capitalize()} is installed and running.")
                return True
            else:
                logging.error(f"{engine_name.capitalize()} is not running.")
                return False
        except Exception as e:
            logging.error(f"Error checking {engine_name}: {e}")
            return False
