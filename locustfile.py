from locust import HttpUser, task, between

from server import load_clubs


class LocustTestServer(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        self.client.get("/")
        self.client.post("/showSummary", data={'email': load_clubs()[0]["email"]})

    @task
    def task1(self):
        pass
