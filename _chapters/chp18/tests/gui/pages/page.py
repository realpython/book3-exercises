from selenium import webdriver

from payments.models import User
from tests.gui.pages.page import SignInPage
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class LoginTests(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        cls.browser = webdriver.Firefox()
        cls.browser.implicitly_wait(10)
        super(LoginTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(LoginTests, cls).tearDownClass()

    def setUp(self):
        self.valid_test_user = User.create(
            "tester", "test@valid.com", "test", 1234)
        self.sign_in_page = SignInPage(self.browser, self.live_server_url)

    def tearDown(self):
        self.valid_test_user.delete()

    def test_login(self):
        self.sign_in_page.go_to()
        self.sign_in_page.do_login("test@valid.com", "test")
        self.assertTrue(
            self.browser.find_element_by_id("user_info").is_displayed())

    def test_falied_login(self):
        self.sign_in_page.go_to()
        self.sign_in_page.do_login("test@test.com", "password")
        self.assertEquals(self.sign_in_page.error_msg,
                          "Incorrect email address or password")

    def test_failed_login_invalid_email(self):
        self.sign_in_page.go_to()
        self.sign_in_page.do_login("test@", "password")
        self.assertEquals(self.sign_in_page.error_msg,
                          "Email: Enter a valid email address.")
