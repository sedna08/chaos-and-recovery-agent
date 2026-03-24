from src.loki_client import LokiPoller

def test_fetch_recent_errors(mocker):
    mock_get = mocker.patch("src.loki_client.httpx.get")
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "data": {
            "result": [
                {
                    "stream": {"container": "inventory-api"}, 
                    "values": [["1733828027704000000", "Exception: Connection timeout"]]
                }
            ]
        }
    }

    poller = LokiPoller(loki_url="http://mock-loki:3100")
    errors = poller.fetch_recent_errors(query='{container="inventory-api"} |= "Exception"')

    assert len(errors) == 1
    assert errors[0]["container"] == "inventory-api"
    assert "Connection timeout" in errors[0]["log"]