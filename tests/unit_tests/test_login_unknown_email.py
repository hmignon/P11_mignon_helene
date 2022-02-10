import server
from server import app


class TestLoginUnknownEmail:

    client = app.test_client()

    def test_valid_email(self):
        result = self.client.post("/showSummary", data={"email": server.clubs[0]["email"]})
        assert result.status_code == 200

    def test_invalid_email(self):
        result = self.client.post("/showSummary", data={"email": "jhbdfkshdvf"})
        assert result.status_code == 401
