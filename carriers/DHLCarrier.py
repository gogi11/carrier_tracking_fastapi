import os
import requests
from carriers.AbstractCarrier import AbstractCarrier


class DHLCarrier(AbstractCarrier):
    def __init__(self) -> None:
        super().__init__("dhl")
        self.url = "https://api-eu.dhl.com/track/shipments"
        self.api_key = os.getenv('DHL_API_KEY')

    def get_api_response(self, tracking_number: str):
        headers = {'DHL-API-Key': self.api_key}
        final_url = self.url + "?trackingNumber=" + tracking_number

        return requests.get(final_url, headers=headers).json()
    
    def get_tracking_statuses(self, api_response):
        statuses = [event["status"] for event in api_response['shipments'][0]["events"]]
        return statuses
