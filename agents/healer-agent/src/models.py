from typing import Literal
from pydantic import BaseModel

class RemediationAction(BaseModel):
    diagnosis: str
    action: Literal["restart", "log_only"] # We can add "scale", "rollback", etc., later
    target_container: str