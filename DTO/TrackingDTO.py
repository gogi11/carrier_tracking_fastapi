from typing import Literal
from pydantic import BaseModel


class TrackingDTO(BaseModel):
    barcode: str
    carrier: Literal["dhl"]
    credentials: str
