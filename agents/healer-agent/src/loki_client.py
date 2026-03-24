import httpx
from src.logger import logger

class LokiPoller:
    def __init__(self, loki_url: str = "http://localhost:3100"):
        self.loki_url = loki_url

    def fetch_recent_errors(self, query: str) -> list[dict]:
        endpoint = f"{self.loki_url}/loki/api/v1/query_range"
        payload = {"query": query, "limit": 10}
        
        logger.info({"query": query}, "Polling Loki for errors")
        
        try:
            response = httpx.get(endpoint, params=payload, timeout=10.0)
            response.raise_for_status()
            data = response.json()
            
            results = []
            
            for result in data.get("data", {}).get("result", []):
                container_name = result.get("stream", {}).get("container", "unknown")
                for value in result.get("values", []):
                    results.append({"container": container_name, "log": value[1]})
                    
            return results
        except Exception as e:
            logger.error({"error": str(e)}, "Failed to fetch logs from Loki")
            return []