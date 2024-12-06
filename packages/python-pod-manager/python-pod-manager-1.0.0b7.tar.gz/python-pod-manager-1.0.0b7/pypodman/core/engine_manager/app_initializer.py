import os
import sys
import logging
from typing import Optional

from .engine_initializer import EngineInitializer
from ..varible_manager.path_manager import PathManager
from ..pod_manager.pod_manager import PodManager
from ..pod_manager.service_manager import ServiceManager
from ...utils.config_loader import ConfigLoader
from ...utils.logger_manager import LoggerManager
from ..pod_manager.isolaton_manager import IsolatedPodManager
from ..varible_manager.name_manager import NameManager
from ..pod_manager.app_manager import AppManager
from ...utils.thread_manager import ThreadManager

DEFAULT_PATH = os.path.expanduser("~/Pypodmanager")


class AppInitializer:
    """Main application class for managing Docker pods."""

    def __init__(
        self, config_path: Optional[str] = None, cwd: Optional[str] = None
    ) -> None:
        """Initialize the DockerManagerApp."""
        self._initialize_components(config_path=config_path, cwd=cwd)
        self._set_default_paths()
        self._load_pod_settings()
        self.isolation_config = self.config.get("isolation", {})
        self.isolated_pod_manager = IsolatedPodManager(self.isolation_config)
        self.name_manager = NameManager()
        self.thread_manager = ThreadManager()  # Initialize the thread manager
        logging.info("DockerManagerApp initialized successfully.")

    def _initialize_components(
        self, config_path: Optional[str], cwd: Optional[str]
    ) -> None:
        """Initialize components and load configuration."""
        try:
            self.config_loader = ConfigLoader(config_path=config_path, cwd=cwd)
            deployment_config = self.config_loader.get_deployment_config()
            self.app_manager = AppManager(config=deployment_config)
            self.config = self.config_loader.config
            self.path_manager = PathManager()
            self.pod_manager = PodManager()
            self.service_manager = ServiceManager()
            self.library_names = self.config_loader.get_library_names()
        except Exception as e:
            logging.exception("Failed to initialize components.")
            raise

    def _set_default_paths(self) -> None:
        """Set default paths for host and pod mounts."""
        mount_config = self.config.get("mount", {})
        self.host_mount_path = mount_config.get("host_mount_path", DEFAULT_PATH)
        self.pod_mount_path = mount_config.get("pod_mount_path", "/app")
        logging.info(
            f"Default paths set: host_mount_path={self.host_mount_path}, pod_mount_path={self.pod_mount_path}"
        )

    def _load_pod_settings(self) -> None:
        """Load pod settings from the configuration."""
        library_pod_config = self.config.get("library_pod", {})
        self.pod_name = library_pod_config.get("pod_name", "my_pod")
        self.version = library_pod_config.get("version", "latest")
        self.base_image = library_pod_config.get("base_image", "python:latest")
        self.working_dir = library_pod_config.get("working_dir", "/app")
        self.dedicated_pod = library_pod_config.get("dedicated_pod", False)
        self.commands = self.config.get("commands", [])
        deployment_config = self.config.get("deployment", {})
        self.compose_file = deployment_config.get("compose_file", "docker-compose.yml")
        engine_config = self.config.get("engine", {})
        self.rebuild = engine_config.get("rebuild", False)

        logging.info(
            f"Pod settings loaded: pod_name={self.pod_name}, version={self.version}, "
            f"image_name={self.base_image}, working_dir={self.working_dir}, commands={self.commands}, "
            f"compose_file={self.compose_file}, rebuild={self.rebuild}, dedicated_pod={self.dedicated_pod}"
        )

    def start_pods(self) -> None:
        """Start pods based on the configuration."""
        logging.info(f"Starting pods; dedicated_pod is set to {self.dedicated_pod}.")
        try:
            if self.dedicated_pod:
                self._start_multiple_pods()
            else:
                self._start_single_pod()

            self.thread_manager.wait_for_threads()
            self.app_manager.start_app()

            # Initialize thread manager to start the isolated pod in a separate thread.
            if self.isolation_config.get("enabled"):
                self.isolated_pod_manager._start_isolated_pod(
                    self.isolation_config,
                    self.library_names if self.dedicated_pod else [f"{self.pod_name}"],
                    self.host_mount_path,
                    self.rebuild,
                )

                logging.info("Isolated pod started in background thread.")

            logging.info("Pods started successfully.")
        except Exception as e:
            logging.error(f"Error while starting pods: {e}")
            raise

    def _start_single_pod(self) -> None:
        """Start a single pod based on the rebuild setting."""
        if not self.rebuild:
            logging.info(
                f"Rebuild is set to False. Skipping the build for pod '{self.pod_name}'."
            )
            self._configure_paths(self.pod_name)
            self.thread_manager.start_thread(
                target=self.service_manager.single_pod_service_config,
                args=(
                    self.pod_name,
                    self.version,
                    self.host_mount_path,
                    self.pod_mount_path,
                    self.compose_file,
                ),
            )
            return

        logging.info(f"Starting a single pod: {self.pod_name}")
        self.thread_manager.start_thread(
            target=self.pod_manager.build_pod,
            args=(
                self.library_names,
                self.base_image,
                self.working_dir,
                self.pod_name,
                self.commands,
            ),
            on_finish=lambda: self.thread_manager.start_thread(
                target=self.service_manager.single_pod_service_config,
                args=(
                    self.pod_name,
                    self.version,
                    self.host_mount_path,
                    self.pod_mount_path,
                    self.compose_file,
                ),
            ),
        )
        self._configure_paths(self.pod_name)

    def _start_multiple_pods(self) -> None:
        """Start multiple pods based on the rebuild setting."""
        if not self.rebuild:
            logging.info(
                "Rebuild is set to False. Skipping the build for multiple pods."
            )
            self._configure_and_launch_multi_pod_services()
            return

        logging.info(f"Starting multiple pods for libraries: {self.library_names}")
        self.thread_manager.start_thread(
            target=self.pod_manager.build_multiple_pods,
            args=(
                self.library_names,
                self.base_image,
                self.working_dir,
                self.commands,
            ),
            on_finish=lambda: self._configure_and_launch_multi_pod_services(),
        )

    def _configure_and_launch_multi_pod_services(self) -> None:
        """Configure paths for multiple pods and start their services."""
        for lib_name in self.library_names:
            formatted_name = self.name_manager._format_library_name(lib_name)
            self._configure_paths(formatted_name)
            logging.info(f"Configured paths for library pod '{formatted_name}'")
        self.thread_manager.start_thread(
            target=self.service_manager.multi_pod_service_config,
            args=(
                self.library_names,
                self.version,
                self.host_mount_path,
                self.pod_mount_path,
                self.compose_file,
            ),
        )

    def _configure_paths(self, pod_name: str) -> None:
        """Configure paths for a given pod."""
        try:
            self.path_manager.configure_paths(pod_name, self.host_mount_path)
            logging.info(f"Paths configured for pod '{pod_name}'.")
        except Exception as e:
            logging.error(f"Error configuring paths for pod '{pod_name}': {e}")
            raise

    def check_engine(self) -> None:
        """Check and initialize the engine."""
        engine_config = self.config_loader.get_engine_config()
        engine_initializer = EngineInitializer(engine_config)
        try:
            if engine_initializer.initialize_engine():
                logging.info("Engine started successfully.")
            else:
                logging.error("Engine not started. Exiting.")
                sys.exit(1)
        except Exception as e:
            logging.error(f"Error during engine initialization: {e}")
            sys.exit(1)

    def configure_logging(self) -> None:
        """Configure application logging."""
        try:
            logging_config = self.config_loader.get_additional_config().get(
                "logging", {}
            )
            log_manager = LoggerManager(DEFAULT_PATH, logging_config)
            log_manager.configure_logging()
            logging.info("Logging configured successfully.")
        except Exception as e:
            logging.error(f"Error configuring logging: {e}")
            raise

    def run(self) -> None:
        """Run the DockerManagerApp."""
        self.configure_logging()
        self.check_engine()
        logging.info("DockerManagerApp run started.")
        try:
            self.start_pods()
            logging.info("DockerManagerApp run completed successfully.")
        except Exception as e:
            logging.error(f"Error during DockerManagerApp run: {e}")
            raise
