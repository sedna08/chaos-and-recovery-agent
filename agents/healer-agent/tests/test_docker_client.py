from src.docker_client import DockerExecutor

def test_restart_container_success(mocker):
    mock_docker_env = mocker.patch("src.docker_client.docker.from_env")
    mock_container = mocker.Mock()
    mock_docker_env.return_value.containers.get.return_value = mock_container

    executor = DockerExecutor()
    success = executor.restart_container("inventory-api")

    assert success is True
    mock_container.restart.assert_called_once()

def test_restart_container_not_found(mocker):
    mock_docker_env = mocker.patch("src.docker_client.docker.from_env")
    mock_docker_env.return_value.containers.get.side_effect = Exception("Container not found")

    executor = DockerExecutor()
    success = executor.restart_container("missing-container")

    assert success is False