import pytest
import tempfile
from pathlib import Path
from src.ast_analyzer import ContextBuilder

@pytest.fixture
def sample_python_file():
    code = """
def successful_function():
    return True

def failing_function(x):
    # This line will throw a ZeroDivisionError
    return x / 0
    
class MyService:
    def process(self):
        pass
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(code)
        temp_path = f.name
        
    yield temp_path
    
    Path(temp_path).unlink()

def test_extract_failing_block_success(sample_python_file):
    builder = ContextBuilder()
    
    # Line 6 is inside `failing_function`
    block = builder.extract_failing_block(sample_python_file, 6)
    
    assert block is not None
    assert "def failing_function(x):" in block
    assert "return x / 0" in block
    assert "successful_function" not in block

def test_extract_failing_block_not_found():
    builder = ContextBuilder()
    block = builder.extract_failing_block("non_existent_file.py", 10)
    assert block is None