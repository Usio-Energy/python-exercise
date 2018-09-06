import json

# Helper utils for tests


class MockResponse:
    """A generic mocked web response."""
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


def get_realistic_data():
    """Return realistic rates data as dict."""
    with open("./tests/artefacts/realistic_response.json", "r") as f:
        return json.load(f)


def get_specific_date_data(desired_date):
    """Returns realistic dataset with specified datetime.
        desired_date is a datetime object
    """
    realistic_data = get_realistic_data()
    realistic_data["timestamp"] = desired_date.timestamp()
    realistic_data["date"] = desired_date.strftime("%Y-%m-%d")
    return realistic_data


def mock_api_response(code=200, when=None):
    api_data = get_specific_date_data(when) if when else get_realistic_data()
    return MockResponse(json_data=api_data, status_code=code)
