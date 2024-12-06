import logging
import time
from ..pod_manager.pod_manager import PodManager
from ..varible_manager.path_manager import PathManager
from ..varible_manager.name_manager import NameManager
from colorama import init, Fore

# Initialize colorama for cross-platform compatibility
init(autoreset=True)

class IsolatedPodManager:
    """Class for handling isolated pod configurations and setup."""

    def __init__(self, isolation_config):
        self.isolation_config = isolation_config
        self.pod_manager = PodManager()
        self.path_manager = PathManager()
        self.name_manager = NameManager()



    def _start_isolated_pod(self, isolation_config: dict, library_names: list, host_mount_path:str, rebuild:str) -> None:
        """Start a pod in isolated mode."""
        try:
            pod_name = isolation_config.get("name", "isolated_pod").lower()
            version = isolation_config.get("version", "latest")
            base_image = isolation_config.get("base_image", "ubuntu:latest")
            commands = isolation_config.get("commands", [])
            working_dir = isolation_config.get("working_dir", "/app")
            volumes = []
            paths = []

            for lib_name in library_names:
                formatted_name = self.name_manager._format_library_name(lib_name)
                volume_str = f"-v {self.path_manager.get_volume_path(formatted_name, host_mount_path)}:{self.path_manager.get_mount_path(formatted_name, working_dir)} \\\n"
                volumes.append(volume_str)
                paths.append(self.path_manager.get_mount_path(formatted_name, working_dir))

            volumes_str = " ".join(volumes)

            env_command = f'PYTHONPATH="{":".join(paths)}"'
            result = [{"name": "ENV", "command": env_command}]
            commands = result + commands
            if all([pod_name, version, base_image]) and rebuild:
                self.pod_manager.build_pod(
                    library=None,
                    image_name=base_image,
                    working_dir=working_dir,
                    pod_name=f"{pod_name}:{version}",
                    commands=commands,
                )
                self._print_isolated_pod_message(pod_name, version, volumes_str)
                logging.info(f"Isolated pod '{pod_name}:{version}' started successfully.")
            elif all([pod_name, version, base_image]) and not rebuild:
                self._print_isolated_pod_message(pod_name, version, volumes_str)
                logging.info(f"Isolated pod '{pod_name}:{version}' already exists. Skipping build.")
            else:
                logging.error("Isolation configuration is missing required fields.")
        except Exception as e:
            logging.error(f"Error in isolation mode: {e}")
            raise

    def _print_isolated_pod_message(self, pod_name: str, version: str, volumes_str: str) -> None:
        """Prints the command to run the isolated pod with some color formatting."""
        print(Fore.GREEN + f"\nYou can now work with the isolated pod:\n")
        print(Fore.CYAN + f"docker run -it --name isolated-container {volumes_str} {pod_name}:{version} bash")
        print(Fore.YELLOW + "\nWaiting for your input to finish...\nPress Ctrl+C to exit.")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print(Fore.RED + "\nProcess interrupted. Exiting the isolated pod session.")