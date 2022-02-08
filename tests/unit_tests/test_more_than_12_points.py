import server
from server import app


class TestMoreThanTwelvePoints:

    client = app.test_client()
    competition = [
        {
            "name": "Test",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "40"
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

    def test_less_than_twelve(self):
        booked = 5

        self.client.post(
            "/purchasePlaces",
            data={
                "places": booked,
                "club": self.club[0]["name"],
                "competition": self.competition[0]["name"]
            }
        )

        assert booked <= 12

    def test_more_than_twelve_once(self):
        booked = 15

        self.client.post(
            "/purchasePlaces",
            data={
                "places": booked,
                "club": self.club[0]["name"],
                "competition": self.competition[0]["name"]
            }
        )

        assert booked <= 12

    def test_more_than_twelve_added(self):
        places_bought = []
        booked = 6

        i = 0
        while i <= 2:
            self.client.post(
                "/purchasePlaces",
                data={
                    "places": booked,
                    "club": self.club[0]["name"],
                    "competition": self.competition[0]["name"]
                }
            )
            places_bought.append(booked)
            i += 1

            assert sum(places_bought) <= 12
