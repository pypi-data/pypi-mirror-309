import os
import logging
import subprocess
from ..varible_manager.name_manager import NameManager

class PodManager:
    def create_dockerfile(
        self,
        pod_name: str,
        libraries: list[str],
        image_name: str,
        working_dir: str,
        commands: list[dict],
    ) -> str:
        """Generate a Dockerfile content string and return the file path.
        Args:
            pod_name (str): Name of the pod.
            libraries (list[str]): List of libraries to install.
            image_name (str): Base Docker image name.
            working_dir (str): Working directory for the pod.
            commands (list[dict]): List of commands to run in the Dockerfile.

        Returns:
            str: Path to the generated Dockerfile.
        """

        if isinstance(libraries, list):
            libraries = " ".join(libraries)

        formatted_commands = "\n".join(
            f"{cmd['name']} {cmd['command'].format(libraries=libraries, working_dir=working_dir)}"
            for cmd in commands
        )
        dockerfile_content = (
            f"FROM {image_name}\n" f"WORKDIR {working_dir}\n" f"{formatted_commands}\n"
        )
        dockerfile_path = os.path.join(os.getcwd(), pod_name, "Dockerfile")
        os.makedirs(os.path.dirname(dockerfile_path), exist_ok=True)

        try:
            with open(dockerfile_path, "w", encoding="utf-8") as dockerfile:
                dockerfile.write(dockerfile_content)
            logging.info(
                f"Dockerfile created for pod '{pod_name}' at {dockerfile_path}"
            )
        except (OSError, IOError) as e:
            logging.exception(f"Failed to create Dockerfile for '{pod_name}'")
            raise
        return dockerfile_path

    def build_pod(
        self,
        library: list[str],
        image_name: str,
        working_dir: str,
        pod_name: str,
        commands: list[dict],
    ):
        """Build a single Docker pod using the specified parameters.
        Args:
            library (list[str]): List of libraries to install.
            image_name (str): Base Docker image name.
            working_dir (str): Working directory for the pod.
            pod_name (str): Name of the pod.
            commands (list[dict]): List of commands to run in the Dockerfile.

        Returns:
            None
        """
        try:
            dockerfile_path = self.create_dockerfile(
                pod_name, library, image_name, working_dir, commands
            )
            logging.info("Initiating Docker build for pod: %s", pod_name)
            subprocess.run(
                ["docker", "build", "-t", pod_name, "-f", dockerfile_path, "."],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            logging.info("Docker build completed for pod: %s", pod_name)
        except subprocess.CalledProcessError as e:
            logging.error(
                "Docker build error for pod '%s': %s", pod_name, e.stderr.decode()
            )
            raise

    def build_multiple_pods(
        self,
        libraries: list[str],
        image_name: str,
        working_dir: str,
        commands: list[dict],
    ):
        """Build multiple Docker pods using the specified parameters.
        Args:
            libraries (list[str]): List of libraries to install.
            image_name (str): Base Docker image name.
            working_dir (str): Working directory for the pod.
            commands (list[dict]): List of commands to run in the Dockerfile.

        Returns:
            None
        """
        
        for library in libraries:
            pod_name = NameManager()._format_library_name(library)
            self.build_pod(library, image_name, working_dir, pod_name, commands)

    def run_pod(self, pod_name: str, volumes: list[str]):
        """Run a Docker pod using the specified parameters.
        Args:
            pod_name (str): Name of the pod.
            volumes (list[str]): List of volume mappings.

        Returns:
            None
        """
        try:
            volume_args = " ".join(volumes)
            logging.info("Starting Docker pod: %s", pod_name)
            subprocess.run(
                ["docker", "run", "-it", "--name", pod_name, volume_args, pod_name, "bash"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except subprocess.CalledProcessError as e:
            logging.error(
                "Docker run error for pod '%s': %s", pod_name, e.stderr.decode()
            )
            raise


    def stop_pod(self, pod_name: str):
        """Stop a Docker pod using the specified parameters.
        Args:
            pod_name (str): Name of the pod.

        Returns:
            None
        """
        try:
            logging.info("Stopping Docker pod: %s", pod_name)
            subprocess.run(
                ["docker", "stop", pod_name, "-f"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
        except subprocess.CalledProcessError as e:
            logging.error(
                "Docker stop error for pod '%s': %s", pod_name, e.stderr.decode()
            )
            raise

    
