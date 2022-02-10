import json
from datetime import datetime


def load_clubs():
    with open('clubs.json') as c:
        list_of_clubs = json.load(c)['clubs']
        return list_of_clubs


def load_competitions():
    with open('competitions.json') as comps:
        list_of_competitions = json.load(comps)['competitions']
        return list_of_competitions


def sort_competitions_date(comps):
    past = []
    present = []

    for comp in comps:
        comp_date = datetime.strptime(comp['date'], '%Y-%m-%d %H:%M:%S')
        if comp_date < datetime.now():
            past.append(comp)
        elif comp_date >= datetime.now():
            present.append(comp)

    return past, present


def initialize_booked_places(comps, clubs_list):
    places = []
    for comp in comps:
        for club in clubs_list:
            places.append({'competition': comp['name'], 'booked': [0, club['name']]})

    return places


def update_booked_places(competition, club, places_booked, places_required):
    for item in places_booked:
        if item['competition'] == competition['name']:
            if item['booked'][1] == club['name'] and item['booked'][0] + places_required <= 12:
                item['booked'][0] += places_required
                break
            else:
                raise ValueError("You can't book more than 12 places in a competition.")

    return places_booked
