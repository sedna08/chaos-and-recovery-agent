import time
from src.loki_client import LokiPoller

def test_fetch_recent_errors_updates_cursor(mocker):
    # 1. Arrange: Mock the initial system time
    initial_time_ns = 1700000000000000000
    mocker.patch("src.loki_client.time.time_ns", return_value=initial_time_ns)

    mock_get = mocker.patch("src.loki_client.httpx.get")
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "data": {
            "result": [
                {
                    "stream": {"container": "inventory-api"}, 
                    "values": [
                        # Provide logs out of order to ensure we parse the maximum value
                        ["1733828027704000000", "Exception: Connection timeout"],
                        ["1733828027704000005", "Exception: Another error"]
                    ]
                }
            ]
        }
    }

    poller = LokiPoller(loki_url="http://mock-loki:3100")
    assert poller.last_poll_time_ns == initial_time_ns

    # 2. Act
    errors = poller.fetch_recent_errors(query='{container="inventory-api"} |= "Exception"')

    # 3. Assert: Verify the 'start' param was injected into the request
    mock_get.assert_called_once()
    called_params = mock_get.call_args.kwargs["params"]
    assert called_params["start"] == initial_time_ns

    # Assert: Verify all errors were extracted
    assert len(errors) == 2
    assert errors[0]["container"] == "inventory-api"
    
    # Assert: Verify the high-water mark cursor updated to the highest timestamp + 1
    assert poller.last_poll_time_ns == 1733828027704000006

def test_fetch_recent_errors_handles_api_failure(mocker):
    # Ensure our failure state still returns an empty list and doesn't crash the loop
    mock_get = mocker.patch("src.loki_client.httpx.get", side_effect=Exception("Network error"))
    
    poller = LokiPoller(loki_url="http://mock-loki:3100")
    errors = poller.fetch_recent_errors(query='{container="inventory-api"} |= "Exception"')
    
    assert errors == []