from datetime import datetime
from werkzeug.exceptions import NotFound
from flask import Flask, render_template, request, redirect, flash, url_for

from repositories.clubs_repo import ClubRepo
from repositories.competitions_repo import CompetitionRepo


app = Flask(__name__)
app.secret_key = 'something_special'

clubs = ClubRepo.load_clubs(ClubRepo.load_json())
competitions = CompetitionRepo.load_competitions(CompetitionRepo.load_json())

NOW = datetime.now()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/show_summary', methods=['POST'])
def show_summary():
    for club in clubs:
        if club.email == request.form['email']:
            return render_template('welcome.html', club=club, competitions=competitions)
        flash('This email is not registered')
        return render_template('index.html')


@app.route('/book/<competition>/<club>')
def book(competition, club):
    found_club = None
    found_competition = None

    for clb in clubs:
        if clb.name == club:
            found_club = clb

    for cpt in competitions:
        if cpt.name == competition:
            found_competition = cpt

    if found_club and found_competition:
        if found_competition.date > NOW:
            flash('You can now book places for this competition')
            return render_template('booking.html', club=found_club, competition=found_competition)
        flash('This competition is no longer available')
        return render_template('welcome.html', club=found_club, competitions=competitions)
    return NotFound()


@app.route('/purchase_places', methods=['POST'])
def purchase_places():
    club = None
    competition = None

    for clb in clubs:
        if clb.name == request.form['club']:
            club = clb

    for cpt in competitions:
        if cpt.name == request.form['competition']:
            competition = cpt

    places_required = int(request.form['places'])

    if places_required > club.points:
        flash('You do not have enough points to book that amount')
    elif places_required > 12:
        flash('You cannot book more than 12 places')
    elif places_required > competition.places:
        flash('Not enough places available')
    else:
        competition.places = competition.places - places_required
        club.points = club.points - places_required
        flash('Great-booking complete!')
        return render_template('welcome.html', club=club, competitions=competitions)
    return render_template('booking.html', club=club, competition=competition)


@app.route('/points_recap')
def points_recap():
    return render_template('points.html', clubs=clubs)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
