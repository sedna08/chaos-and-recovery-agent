from src.sandbox import ExecutionSandbox

def test_sandbox_tests_pass(mocker):
    # Setup: Mock subprocess to simulate passing pytest
    mock_run = mocker.patch("src.sandbox.subprocess.run")
    mock_result = mocker.Mock()
    mock_result.returncode = 0
    mock_result.stdout = "2 passed in 0.05s"
    mock_run.return_value = mock_result

    sandbox = ExecutionSandbox()
    
    # We pass a dummy original_file; the sandbox will create an ephemeral copy
    success, output = sandbox.apply_and_test(
        original_file="dummy_app.py", 
        patch_code="def fix(): pass", 
        test_cmd=["pytest", "test_dummy_app.py"]
    )

    assert success is True
    assert "2 passed" in output
    mock_run.assert_called_once()

def test_sandbox_tests_fail(mocker):
    # Setup: Mock subprocess to simulate a failing unit test assertion
    mock_run = mocker.patch("src.sandbox.subprocess.run")
    mock_result = mocker.Mock()
    mock_result.returncode = 1
    mock_result.stderr = "AssertionError: expected True but got False"
    mock_run.return_value = mock_result

    sandbox = ExecutionSandbox()
    success, output = sandbox.apply_and_test(
        original_file="dummy_app.py", 
        patch_code="def bad_fix(): return False", 
        test_cmd=["pytest", "test_dummy_app.py"]
    )

    assert success is False
    assert "AssertionError" in output