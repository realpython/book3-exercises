from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver


class LoginTests(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        cls.browser = webdriver.Firefox()
        super(LoginTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(LoginTests, cls).tearDownClass()

    def test_login(self):
        self.browser.get('%s%s' % (self.live_server_url, '/sign_in'))
