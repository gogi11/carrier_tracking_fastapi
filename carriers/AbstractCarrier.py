from abc import ABC, abstractmethod
import json
from fastapi import HTTPException
from requests import Response
from DTO.TraceyEventDTO import TraceyEventDTO


def get_tracey_mapping() -> dict[str, dict[str, TraceyEventDTO]]:
    with open("./filtered_events.json", "r") as json_file:
        return json.load(json_file)


class AbstractCarrier(ABC):
    def __init__(self, carrier_name: str) -> None:
        self.carrier_name = carrier_name

    @abstractmethod
    def get_api_response(self, tracking_number: str) -> Response:
        pass

    @abstractmethod
    def get_tracking_status(self, api_response: Response) -> str:
        pass

    def map_status(self, status: str):
        all_corriers_mapping = get_tracey_mapping()
        if self.carrier_name not in all_corriers_mapping:
            raise HTTPException(status_code=404, detail={
                                    "message": f"Courier '{self.carrier_name}' is not supported."})

        mappings = all_corriers_mapping[self.carrier_name]

        if status not in mappings:
            raise HTTPException(status_code=501, detail={
                                    "message": f"Unfortunately, we do not support this status type from {self.carrier_name}",
                                    "external_api_status": status})
        return mappings[status]

    def get_tracking_info(self, tracking_number: str) -> TraceyEventDTO:
        api_response = self.get_api_response(tracking_number)
        if api_response.status_code == 500:
            raise HTTPException(status_code=500,
                                detail=api_response.json())
        if api_response.status_code == 429:
            raise HTTPException(status_code=429,
                                detail={"message": "The daily limit of the external api has been reached. Please try again tomorrow."})
        if api_response.status_code == 404:
            raise HTTPException(status_code=404,
                                detail={"message": "Barcode not found. Please check the barcode and try again later."})
        status = self.get_tracking_status(api_response)
        return self.map_status(status)
