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
            Club('Test club 1', 'test1@email.com', 30),
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