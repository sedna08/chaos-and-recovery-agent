import ast
from pathlib import Path
from src.logger import logger

class ContextBuilder:
    def extract_failing_block(self, file_path: str, line_number: int) -> str | None:
        path = Path(file_path)
        if not path.exists():
            logger.error({"file": file_path}, "File not found for AST parsing")
            return None

        try:
            source = path.read_text(encoding="utf-8")
            tree = ast.parse(source)
        except SyntaxError as e:
            logger.error({"error": str(e), "file": file_path}, "Syntax error while parsing AST")
            return None
        except Exception as e:
            logger.error({"error": str(e)}, "Unexpected error reading file")
            return None

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                if hasattr(node, "lineno") and hasattr(node, "end_lineno"):
                    if node.lineno <= line_number <= node.end_lineno:
                        logger.info({"file": file_path, "node": node.name}, "Extracted context block")
                        return ast.get_source_segment(source, node)
        
        logger.warning({"file": file_path, "line": line_number}, "Could not find enclosing AST node")
        return None

    def query_rag_history(self, error_signature: str) -> list[str]:
        logger.info({"signature": error_signature}, "Querying vector DB for historical fixes")
        return []