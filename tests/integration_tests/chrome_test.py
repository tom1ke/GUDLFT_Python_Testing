import multiprocessing
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from flask_testing import LiveServerTestCase

from server import app


class TestChrome(LiveServerTestCase):

    def create_app(self):
        multiprocessing.set_start_method('fork', True)
        app.config['DEBUG'] = True
        app.config['TESTING'] = True
        return app

    def setUp(self):
        service = Service('tests/integration_tests/chromedriver')
        self.driver = webdriver.Chrome(service=service)

    def tearDown(self):
        self.driver.quit()

    def test_chrome(self):

        # get index page
        self.driver.get('http://127.0.0.1:5000')

        sleep(2)

        assert self.driver.find_element(By.TAG_NAME, 'h1').text == 'Welcome to the GUDLFT Registration Portal!'

        # get points recap page
        self.driver.find_element(By.LINK_TEXT, 'View points').click()

        sleep(2)

        assert self.driver.current_url == 'http://127.0.0.1:5000/points_recap'
        assert self.driver.find_element(By.TAG_NAME, 'li').text == 'Simply Lift : 13'

        # back to index page
        self.driver.find_element(By.LINK_TEXT, 'Back').click()

        # login with wrong email
        self.driver.find_element(By.TAG_NAME, 'input').send_keys('wrong@email.com')
        self.driver.find_element(By.TAG_NAME, 'button').submit()

        sleep(2)

        assert self.driver.find_element(By.TAG_NAME, 'li').text == 'This email is not registered'

        # login with registered email
        self.driver.find_element(By.TAG_NAME, 'input').send_keys('john@simplylift.co')
        self.driver.find_element(By.TAG_NAME, 'button').submit()

        sleep(2)

        assert self.driver.current_url == 'http://127.0.0.1:5000/show_summary'
        assert self.driver.find_element(By.TAG_NAME, 'h2').text == 'Welcome, john@simplylift.co'

        # get booking of passed competition
        self.driver.find_element(By.ID, 'Spring Festival').click()

        sleep(2)

        assert self.driver.find_element(By.TAG_NAME, 'li').text == 'This competition is no longer available'

        # get booking of invalid competition
        self.driver.get('http://127.0.0.1:5000/book/Wrong competition/Wrong club')

        sleep(2)

        assert self.driver.find_element(By.TAG_NAME, 'h1').text == 'Not Found'

        # get booking of valid competition
        self.driver.back()
        self.driver.find_element(By.ID, 'Test competition 1').click()

        sleep(2)

        assert self.driver.current_url == 'http://127.0.0.1:5000/book/Test%20competition%201/Simply%20Lift'
        assert self.driver.find_element(By.TAG_NAME, 'h2').text == 'Test competition 1'

        # book more than 12 places
        self.driver.find_element(By.NAME, 'places').send_keys('13')
        self.driver.find_element(By.TAG_NAME, 'button').submit()

        sleep(2)

        assert self.driver.find_element(By.TAG_NAME, 'li').text == 'You cannot book more than 12 places'

        # book more places than available
        self.driver.find_element(By.NAME, 'places').send_keys('12')
        self.driver.find_element(By.TAG_NAME, 'button').submit()

        sleep(2)

        assert self.driver.find_element(By.TAG_NAME, 'li').text == 'Not enough places available'

        # book valid amount of places
        self.driver.find_element(By.NAME, 'places').send_keys('5')
        self.driver.find_element(By.TAG_NAME, 'button').submit()

        sleep(2)

        assert self.driver.current_url == 'http://127.0.0.1:5000/purchase_places'
        assert self.driver.find_element(By.TAG_NAME, 'li').text == 'Great-booking complete!'
        assert self.driver.find_element(By.TAG_NAME, 'p').text == 'Points available: 8'

        # book more places than club points available
        self.driver.find_element(By.ID, 'Test competition 2').click()
        self.driver.find_element(By.NAME, 'places').send_keys('9')
        self.driver.find_element(By.TAG_NAME, 'button').submit()

        sleep(2)

        assert self.driver.find_element(By.TAG_NAME, 'li').text == 'You do not have enough points to book that amount'

        self.driver.back()
        self.driver.back()

        # logout
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()

        sleep(2)

        assert self.driver.current_url == 'http://127.0.0.1:5000/'

        self.driver.quit()
