import server
from server import app


class TestMorePointsThanAllowed:
    client = app.test_client()
    competition = [
        {
            "name": "Test",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "25"
        }
    ]

    club = [
        {
            "name": "Test club",
            "email": "test_club@email.com",
            "points": "10"
        }
    ]

    def setup_method(self):
        server.competitions = self.competition
        server.clubs = self.club

    def test_points_within_allowed(self):
        result = self.client.post(
            "/purchasePlaces",
            data={
                "places": 3,
                "club": self.club[0]["name"],
                "competition": self.competition[0]["name"]
            }
        )

        assert result.status_code == 200
        assert "Great-booking complete!" in result.data.decode()
        assert int(self.club[0]["points"]) >= 0

    def test_more_points_than_allowed(self):
        result = self.client.post(
            "/purchasePlaces",
            data={
                "places": 5,
                "club": self.club[0]["name"],
                "competition": self.competition[0]["name"]
            }
        )

        assert result.status_code == 400
        assert "have enough points." in result.data.decode()
        assert int(self.club[0]["points"]) >= 0
