import os
import requests
from carriers.AbstractCarrier import AbstractCarrier


class DHLCarrier(AbstractCarrier):
    def __init__(self):
        super().__init__("dhl")
        self.url = "https://api-eu.dhl.com/track/shipments"
        self.api_key = os.getenv('DHL_API_KEY')

    def get_api_response(self, tracking_number):
        headers = {'DHL-API-Key': self.api_key}
        return requests.get(self.url, headers=headers, params={"trackingNumber": tracking_number})
    
    def get_tracking_status(self, api_response):
        status = api_response.json()['shipments'][0]["status"]["status"]
        return status
