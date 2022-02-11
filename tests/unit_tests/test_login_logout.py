from server import app


class TestLoginLogout:
    client = app.test_client()

    def test_login(self):
        result = self.client.get("/")
        assert result.status_code == 200

    def test_logout(self):
        result = self.client.get("/logout")
        assert result.status_code == 302
