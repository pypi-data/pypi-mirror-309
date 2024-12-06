import os
import sys
import logging
from typing import Optional
from ..varible_manager.name_manager import NameManager

class PathManager:
    @staticmethod
    def set_pythonpath(volume_path: str) -> None:
        """Set or update the PYTHONPATH environment variable to include the given volume path.

        Args:
            volume_path (str): The path to add to PYTHONPATH.
        
        Returns:
            None
        """
        original_path: Optional[str] = os.environ.get('PYTHONPATH', '')
        path_separator: str = ';' if os.name == 'nt' else ':'
        new_path: str = f"{volume_path}{path_separator}{original_path}" if original_path else volume_path
        
        # Update environment variable and sys.path for runtime imports
        os.environ['PYTHONPATH'] = new_path
        if volume_path not in sys.path:
            sys.path.insert(0, volume_path)
        
        logging.info(f"PYTHONPATH updated with volume path: {volume_path}")
        logging.debug(f"Full PYTHONPATH: {new_path}")

    def configure_paths(self, pod_name: str, base_path: str) -> None:
        """Configure paths for a pod by generating and setting the PYTHONPATH.

        Args:
            pod_name (str): Name of the pod.
            base_path (str): The base directory path where the pod libraries are stored.

        Returns:
            None
        """
        volume_path: str = self.get_volume_path(pod_name, base_path)
        self.set_pythonpath(volume_path)
        logging.info(f"Paths configured for pod '{pod_name}' with base path '{base_path}'.")

    def get_volume_path(self, pod_name: str, base_path: str) -> str:
        """Generate the volume path for a pod and ensure that the path exists.

        Args:
            pod_name (str): Name of the pod.
            base_path (str): The base directory path where the pod libraries are stored.

        Returns:
            str: The full path to the pod's volume.
        """
        volume_path: str = os.path.join(base_path, 'libs', NameManager()._format_library_name(pod_name))
        
        try:
            os.makedirs(volume_path, exist_ok=True)
            logging.info(f"Volume path '{volume_path}' created or verified.")
        except OSError as e:
            logging.error(f"Failed to create or access volume path '{volume_path}': {e}")
            raise
        
        return volume_path
    
    def get_mount_path(self, pod_name:str, working_dir:str) -> str:
        mount_path: str = os.path.join(working_dir, 'libs', NameManager()._format_library_name(pod_name))
        return mount_path
    
