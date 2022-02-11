import server
from server import app


class TestBookPastCompetition:
    client = app.test_client()
    competitions = [
        {
            "name": "Test_closed",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "20"
        },
        {
            "name": "Test_open",
            "date": "2022-03-27 10:00:00",
            "numberOfPlaces": "20"
        }
    ]

    club = [
        {
            "name": "Test club",
            "email": "test_club@email.com",
            "points": "15"
        }
    ]

    def setup_method(self):
        server.competitions = self.competitions
        server.clubs = self.club

    def test_book_closed_competition(self):
        result = self.client.get(
            f"/book/{self.competitions[0]['name']}/{self.club[0]['name']}"
        )
        assert result.status_code == 400
        assert "This competition is over." in result.data.decode()

    def test_book_open_competition(self):
        result = self.client.get(
            f"/book/{self.competitions[1]['name']}/{self.club[0]['name']}"
        )
        assert result.status_code == 200

    def test_book_non_existant_competition(self):
        result = self.client.get(
            f"/book/random_name/{self.club[0]['name']}"
        )
        assert result.status_code == 404
        assert "Something went wrong-please try again" in result.data.decode()
