import time
from src.loki_client import LokiPoller
from src.llm_client import LLMDecider
from src.docker_client import DockerExecutor
from src.logger import logger

def run_healer_agent():
    logger.info({}, "Starting Healer Agent Subsystem")
    
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
            
            if decision and decision.action == "restart":
                executor.restart_container(decision.target_container)
                
        time.sleep(15)

if __name__ == "__main__":
    run_healer_agent()