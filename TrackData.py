# tracking barcode, a carrier and carrier tracking credentials 
from pydantic import BaseModel

class TrackData(BaseModel):
    barcode: str
    carrier: str
    credentials: str