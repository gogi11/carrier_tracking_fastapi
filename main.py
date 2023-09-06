import uvicorn
from fastapi import FastAPI

from TrackData import TrackData
from DHLCarrier import DHLCarrier
from dotenv import load_dotenv


load_dotenv()
app = FastAPI()



@app.get("/")
async def index():
   return {"message": "Hello World"}


@app.post("/track")
async def index(data: TrackData):
   carrier = DHLCarrier()
   return carrier.get_tracking_info(data.barcode)


if __name__ == "__main__":
   uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)