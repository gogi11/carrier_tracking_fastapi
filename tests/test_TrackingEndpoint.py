import main
from fastapi.testclient import TestClient
from main import app, carriers
from tests.ResponseTestMixin import ResponseTestMixin

client = TestClient(app)


class TestTrackingEndpoint(ResponseTestMixin):
    def get_tracking_dto(self):
        return {"barcode": "JVGL06252498001022908447", "carrier": "dhl", "credentials": ""}

    def test_GET_PUT_DELETE_not_allowed(self):
        response = client.get("/tracking")
        assert response.status_code == 405

        response = client.put("/tracking")
        assert response.status_code == 405

        response = client.delete("/tracking")
        assert response.status_code == 405

    def test_incorrect_carrier_raises_error(self):
        wrong_carrier_dto = self.get_tracking_dto()
        wrong_carrier_dto["carrier"] = "wrongcarrier"

        response = client.post("/tracking", json=wrong_carrier_dto)

        assert response.status_code == 422
        assert response.json()["detail"][0]["msg"] == "Input should be {0}" \
            .format(" or ".join(["'" + c + "'" for c in carriers]))

    def test_incorrect_barcode_raises_error(self):
        wrong_barcode_dto = self.get_tracking_dto()
        wrong_barcode_dto["barcode"] = "wrongbarcode"

        response = client.post("/tracking", json=wrong_barcode_dto)

        assert response.status_code == 404
        assert response.json()["detail"][
                   "message"] == "Barcode not found. Please check the barcode and try again later."

    def test_status_outside_of_filtered_events_raises_error(self):
        dto = self.get_tracking_dto()
        dto["barcode"] = "JVGL06252498000966068673"

        response = client.post("/tracking", json=dto)

        assert response.status_code == 501
        assert response.json()["detail"]["message"] == \
               f"Unfortunately, we do not support this status type from {self.get_tracking_dto()['carrier']}"

    def test_too_many_external_api_calls_raises_error(self, mocker):
        mocker.patch("requests.get", return_value=self.mock_response("www.whatever.com", status_code=429))
        response = client.post("/tracking", json=self.get_tracking_dto())
        assert response.status_code == 429
        assert response.json()["detail"]["message"] == "The daily limit of the external api has been reached. Please try again tomorrow."

    def test_crash_in_external_api_calls_raises_error(self, mocker):
        mocker.patch(
            "requests.get",
            return_value=self.mock_response("www.whatever.com", status_code=500,
                                            json_data={"message": "api error", "other": "info"})
        )
        response = client.post("/tracking", json=self.get_tracking_dto())
        assert response.status_code == 500
        assert response.json()["detail"]["message"] == "api error"
        assert response.json()["detail"]["other"] == "info"

    def test_valid_call_returns_valid_tracey_event(self):
        dto = self.get_tracking_dto()

        response = client.post("/tracking", json=dto)

        assert response.status_code == 200
        assert response.json() == {
            "carrierException": None,
            "exceptionType": "success",
            "isReturned": False,
            "phase": "delivered",
            "subPhase": "receiver",
            "traceyEvent": "dhl1_0213"
        }
