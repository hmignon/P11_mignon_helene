from locust import HttpUser, task, between

from server import load_clubs, load_competitions


class LocustTestServer(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        self.client.get("/")
        self.client.post("/showSummary", data={'email': load_clubs()[0]["email"]})

    @task
    def book_places(self):
        self.client.post(
            "/purchasePlaces",
            data={
                "places": 0,
                "club": load_clubs()[0]["name"],
                "competition": load_competitions()[0]["name"]
            }
        )
