import subprocess
import tempfile
from pathlib import Path
from src.logger import logger

class ExecutionSandbox:
    def apply_and_test(self, original_file: str, patch_code: str, test_cmd: list[str]) -> tuple[bool, str]:
        original_path = Path(original_file)
        
        logger.info({"file": original_file}, "Staging patch in ephemeral sandbox")
        
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            patched_file = temp_path / original_path.name
            
            try:
                patched_file.write_text(patch_code, encoding="utf-8")
            except Exception as e:
                logger.error({"error": str(e)}, "Failed to write patch to sandbox")
                return False, f"System Error: {str(e)}"

            try:
                result = subprocess.run(
                    test_cmd,
                    cwd=temp_dir,
                    capture_output=True,
                    text=True,
                    timeout=30.0
                )
                
                if result.returncode == 0:
                    logger.info({"exit_code": result.returncode}, "Validation tests passed")
                    return True, result.stdout
                else:
                    logger.warning({"exit_code": result.returncode}, "Validation tests failed")
                    return False, result.stderr or result.stdout
                    
            except subprocess.TimeoutExpired:
                logger.error({}, "Validation tests timed out")
                return False, "Execution timed out after 30 seconds."
            except Exception as e:
                logger.error({"error": str(e)}, "Sandbox execution exception")
                return False, f"Execution Exception: {str(e)}"