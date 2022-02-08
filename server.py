import json
from datetime import datetime

from flask import Flask, render_template, request, redirect, flash, url_for


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
        if datetime.strptime(comp['date'], '%Y-%m-%d %H:%M:%S') < datetime.now():
            past.append(comp)
        elif datetime.strptime(comp['date'], '%Y-%m-%d %H:%M:%S') >= datetime.now():
            present.append(comp)

    return past, present


def initialize_booked_places(comps, clubs_list):
    places = []
    for comp in comps:
        for club in clubs_list:
            places.append({'competition': comp['name'], 'booked': [0, club['name']]})

    return places


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = load_competitions()
clubs = load_clubs()
past_competitions, present_competitions = sort_competitions_date(competitions)
places_booked = initialize_booked_places(competitions, clubs)


def update_booked_places(competition, club, places_required):
    for item in places_booked:
        if item['competition'] == competition['name']:
            if item['booked'][1] == club['name'] and item['booked'][0] + places_required <= 12:
                item['booked'][0] += places_required
                break
            else:
                raise ValueError("You can't book more than 12 places in a competition.")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def show_summary():
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        return render_template(
            'welcome.html',
            club=club,
            past_competitions=past_competitions,
            present_competitions=present_competitions
        )
    except IndexError:
        if request.form['email'] == '':
            flash("Please enter your email.", 'error')
        else:
            flash("No account related to this email.", 'error')
        return render_template('index.html'), 403


@app.route('/book/<competition>/<club>')
def book(competition, club):
    found_club = [c for c in clubs if c['name'] == club][0]
    found_competition = [c for c in competitions if c['name'] == competition][0]
    if found_club and found_competition:
        if datetime.strptime(found_competition['date'], '%Y-%m-%d %H:%M:%S') < datetime.now():
            flash("This competition is over.", 'error')
            return render_template(
                'welcome.html',
                club=club,
                past_competitions=past_competitions,
                present_competitions=present_competitions
            ), 403
        return render_template('booking.html', club=found_club, competition=found_competition)

    else:
        flash("Something went wrong-please try again", 'error')
        return render_template(
            'welcome.html',
            club=club,
            past_competitions=past_competitions,
            present_competitions=present_competitions
        ), 403


@app.route('/purchasePlaces', methods=['POST'])
def purchase_places():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]

    try:
        places_required = int(request.form['places'])
    except ValueError:
        flash('Please enter a number between 0 and 12.', 'error')
        return render_template('booking.html', club=club, competition=competition), 403

    if places_required > int(competition['numberOfPlaces']):
        flash('Not enough places available.', 'error')
        return render_template('booking.html', club=club, competition=competition), 403

    elif places_required > int(club['points']):
        flash('You don\'t have enough points.', 'error')
        return render_template('booking.html', club=club, competition=competition), 403

    elif places_required > 12:
        flash('You can\'t book more than 12 places in a competition.', 'error')
        return render_template('booking.html', club=club, competition=competition), 403

    else:
        try:
            update_booked_places(competition, club, places_required)
            competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - places_required
            club['points'] = int(club['points']) - places_required
            flash('Great-booking complete!', 'success')
            return render_template(
                'welcome.html',
                club=club,
                past_competitions=past_competitions,
                present_competitions=present_competitions
            )

        except ValueError as error_message:
            flash(error_message, 'error')
            return render_template('booking.html', club=club, competition=competition), 403


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
