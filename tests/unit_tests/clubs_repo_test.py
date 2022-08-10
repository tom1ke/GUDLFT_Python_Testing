import pytest

from models.clubs import Club
from repositories.clubs_repo import ClubRepo


class TestClub:

    @pytest.fixture
    def club_data_fixture(self):
        return [
            {
                'name': 'Test club 1',
                'email': 'test1@email.com',
                'points': '10'

            },
            {
                'name': 'Test club 2',
                'email': 'test2@email.com',
                'points': '5'
            }
        ]

    def test_load_clubs(self, club_data_fixture):
        test_club_1 = Club('Test club 1', 'test1@email.com', 10)
        test_club_2 = Club('Test club 2', 'test2@email.com', 5)
        expected = [test_club_1, test_club_2]
        sut = ClubRepo.load_clubs(club_data_fixture)
        assert sut == expected
