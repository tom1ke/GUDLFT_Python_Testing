import json
from datetime import datetime

from models.competitions import Competition


class CompetitionRepo:

    @staticmethod
    def load_json():
        with open('repositories/competitions.json') as competitions:
            return json.load(competitions)['competitions']

    @classmethod
    def load_competitions(cls, competitions_data):
        list_of_competitions = []
        for c in competitions_data:
            name = c['name']
            date = datetime.strptime(c['date'], '%Y-%m-%d %H:%M:%S')
            places = int(c['numberOfPlaces'])
            competition = Competition(name, date, places)
            list_of_competitions.append(competition)
        return list_of_competitions
