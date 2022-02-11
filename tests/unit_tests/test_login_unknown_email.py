import server
from server import app


class TestLoginUnknownEmail:

    client = app.test_client()

    def test_valid_email(self):
        result = self.client.post("/showSummary", data={"email": server.clubs[0]["email"]})

        assert result.status_code == 200
        assert f"{server.clubs[0]['email']}" in result.data.decode()

    def test_invalid_email(self):
        result = self.client.post("/showSummary", data={"email": "jhbdfkshdvf"})

        assert result.status_code == 401
        assert "No account related to this email." in result.data.decode()

    def test_empty_email(self):
        result = self.client.post("/showSummary", data={"email": ""})

        assert result.status_code == 401
        assert "Please enter your email." in result.data.decode()
