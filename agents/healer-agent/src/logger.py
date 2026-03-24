import logging
import json

class AgentLogger:
    def __init__(self, name: str):
        self._logger = logging.getLogger(name)
        logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

    def info(self, payload: dict, msg: str) -> None:
        self._logger.info(f"{msg} | payload={json.dumps(payload)}")

    def error(self, payload: dict, msg: str) -> None:
        self._logger.error(f"{msg} | payload={json.dumps(payload)}")
        
    def warning(self, payload: dict, msg: str) -> None:
        self._logger.warning(f"{msg} | payload={json.dumps(payload)}")

logger = AgentLogger("healer-agent")