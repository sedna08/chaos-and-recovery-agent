from pydantic import BaseModel

class RemediationAction(BaseModel):
    rationale: str
    action: str
    target_container: str