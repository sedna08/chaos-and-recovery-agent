import docker
from src.logger import logger

class DockerExecutor:
    def __init__(self):
        try:
            self.client = docker.from_env()
        except Exception as e:
            logger.error({"error": str(e)}, "Failed to connect to Docker daemon")
            self.client = None

    def restart_container(self, container_name: str) -> bool:
        if not self.client:
            return False
            
        logger.info({"container": container_name}, "Initiating container restart")
        try:
            container = self.client.containers.get(container_name)
            container.restart()
            logger.info({"container": container_name}, "Container successfully restarted")
            return True
        except Exception as e:
            logger.error({"container": container_name, "error": str(e)}, "Failed to restart container")
            return False