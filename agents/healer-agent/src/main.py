import time
from src.loki_client import LokiPoller
from src.llm_client import LLMDecider
from src.docker_client import DockerExecutor
from src.logger import logger

def run_healer_agent():
    logger.info({}, "Starting Infrastructure Healer Agent")
    
    poller = LokiPoller("http://localhost:3100")
    decider = LLMDecider("llama3.2")
    executor = DockerExecutor()
    
    logql_query = '{container=~"inventory-api|store-frontend"} |= "Exception"'

    while True:
        errors = poller.fetch_recent_errors(logql_query)
        
        for error in errors:
            container_name = error["container"]
            error_log = error["log"]
            
            decision = decider.analyze_error(error_log, container_name)
            
            if not decision:
                continue
                
            if decision.action == "restart":
                logger.warning(
                    {"container": container_name, "diagnosis": decision.diagnosis}, 
                    "Transient fault detected. Intervening via Docker restart."
                )
                executor.restart_container(decision.target_container)
                
            elif decision.action == "log_only":
                # The agent correctly identifies it shouldn't touch the code
                logger.error(
                    {"container": container_name, "investigation_result": decision.diagnosis}, 
                    "Application code fault detected. Intervention aborted. Engineer required."
                )
                
        time.sleep(15)

if __name__ == "__main__":
    run_healer_agent()