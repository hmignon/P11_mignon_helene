from server import app


class TestLogin:

    client = app.test_client()

    def test_valid_email(self):
        result = self.client.post("/showSummary", data=dict(email="admin@irontemple.com"))
        assert result.status_code == 200

    def test_invalid_email(self):
        result = self.client.post("/showSummary", data=dict(email="jhbdfkshdvf"))
        assert result.status_code == 403
