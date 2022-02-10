from datetime import datetime

from flask import Flask, render_template, request, redirect, flash, url_for

import utils

app = Flask(__name__)
app.secret_key = 'something_special'

competitions = utils.load_competitions()
clubs = utils.load_clubs()
past_competitions, present_competitions = utils.sort_competitions_date(competitions)
places_booked = utils.initialize_booked_places(competitions, clubs)


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
        return render_template('index.html'), 401


@app.route('/book/<competition>/<club>')
def book(competition, club):
    found_club = [c for c in clubs if c['name'] == club][0]

    try:
        found_competition = [c for c in competitions if c['name'] == competition][0]

        if datetime.strptime(found_competition['date'], '%Y-%m-%d %H:%M:%S') < datetime.now():
            flash("This competition is over.", 'error')
            status_code = 400

        else:
            return render_template('booking.html', club=found_club, competition=found_competition)

    except IndexError:
        flash("Something went wrong-please try again", 'error')
        status_code = 404

    return render_template(
        'welcome.html',
        club=found_club,
        past_competitions=past_competitions,
        present_competitions=present_competitions
    ), status_code


@app.route('/purchasePlaces', methods=['POST'])
def purchase_places():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]

    try:
        places_required = int(request.form['places'])

        if places_required > int(competition['numberOfPlaces']):
            flash('Not enough places available.', 'error')

        elif places_required * 3 > int(club['points']):
            flash("You don't have enough points.", 'error')

        elif places_required > 12:
            flash("You can't book more than 12 places in a competition.", 'error')

        else:
            try:
                utils.update_booked_places(competition, club, places_booked, places_required)
                competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - places_required
                club['points'] = int(club['points']) - (places_required * 3)
                flash('Great-booking complete!', 'success')

                return render_template(
                    'welcome.html',
                    club=club,
                    past_competitions=past_competitions,
                    present_competitions=present_competitions
                )

            except ValueError as error_message:
                flash(error_message, 'error')

    except ValueError:
        flash('Please enter a number between 0 and 12.', 'error')

    return render_template('booking.html', club=club, competition=competition), 400


@app.route('/viewClubPoints')
def view_club_points():
    club_list = sorted(clubs, key=lambda club: club['name'])
    return render_template('club_points.html', clubs=club_list)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
