import logging
import yaml
from ..varible_manager.path_manager import PathManager
from ..varible_manager.name_manager import NameManager
from typing import Dict, List, OrderedDict


class ServiceManager:
    def __init__(self):
        self.path_manager = PathManager()
        self.name_manager = NameManager()
        logging.debug("Initialized ServiceManager with PathManager.")

    def create_service_definition(
        self, pod_name: str, image_name: str, volume_name: str, pod_mount_path: str
    ) -> Dict[str, Dict]:
        """Create a service definition for a pod.
        Args:
            pod_name (str): Name of the pod.
            image_name (str): Docker image name.
            volume_name (str): Name of the volume.
            pod_mount_path (str): Mount path for the pod.

        Returns:
            dict: Service definition for the pod.
        """
        service_def = {
            pod_name: {
                "image": image_name,
                "volumes": [f"{volume_name}:{pod_mount_path}"],
                "deploy": {
                    "replicas": 1
                },  # Default to one replica; adjust as necessary
            }
        }
        logging.debug(f"Service definition created for pod '{pod_name}': {service_def}")
        return service_def

    def create_volume_definition(
        self, volume_name: str, base_path: str
    ) -> Dict[str, Dict]:
        """Create a volume definition for a pod.
        Args:
            volume_name (str): Name of the volume.
            base_path (str): Base path for the volume.

        Returns:
            dict: Volume definition for the pod.
        """
        volume_def = {
            volume_name: {
                "driver": "local",
                "driver_opts": {
                    "device": base_path,
                    "o": "bind",
                    "type": "none",
                },
            }
        }
        logging.debug(
            f"Volume definition created for volume '{volume_name}': {volume_def}"
        )
        return volume_def
    
    def create_isolated_service_definition(
        self,
        isolated_pod_name: str,
        image_name: str,
        library_names: List[str],
        pod_mount_path: str,
        host_mount_path: str
    ) -> Dict[str, Dict]:
        """Create a service definition for an isolated pod with mounted libraries.
        
        Args:
            isolated_pod_name (str): Name of the isolated pod.
            image_name (str): Docker image name.
            library_names (List[str]): List of other pods' libraries to mount.
            pod_mount_path (str): Mount path for the pod.
            host_mount_path (str): Host mount path for libraries.

        Returns:
            dict: Service definition for the isolated pod.
        """
        # Create the base service definition for the isolated pod
        volumes = [
            f"{self.path_manager.get_volume_path(pod, host_mount_path)}:{pod_mount_path}"
            for pod in library_names
        ]

        service_def = {
            isolated_pod_name: {
                "image": image_name,
                "volumes": volumes,
                "deploy": {
                    "replicas": 1
                }
            }
        }
        
        logging.debug(f"Isolated service definition created for '{isolated_pod_name}': {service_def}")
        return service_def

    def build_single_pod_service_config(
        self, custom_pod_name, version, host_mount_path, pod_mount_path
    ):
        """Generate Docker Compose config for a single pod.
        Args:
            custom_pod_name (str): Name of the custom pod.
            version (str): Version of the pod.
            host_mount_path (str): Host mount path.
            pod_mount_path (str): Mount path for the pod.

        Returns:
            dict: Docker Compose configuration for the single pod.
        """
        volume_name = self.name_manager._pod_lib_name(custom_pod_name)
        volume_path = self.path_manager.get_volume_path(
            custom_pod_name, host_mount_path
        )
        logging.info(
            f"Building single pod service config for '{custom_pod_name}' with volume path '{volume_path}'."
        )

        services = self.create_service_definition(
            custom_pod_name, f"{custom_pod_name}:{version}", volume_name, pod_mount_path
        )
        volumes = self.create_volume_definition(volume_name, volume_path)

        # Use OrderedDict to ensure "version" key is at the top
        compose_config = OrderedDict()
        compose_config["services"] = services
        compose_config["volumes"] = volumes

        logging.debug(f"Single pod Docker Compose configuration: {compose_config}")
        return compose_config

    def build_multi_pod_service_config(
        self,
        library_names: List[str],
        version: str,
        host_mount_path: str,
        pod_mount_path: str,
    ) -> Dict:
        """Generate Docker Compose config for multiple pods.
        Args:
            library_names (List[str]): List of library names.
            version (str): Version of the pods.
            host_mount_path (str): Host mount path.
            pod_mount_path (str): Mount path for the pods.

        Returns:
            dict: Docker Compose configuration for the multiple pods
        """
        logging.info("Building multi-pod service config.")

        services = {}
        volumes = {}

        for pod_name in library_names:
            sanitized_pod_name = self.name_manager._format_library_name(pod_name)
            volume_name = self.name_manager._pod_lib_name(sanitized_pod_name)
            volume_path = self.path_manager.get_volume_path(
                sanitized_pod_name, host_mount_path
            )

            logging.debug(
                f"Creating service and volume for '{sanitized_pod_name}' with volume path '{volume_path}'."
            )

            services.update(
                self.create_service_definition(
                    sanitized_pod_name,
                    f"{sanitized_pod_name}:{version}",
                    volume_name,
                    pod_mount_path,
                )
            )
            volumes.update(self.create_volume_definition(volume_name, volume_path))

        compose_config = {"services": services, "volumes": volumes}
        logging.debug(
            f"Generated multi-pod Docker Compose configuration: {compose_config}"
        )
        return compose_config

    def single_pod_service_config(
        self,
        custom_pod_name: str,
        version: str,
        host_mount_path: str,
        pod_mount_path: str,
        compose_file: str,
    ):
        """Create and write Docker Compose config for a single pod.
        Args:
            custom_pod_name (str): Name of the custom pod.
            version (str): Version of the pod.
            host_mount_path (str): Host mount path.
            pod_mount_path (str): Mount path for the pod.
            compose_file (str): Path to write the Docker Compose file.

        Returns:
            None
        """
        logging.info(
            f"Creating Docker Compose config for single pod '{custom_pod_name}'."
        )
        compose_config = self.build_single_pod_service_config(
            custom_pod_name, version, host_mount_path, pod_mount_path
        )
        self.write_compose_file(compose_config, compose_file)

    def multi_pod_service_config(
        self,
        library_names: List[str],
        version: str,
        host_mount_path: str,
        pod_mount_path: str,
        compose_file: str,
    ):
        """Create and write Docker Compose config for multiple pods.
        Args:
            library_names (List[str]): List of library names.
            version (str): Version of the pods.
            host_mount_path (str): Host mount path.
            pod_mount_path (str): Mount path for the pods.
            compose_file (str): Path to write the Docker Compose file.
        
        Returns:
            None
        """
        logging.info("Creating Docker Compose config for multiple pods.")
        compose_config = self.build_multi_pod_service_config(
            library_names, version, host_mount_path, pod_mount_path
        )
        self.write_compose_file(compose_config, compose_file)

    def write_compose_file(self, compose_config, compose_file):
        """Write Docker Compose configuration to a file.
        Args:
            compose_config (dict): Docker Compose configuration.
            compose_file (str): Path to write the Docker Compose file.

        Returns:
            None
        """
        try:
            # Convert OrderedDict to a standard dictionary
            if isinstance(compose_config, OrderedDict):
                compose_config = dict(compose_config)

            with open(compose_file, "w") as file:
                yaml.dump(
                    compose_config, file, default_flow_style=False, sort_keys=False
                )
            logging.info(f"Docker Compose file successfully written: {compose_file}")
        except (OSError, yaml.YAMLError) as e:
            logging.error(
                f"Failed to write Docker Compose file: {compose_file}. Error: {e}"
            )
