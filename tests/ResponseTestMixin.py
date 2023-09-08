import responses


class ResponseTestMixin:
    def mock_response(self, url, method="GET", json_data={}, status_code=200):
        response = responses.Response(
            method="GET",
            url=url,
            json=json_data,
            status=status_code
        )
        response.json = lambda: json_data
        response.status_code = status_code
        return response