from ollama import chat
from pydantic import ValidationError
from src.models import RemediationAction
from src.logger import logger

class LLMDecider:
    def __init__(self, model_name: str = "llama3.2"):
        self.model_name = model_name

    def analyze_error(self, error_log: str, container_name: str) -> RemediationAction | None:
        prompt = (
            f"The container '{container_name}' has crashed with the following error:\n"
            f"{error_log}\n"
            f"Analyze the error. If the container requires a restart to recover, set action to 'restart'. "
            f"Provide your rationale."
        )
        
        logger.info({"container": container_name, "model": self.model_name}, "Requesting LLM remediation decision")

        try:
            response = chat(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                format=RemediationAction.model_json_schema(),
                options={"temperature": 0.0}
            )
            
            action = RemediationAction.model_validate_json(response.message.content)
            logger.info({"action": action.action, "target": action.target_container}, "LLM decision received")
            return action
            
        except ValidationError as e:
            logger.error({"error": str(e)}, "LLM returned malformed JSON schema")
            return None
        except Exception as e:
            logger.error({"error": str(e)}, "LLM inference failed")
            return None