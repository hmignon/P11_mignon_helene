import server
from server import app


class TestOverbookCompetition:

    client = app.test_client()
    competition = [
        {
            "name": "Test",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "5"
        }
    ]

    club = [
        {
            "name": "Test club",
            "email": "test_club@email.com",
            "points": "20"
        }
    ]

    def setup_method(self):
        server.competitions = self.competition
        server.clubs = self.club

    def test_overbook_competition(self):
        booked = 6

        result = self.client.post(
            "/purchasePlaces",
            data={
                "places": booked,
                "club": self.club[0]["name"],
                "competition": self.competition[0]["name"]
            }
        )

        assert result.status_code == 400
        assert "Not enough places available." in result.data.decode()
        assert int(self.competition[0]['numberOfPlaces']) >= 0
