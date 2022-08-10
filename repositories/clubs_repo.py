import json

from models.clubs import Club


class ClubRepo:

    @staticmethod
    def load_json():
        with open('repositories/clubs.json') as clubs:
            return json.load(clubs)['clubs']

    @classmethod
    def load_clubs(cls, clubs_data):
        list_of_clubs = []
        for c in clubs_data:
            name = c['name']
            email = c['email']
            points = int(c['points'])
            club = Club(name, email, points)
            list_of_clubs.append(club)
        return list_of_clubs
