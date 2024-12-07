import pytest
from unittest.mock import patch, Mock
from uniworkflow import UniwWorkflow
from uniworkflow.exceptions import ProviderNotFoundError, WorkflowExecutionError
WORKFLOW_URL = "https://app4.evalsone.com/webhook/6f7b288e-1efe-4504-a6fd-660931327269"
API_KEY = "withfun7514"


@pytest.fixture
def mock_n8n_provider(monkeypatch):
    mock_provider = Mock()
    monkeypatch.setattr('uniworkflow.providers.n8n.N8nProvider', mock_provider)
    return mock_provider

def test_execute_workflow_successful(mock_n8n_provider):
    # Arrange
    expected_result = {
        "video_url": "......",
        "description": "..."
    }
    mock_n8n_provider.execute.return_value = expected_result, 200

    kwargs = {
        "workflow_url": WORKFLOW_URL,
        "method": "GET",
        # "data": {"url": "https://www.youtube.com/watch?v=VGjorrrxh2Y&t=4s"},
        "api_key": API_KEY
    }

    # Act
    result, response_data, status_code = UniwWorkflow.execute("n8n", **kwargs)
    print(response_data)
    print(result)
    # Assert
    assert isinstance(result, dict)
    # assert "video_url" in result
    # assert "description" in result
    assert status_code == 200

# def test_execute_workflow_error(mock_n8n_provider):
#     # Arrange
#     mock_n8n_provider.execute.side_effect = Exception("Workflow execution failed")

#     kwargs = {
#         "workflow_url": WORKFLOW_URL,
#         "method": "GET",
#         "data": {"topic": "Test Topic"},
#         "api_key": API_KEY
#     }

#     # Act & Assert
#     with pytest.raises(WorkflowExecutionError) as exc_info:
#         UniwWorkflow.execute("n8n", **kwargs)

#     assert str(exc_info.value) == "Error executing workflow: Workflow execution failed"

# def test_execute_workflow_missing_api_key():
#     # Arrange
#     kwargs = {
#         "workflow_url": WORKFLOW_URL,
#         "data": {"topic": "Test Topic"}
#     }

#     # Act & Assert
#     with pytest.raises(ValueError) as exc_info:
#         UniwWorkflow.execute("n8n", **kwargs)

#     assert str(exc_info.value) == "API key is required"

# def test_execute_workflow_invalid_provider():
#     # Arrange
#     kwargs = {
#         "workflow_url": "your_workflow_url",
#         "data": {"key": "value"},
#         "api_key": API_KEY
#     }

#     # Act & Assert
#     with pytest.raises(ProviderNotFoundError) as exc_info:
#         UniwWorkflow.execute("invalid_provider", **kwargs)

#     assert "Provider 'invalid_provider' not found" in str(exc_info.value)