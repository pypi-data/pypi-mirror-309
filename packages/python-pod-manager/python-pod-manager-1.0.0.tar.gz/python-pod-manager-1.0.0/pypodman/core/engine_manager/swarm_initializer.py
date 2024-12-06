import subprocess
import psutil
import logging
from typing import Optional, Tuple


class SwarmInitializer:
    """Class responsible for initializing and managing Docker Swarm."""

    def get_default_network_interface(self) -> Tuple[Optional[str], Optional[str]]:
        """
        Get the default network interface with an IP address for Swarm initialization.
        
        Returns:
            Tuple containing the name of the interface and its IP address if found, otherwise (None, None).
        """
        logging.debug("Searching for a default network interface with a valid IP address.")
        for interface, addrs in psutil.net_if_addrs().items():
            if self.is_valid_interface(interface):
                for addr in addrs:
                    if addr.family in {2, 23}:  # 2 for IPv4, 23 for IPv6 on Windows
                        logging.info(f"Valid network interface found: {interface} with IP {addr.address}")
                        return interface, addr.address
        logging.error("No valid network interface with an IP address found.")
        return None, None

    def is_valid_interface(self, interface: str) -> bool:
        """
        Check if a network interface is valid for Swarm initialization.
        
        Args:
            interface: The name of the network interface.
        
        Returns:
            True if the interface is valid, False otherwise.
        """
        invalid_prefixes = ("vmnet", "br", "lo", "docker", "veth", "tun", "virbr")
        is_valid = not interface.startswith(invalid_prefixes)
        if not is_valid:
            logging.debug(f"Ignored interface: {interface} (invalid prefix)")
        return is_valid

    def init_swarm(self) -> None:
        """
        Initialize Docker Swarm using the default network interface.
        """
        interface, ip_address = self.get_default_network_interface()

        if not ip_address:
            logging.error("No suitable IP address found. Swarm initialization aborted.")
            return

        try:
            logging.info(f"Initializing Docker Swarm with advertise address: {ip_address}")
            self._run_swarm_command("init", ip_address)
        except subprocess.CalledProcessError as e:
            logging.error(f"Swarm initialization failed with subprocess error: {e}")
        except Exception as e:
            logging.error(f"Unexpected error during Swarm initialization: {e}")

    def _run_swarm_command(self, command_type: str, advertise_addr: Optional[str] = None) -> None:
        """
        Run a Docker Swarm command.

        Args:
            command_type: The type of Swarm command ('init' or 'leave').
            advertise_addr: The advertise address for the 'init' command.
        """
        if command_type == "init" and advertise_addr:
            command = ["docker", "swarm", "init", "--advertise-addr", advertise_addr]
        elif command_type == "leave":
            command = ["docker", "swarm", "leave", "--force"]
        else:
            logging.error("Invalid command type specified.")
            return

        try:
            logging.debug(f"Executing command: {' '.join(command)}")
            subprocess.run(command, check=True)
            logging.info(f"Swarm command '{command_type}' executed successfully.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error during Docker Swarm '{command_type}' command: {e}")
            raise

    def leave_swarm(self) -> None:
        """
        Leave the Docker Swarm.
        """
        try:
            logging.info("Attempting to leave Docker Swarm.")
            self._run_swarm_command("leave")
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to leave Swarm due to subprocess error: {e}")
        except Exception as e:
            logging.error(f"Unexpected error while leaving Swarm: {e}")
