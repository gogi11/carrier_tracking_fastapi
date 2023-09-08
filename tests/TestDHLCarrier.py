import json
import pytest
from carriers.DHLCarrier import DHLCarrier
from tests.ResponseTestMixin import ResponseTestMixin


class TestDHLCarrier(ResponseTestMixin):
    carrier = DHLCarrier()
    tracking_nr = "JVGL06252498000966068673"

    @staticmethod
    def get_valid_external_api_json():
        with(open("tests/valid_responses/example_dhl_response.json", "r")) as file:
            return json.load(file)

    def test_is_correctly_initialized(self):
        assert self.carrier.carrier_name == "dhl"
        assert self.carrier.url == "https://api-eu.dhl.com/track/shipments"
        assert self.carrier.api_key != ""

    def test_valid_get_api_response_works_correctly(self):
        response = self.carrier.get_api_response(self.tracking_nr)
        assert response.status_code == 200
        assert response.json()["shipments"] == self.get_valid_external_api_json()["shipments"]

    def test_invalid_get_api_response_returns_404_status_code(self):
        response = self.carrier.get_api_response("wrongbarcode")
        assert response.status_code == 404

    def test_valid_get_tracking_status_returns_string(self):
        valid_response = self.mock_response(self.carrier.url, json_data=self.get_valid_external_api_json())
        status = self.carrier.get_tracking_status(valid_response)
        assert status == self.get_valid_external_api_json()['shipments'][0]["status"]["status"]

    def test_invalid_get_tracking_status_raises_key_error(self):
        invalid_response = self.mock_response(self.carrier.url, json_data={"invalid": "json"})
        with (pytest.raises(KeyError)):
            self.carrier.get_tracking_status(invalid_response)

