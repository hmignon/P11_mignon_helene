from datetime import datetime

import server

from utils import (
    load_clubs,
    load_competitions,
    sort_competitions_date,
    initialize_booked_places,
    update_booked_places
)


class TestUtils:

    def test_load_clubs(self):
        result = load_clubs()
        assert type(result) is list

    def test_load_competitions(self):
        result = load_competitions()
        assert type(result) is list

    def test_sort_competitions(self):
        competitions = load_competitions()
        past, present = sort_competitions_date(competitions)

        assert type(past) is list
        assert type(present) is list
        assert len(past) + len(present) == len(competitions)
        assert datetime.strptime(past[0]['date'], '%Y-%m-%d %H:%M:%S') < datetime.now()
        assert datetime.strptime(present[0]['date'], '%Y-%m-%d %H:%M:%S') >= datetime.now()

    def test_initialize_booked_places(self):
        booked_places = initialize_booked_places(server.competitions, server.clubs)

        assert type(booked_places) is list
        assert len(booked_places) == len(server.competitions) * len(server.clubs)
        assert booked_places[0]['booked'] == [0, server.clubs[0]['name']]

    def test_update_booked_places(self):
        places_required = 2
        places_booked = initialize_booked_places(server.competitions, server.clubs)
        booked_places = update_booked_places(
            server.competitions[0],
            server.clubs[0],
            places_booked,
            places_required
        )

        assert type(booked_places) is list
        assert len(booked_places) == 1
        assert booked_places[0]['booked'] == [places_required, server.clubs[0]['name']]
