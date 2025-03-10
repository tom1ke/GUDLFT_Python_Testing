import pytest
from datetime import datetime

import server
from server import app
from models.clubs import Club
from models.competitions import Competition


class TestServer:

    @pytest.fixture
    def client(self):
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client

    @pytest.fixture
    def example_club_instances(self):
        return [
            Club('Test club 1', 'test1@email.com', 40),
            Club('Test club 2', 'test2@email.com', 10),
            Club('Test club 3', 'test3@email.com', 5)
        ]

    @pytest.fixture
    def example_competition_instances(self):
        return [
            Competition('Test competition 1', datetime(2022, 11, 27, 13, 37), 15),
            Competition('Test competition 2', datetime(2022, 12, 25, 15, 15, 15), 25),
            Competition('Test competition 3', datetime(2023, 1, 15, 10), 10),
            Competition('Test competition 4', datetime(2020, 1, 12, 10), 16)
        ]


class TestIndex(TestServer):

    def test_should_return_index_page(self, client):
        rv = client.get('/')

        assert rv.status_code == 200


class TestShowSummary(TestServer):

    def test_should_return_show_summary_page_if_registered_email(self, client, monkeypatch, example_club_instances):
        monkeypatch.setattr(server, 'clubs', example_club_instances)

        rv = client.post('/show_summary', data=dict(email='test1@email.com'))

        assert rv.status_code == 200
        assert b'<h2>Welcome, test1@email.com </h2>' in rv.data

    def test_should_return_index_page_if_not_registered_email(self, client):
        rv = client.post('/show_summary', data=dict(email='wrong@email.com'))

        assert rv.status_code == 200
        assert b'<li>This email is not registered</li>' in rv.data


class TestBook(TestServer):

    def test_should_return_book_page_if_club_and_competition_are_valid(self, client, monkeypatch,
                                                                       example_club_instances,
                                                                       example_competition_instances):
        monkeypatch.setattr(server, 'clubs', example_club_instances)
        monkeypatch.setattr(server, 'competitions', example_competition_instances)

        rv = client.get('/book/Test competition 1/Test club 1')

        assert rv.status_code == 200
        assert b'<li>You can now book places for this competition</li>' in rv.data
        assert b'<h2>Test competition 1</h2>' in rv.data
        assert b'<input type="hidden" name="club" value="Test club 1">' in rv.data

    def test_should_return_404_if_club_or_competition_is_invalid(self, client, monkeypatch,
                                                                 example_club_instances,
                                                                 example_competition_instances):
        monkeypatch.setattr(server, 'clubs', example_club_instances)
        monkeypatch.setattr(server, 'competitions', example_competition_instances)

        rv = client.get('/book/Wrong competition/Wrong club')

        assert rv.status_code == 404

    def test_should_return_book_page_if_competition_date_is_passed(self, client, monkeypatch,
                                                                   example_club_instances,
                                                                   example_competition_instances):
        monkeypatch.setattr(server, 'clubs', example_club_instances)
        monkeypatch.setattr(server, 'competitions', example_competition_instances)

        rv = client.get('book/Test competition 4/Test club 1')

        assert rv.status_code == 200
        assert b'<li>This competition is no longer available</li>' \
               in rv.data


class TestPurchasePlaces(TestServer):

    def test_should_return_show_summary_page_if_booking_conditions_are_valid(self, client, monkeypatch,
                                                                             example_club_instances,
                                                                             example_competition_instances):
        monkeypatch.setattr(server, 'clubs', example_club_instances)
        monkeypatch.setattr(server, 'competitions', example_competition_instances)

        rv = client.post('/purchase_places', data=dict(club='Test club 1',
                                                       competition='Test competition 1',
                                                       places='10'))

        assert rv.status_code == 200
        assert b'<li>Great-booking complete!</li>' in rv.data

    def test_should_return_show_summary_with_points_updated(self, client, monkeypatch,
                                                            example_club_instances,
                                                            example_competition_instances):
        monkeypatch.setattr(server, 'clubs', example_club_instances)
        monkeypatch.setattr(server, 'competitions', example_competition_instances)

        rv = client.post('/purchase_places', data=dict(club='Test club 1',
                                                       competition='Test competition 1',
                                                       places='10'))

        assert rv.status_code == 200
        assert b'<p>Points available: 10</p>' in rv.data

    def test_should_return_purchase_places_page_if_not_enough_club_points(self, client, monkeypatch,
                                                                          example_club_instances,
                                                                          example_competition_instances):
        monkeypatch.setattr(server, 'clubs', example_club_instances)
        monkeypatch.setattr(server, 'competitions', example_competition_instances)

        rv = client.post('/purchase_places', data=dict(club='Test club 3',
                                                       competition='Test competition 1',
                                                       places='10'))

        assert rv.status_code == 200
        assert b'<li>You do not have enough points to book that amount</li>' in rv.data

    def test_should_return_purchase_places_page_if_book_more_than_12_places(self, client, monkeypatch,
                                                                            example_club_instances,
                                                                            example_competition_instances):
        monkeypatch.setattr(server, 'clubs', example_club_instances)
        monkeypatch.setattr(server, 'competitions', example_competition_instances)

        rv = client.post('/purchase_places', data=dict(club='Test club 1',
                                                       competition='Test competition 1',
                                                       places='13'))

        assert rv.status_code == 200
        assert b'<li>You cannot book more than 12 places</li>' in rv.data

    def test_should_return_purchase_places_page_if_not_enough_places_available(self, client, monkeypatch,
                                                                               example_club_instances,
                                                                               example_competition_instances):
        monkeypatch.setattr(server, 'clubs', example_club_instances)
        monkeypatch.setattr(server, 'competitions', example_competition_instances)

        rv = client.post('/purchase_places', data=dict(club='Test club 1',
                                                       competition='Test competition 3',
                                                       places='12'))

        assert rv.status_code == 200
        assert b'<li>Not enough places available</li>' in rv.data


class TestPointsRecap(TestServer):

    def test_should_return_points_recap_page_with_all_clubs_name_and_points(self, client, monkeypatch,
                                                                            example_club_instances):
        monkeypatch.setattr(server, 'clubs', example_club_instances)

        rv = client.get('/points_recap')

        assert rv.status_code == 200
        assert b'<li id="Test club 1">Test club 1 : 40</li>' in rv.data
        assert b'<li id="Test club 2">Test club 2 : 10</li>' in rv.data
        assert b'<li id="Test club 3">Test club 3 : 5</li>' in rv.data


class TestLogout(TestServer):

    def test_should_redirect_to_index_page(self, client):
        rv = client.get('/logout')

        assert rv.status_code == 302
