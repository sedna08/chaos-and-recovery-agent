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
    
    # Query 1: The standard application error logs
    app_logql = '{container=~"inventory-api|store-frontend"} |= "Exception"'
    
    # Query 2: The new Telegraf metric logs (filtering for > 90% CPU usage)
    # Updated OODA Loop Query
    # 1. Select the debug stream
    # 2. Parse the key-value pairs (logfmt)
    # 3. Filter by the name we moved into the body
    # 4. Check the usage threshold
    metric_logql = '{job="debug_metrics"} | logfmt | container_name =~ "inventory-api|store-frontend" | usage_percent >= 90'

    while True:
        # Fetch both streams
        app_errors = poller.fetch_recent_errors(app_logql)
        resource_spikes = poller.fetch_recent_errors(metric_logql)
        
        # Combine the context
        all_issues = app_errors + resource_spikes
        
        for issue in all_issues:
            container_name = issue.get("container", "inventory-api")
            diagnostic_payload = issue["log"]
            
            # The LLM now receives either a stack trace OR a JSON hardware metric
            decision = decider.analyze_error(diagnostic_payload, container_name)
            
            if decision and decision.action == "restart":
                logger.warning(
                    {"container": container_name, "diagnosis": decision.diagnosis}, 
                    "Intervening via Docker restart."
                )
                executor.restart_container(decision.target_container)
                
            elif decision and decision.action == "log_only":
                logger.error(
                    {"container": container_name, "investigation_result": decision.diagnosis}, 
                    "Intervention aborted. Engineer required."
                )
                
        time.sleep(15)

if __name__ == "__main__":
    run_healer_agent()