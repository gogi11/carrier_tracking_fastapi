from abc import ABC, abstractmethod
import json
from DTO.TraceyEventDTO import TraceyEventDTO


def get_tracey_mapping() -> dict[str, dict[str, TraceyEventDTO]]:
    with open("./filtered_events.json", "r") as json_file:
        return json.load(json_file)


class AbstractCarrier(ABC):
    def __init__(self, carrier_name: str) -> None:
        self.carrier_name = carrier_name

    @abstractmethod
    def get_api_response(self, tracking_number: str) -> object:
        pass

    @abstractmethod
    def get_tracking_statuses(self, api_response) -> list[str]:
        pass

    def get_tracking_info(self, tracking_number: str) -> list[TraceyEventDTO]:
        api_response = self.get_api_response(tracking_number)
        statuses = self.get_tracking_statuses(api_response)

        mappings = get_tracey_mapping()[self.carrier_name]
        tracey_dtos = []
        for status in statuses:
            if status in mappings:
                tracey_dtos.append(mappings[status])
            else:
                tracey_dtos.append(
                    TraceyEventDTO(
                        carrierException=status,
                        exceptionType="warning",
                        isReturned=False,
                        phase="none",
                        subPhase="none",
                        traceyEvent="none"
                    ))
        return tracey_dtos
