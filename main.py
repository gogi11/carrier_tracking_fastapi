import uvicorn
from fastapi import FastAPI
from DTO.TrackingDTO import TrackingDTO
from carriers.DHLCarrier import DHLCarrier
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

carriers = {
    "dhl": DHLCarrier(),
    "other": None
}


@app.post("/track")
async def index(data: TrackingDTO):
    return carriers[data.carrier].get_tracking_info(data.barcode)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
