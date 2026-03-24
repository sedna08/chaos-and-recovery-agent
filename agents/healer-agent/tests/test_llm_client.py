from src.llm_client import LLMDecider
from src.models import RemediationAction

def test_analyze_error_returns_structured_action(mocker):
    mock_chat = mocker.patch("src.llm_client.chat")
    mock_response = mocker.Mock()
    mock_response.message.content = '{"rationale": "API is unresponsive", "action": "restart", "target_container": "inventory-api"}'
    mock_chat.return_value = mock_response

    decider = LLMDecider(model_name="llama3.2")
    decision = decider.analyze_error(error_log="Exception: Connection timeout", container_name="inventory-api")

    assert isinstance(decision, RemediationAction)
    assert decision.action == "restart"
    assert decision.target_container == "inventory-api"
    mock_chat.assert_called_once()