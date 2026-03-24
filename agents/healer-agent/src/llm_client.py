from ollama import chat
from pydantic import ValidationError
from src.models import RemediationAction
from src.logger import logger

class LLMDecider:
    def __init__(self, model_name: str = "llama3.2"):
        self.model_name = model_name

    def analyze_error(self, error_log: str, container_name: str) -> RemediationAction | None:
        prompt = (
            f"You are an autonomous SRE agent managing a Dockerized environment.\n"
            f"The container '{container_name}' threw this error: \n{error_log}\n\n"
            f"Determine the root cause. If this is a transient infrastructure issue "
            f"(e.g., connection timeout, memory leak, deadlock) that can be temporarily mitigated "
            f"by restarting the service, set action to 'restart'.\n"
            f"If this is a syntax error or a hard-coded logical bug in the application code "
            f"(e.g., TypeError, KeyError, unhandled null value), you cannot fix it. "
            f"Provide a clear diagnosis of the bug and set action to 'log_only'."
        )
        
        logger.info({"container": container_name}, "Requesting LLM infrastructure triage")

        try:
            response = chat(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                format=RemediationAction.model_json_schema(),
                options={"temperature": 0.0} # Keep it deterministic
            )
            
            return RemediationAction.model_validate_json(response.message.content)
            
        except Exception as e:
            logger.error({"error": str(e)}, "LLM inference failed")
            return None