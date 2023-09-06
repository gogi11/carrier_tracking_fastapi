from typing import Literal
from pydantic import BaseModel

class TraceyEvent(BaseModel):
    carrierException: str | None
    exceptionType: Literal["warning",  "error", "success"]
    isReturned: bool 
    phase: str
    subPhase: str
    traceyEvent: str

