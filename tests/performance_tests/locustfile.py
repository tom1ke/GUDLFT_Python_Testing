from locust import HttpUser, task


class PerfTest(HttpUser):

    @task
    def home(self):
        self.client.get('http://127.0.0.1:5000/')

    @task
    def points_recap(self):
        self.client.get('http://127.0.0.1:5000/points_recap')

    @task
    def login(self):
        self.client.post('http://127.0.0.1:5000/show_summary', {'email': 'john@simplylift.co'})

    @task
    def booking(self):
        self.client.get('http://127.0.0.1:5000/book/Test%20competition%201/Simply%20Lift')

    @task
    def purchase(self):
        self.client.post('http://127.0.0.1:5000/purchase_places', {'club': 'Simply Lift',
                                                                   'competition': 'Test competition 1',
                                                                   'places': '1'})

    @task
    def logout(self):
        self.client.get('http://127.0.0.1:5000/logout')
