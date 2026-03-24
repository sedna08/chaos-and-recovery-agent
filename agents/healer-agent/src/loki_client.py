import time
import httpx
from src.logger import logger

class LokiPoller:
    def __init__(self, loki_url: str = "http://localhost:3100"):
        self.loki_url = loki_url
        # Initialize the cursor to the current time so we don't process historical logs on startup
        self.last_poll_time_ns = time.time_ns()

    def fetch_recent_errors(self, query: str) -> list[dict]:
        endpoint = f"{self.loki_url}/loki/api/v1/query_range"
        payload = {
            "query": query, 
            "limit": 10,
            "start": self.last_poll_time_ns
        }
        
        logger.info({"query": query}, "Polling Loki for errors")
        
        try:
            response = httpx.get(endpoint, params=payload, timeout=10.0)
            response.raise_for_status()
            data = response.json()
            
            results = []
            max_ts = self.last_poll_time_ns
            
            for result in data.get("data", {}).get("result", []):
                container_name = result.get("stream", {}).get("container", "unknown")
                for value in result.get("values", []):
                    ts_str, log_msg = value[0], value[1]
                    
                    try:
                        ts_int = int(ts_str)
                        if ts_int >= max_ts:
                            max_ts = ts_int + 1
                    except ValueError:
                        logger.error({"timestamp": ts_str}, "Invalid timestamp format from Loki")
                        
                    results.append({"container": container_name, "log": log_msg})
            
            # Update state for the next polling cycle
            self.last_poll_time_ns = max_ts
            return results
            
        except Exception as e:
            logger.error({"error": str(e)}, "Failed to fetch logs from Loki")
            return []