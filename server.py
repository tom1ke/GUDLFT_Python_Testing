from datetime import datetime
from flask import Flask, render_template, request, redirect, flash, url_for

from repositories.clubs_repo import ClubRepo
from repositories.competitions_repo import CompetitionRepo


app = Flask(__name__)
app.secret_key = 'something_special'

clubs = ClubRepo.load_clubs(ClubRepo.load_json())
competitions = CompetitionRepo.load_competitions(CompetitionRepo.load_json())


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
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


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
        flash('Great-booking complete!')
        return render_template('welcome.html', club=club, competitions=competitions)
    return render_template('booking.html', club=club, competition=competition)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))