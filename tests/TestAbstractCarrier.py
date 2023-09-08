import pytest
import responses
from fastapi import HTTPException
from carriers.AbstractCarrier import AbstractCarrier, get_tracey_mapping
from tests.ResponseTestMixin import ResponseTestMixin


class TestAbstractCarrier(ResponseTestMixin):
    invalid_carrier_name = "invalid_carrier_name"
    valid_carrier_name = "dhl"
    invalid_status = "invalid_status"
    valid_status = "Delivered"

    def mock_carrier(self, carrier_name, status_code=200, status_name="Delivered"):
        AbstractCarrier.__abstractmethods__ = set()
        carrier = AbstractCarrier(carrier_name)
        carrier.get_api_response = lambda tracking_number: self.mock_response("www.exampleapi.com", status_code=status_code)
        carrier.get_tracking_status = lambda request: status_name
        return carrier

    def test_is_correctly_initialized(self):
        carrier = self.mock_carrier(self.invalid_carrier_name)

        assert carrier.carrier_name == self.invalid_carrier_name

    def test_map_status_with_invalid_carrier_raises_404_error(self):
        carrier = self.mock_carrier(self.invalid_carrier_name)
        with (pytest.raises(HTTPException)) as err:
            carrier.map_status(self.valid_status)

        assert err.value.status_code == 404
        assert err.value.detail["message"] == f"Courier '{self.invalid_carrier_name}' is not supported."

    def test_map_status_with_invalid_status_raises_501_error(self):
        carrier = self.mock_carrier(self.valid_carrier_name)
        with (pytest.raises(HTTPException)) as err:
            carrier.map_status(self.invalid_status)

        assert err.value.status_code == 501
        assert err.value.detail["external_api_status"] == self.invalid_status
        assert err.value.detail["message"] == f"Unfortunately, we do not support this status type from {self.valid_carrier_name}"

    def test_valid_map_status_returns_tracey_event_dto_for_all_events(self):
        valid_mappings = get_tracey_mapping()
        # delete non-dhl for now
        del valid_mappings["bpost"]

        for carrier_name in valid_mappings.keys():
            carrier = self.mock_carrier(self.valid_carrier_name)
            for status_name in valid_mappings[carrier_name].keys():
                status = carrier.map_status(status_name)
                assert status == valid_mappings[carrier_name][status_name]

    def test_get_tracking_info_with_invalid_barcode_raises_404_error(self):
        carrier = self.mock_carrier(self.valid_carrier_name, status_code=404, status_name=self.valid_status)

        with (pytest.raises(HTTPException)) as err:
            carrier.get_tracking_info(self.invalid_status)

        assert err.value.status_code == 404
        assert err.value.detail["message"] == "Barcode not found. Please check the barcode and try again later."

    def test_valid_get_tracking_info_calls_map_status_with_correct_status(self):
        statuses=[]
        carrier = self.mock_carrier(self.valid_carrier_name, status_code=200, status_name=self.valid_status)
        carrier.map_status = lambda s: statuses.append(s)

        carrier.get_tracking_info(self.invalid_status)

        assert len(statuses) == 1
        assert statuses[0] == self.valid_status



