import pytest
from datetime import datetime

from models.competitions import Competition
from repositories.competitions_repo import CompetitionRepo


class TestCompetition:

    @pytest.fixture
    def competition_data_fixture(self):
        return [
            {
                'name': 'Test competition 1',
                'date': '2022-11-27 13:37:00',
                'numberOfPlaces': '15'
            },
            {
                'name': 'Test competition 2',
                'date': '2022-12-25 15:15:15',
                'numberOfPlaces': '25'
            }
        ]

    def test_load_competitions(self, competition_data_fixture):
        test_competition_1 = Competition('Test competition 1', datetime(2022, 11, 27, 13, 37), 15)
        test_competition_2 = Competition('Test competition 2', datetime(2022, 12, 25, 15, 15, 15), 25)
        expected = [test_competition_1, test_competition_2]
        sut = CompetitionRepo.load_competitions(competition_data_fixture)
        assert sut == expected
