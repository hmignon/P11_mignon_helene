from locust import HttpUser, task, between

from server import load_clubs, load_competitions


class LocustTestServer(HttpUser):
    wait_time = between(1, 5)
    competition = load_competitions()[0]
    club = load_clubs()[0]

    def on_start(self):
        self.client.get("/")
        self.client.post("/showSummary", data={'email': self.club["email"]}, name="/showSummary")

    @task
    def get_booking(self):
        self.client.get(
            f"/book/{self.competition['name']}/{self.club['name']}",
            name="/book/..."
        )

    @task
    def post_booking(self):
        self.client.post(
            "/purchasePlaces",
            data={
                "places": 0,
                "club": self.club["name"],
                "competition": self.competition["name"]
            },
            name="/purchasePlaces"
        )
