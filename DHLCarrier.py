from abc import ABC, abstractmethod
import http.client
import json
import os
from TraceyEvent import TraceyEvent



class Carrier(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def get_api_headers(self) -> dict:
        pass

    @abstractmethod
    def get_tracking_URL(self, tracking_number: str) -> dict:
        pass
    
    @abstractmethod
    def convert_response_to_tracey_event(self, response) -> TraceyEvent:
        pass


class DHLCarrier(Carrier):
    def __init__(self) -> None:
        self.url = "https://api-eu.dhl.com/track/shipments"
        self.api_key = os.getenv('DHL_API_KEY')
    
    def get_api_headers(self) -> dict:
        return {'DHL-API-Key': self.api_key}
    
    def get_tracking_URL(self, tracking_number: str) -> str:
        return self.url + "?trackingNumber=" + tracking_number
    
    
    def get_tracking_info(self, tracking_number: str) -> TraceyEvent:
        connection = http.client.HTTPSConnection()
        connection.request("GET", self.get_tracking_URL(tracking_number), "", self.get_api_headers())
        response = connection.getresponse()
        data = json.loads(response.read())
        connection.close()
        return data
