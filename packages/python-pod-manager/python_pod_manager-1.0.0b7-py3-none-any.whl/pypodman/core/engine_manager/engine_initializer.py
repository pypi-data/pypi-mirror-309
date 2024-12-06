from colorama import Fore, init
import subprocess
import logging
import shutil

init(autoreset=True)

class EngineInitializer:
    """Initialize and check the status of the container engine."""

    def __init__(self, config: str):
        self.config = config
        self.engine_name = self.config.get("name", "docker").lower()

    def initialize_engine(self) -> bool:
        """Initialize the Container Engine based on the configuration."""
        if self.check_engine(self.engine_name):
            logging.info(f"{self.engine_name.capitalize()} is installed and running.")
            print(Fore.GREEN + f"{self.engine_name.capitalize()} is installed and running.")
            return True
        else:
            logging.error(f"{self.engine_name.capitalize()} is not installed or not running.")
            print(Fore.RED + f"{self.engine_name.capitalize()} is not accessible.")
            response = input(Fore.YELLOW + f"Would you like to try starting it? (Y/n): ").strip().lower() or 'y'
            if response == 'y':
                if self.try_start_engine(self.engine_name.lower()):
                    logging.info(f"{self.engine_name.capitalize()} has been started successfully.")
                    print(Fore.GREEN + f"{self.engine_name.capitalize()} has been started successfully.")
                    return True
                else:
                    logging.error(f"Failed to start {self.engine_name}. Please check the service manually.")
                    print(Fore.RED + f"Failed to start {self.engine_name}. Please check the service manually.")
                    return False
            else:
                logging.info("User chose not to attempt starting the engine.")
                print(Fore.CYAN + "User chose not to attempt starting the engine.")
                return False

    def check_engine(self, engine_name: str) -> bool:
        """Check if the specified container engine is installed and accessible."""
        if engine_name not in ["podman", "docker"]:
            logging.error(f"Unsupported engine '{engine_name}' specified.")
            print(Fore.RED + f"Unsupported engine '{engine_name}' specified.")
            exit(1)

        if shutil.which(engine_name) is None:
            logging.error(f"{engine_name.capitalize()} is not installed.")
            print(Fore.RED + f"{engine_name.capitalize()} is not installed.")
            exit(1)

        try:
            result = subprocess.run(
                [engine_name, "ps"], capture_output=True, text=True
            )
            if result.returncode == 0:
                return True
            else:
                return False
        except Exception as e:
            logging.error(f"Error checking {engine_name}: {e}")
            print(Fore.RED + f"Error checking {engine_name}: {e}")
            exit(1)

    def try_start_engine(self, engine_name: str) -> bool:
        """Try to start the container engine service."""
        try:
            subprocess.run(["systemctl", "start", engine_name], check=True)
            return True
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to start {engine_name}: {e}")
            print(Fore.RED + f"Failed to start {engine_name}: {e}")
            exit(1)