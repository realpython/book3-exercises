from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from payments.models import User


class LoginTests(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        cls.browser = webdriver.Firefox()
        super(LoginTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(LoginTests, cls).tearDownClass()

    def setUp(self):
        self.valid_test_user = User.create(
            "tester", "test@valid.com", "test", 1234)

    def tearDown(self):
        self.valid_test_user.delete()

    def test_failed_login_invalid_email(self):
        self.browser.get('%s%s' % (self.live_server_url, '/sign_in'))
        email_textbox = self.browser.find_element_by_id("id_email")
        pwd_textbox = self.browser.find_element_by_id("id_password")
        email_textbox.send_keys("test@")
        pwd_textbox.send_keys("password")

        # click signin
        self.browser.find_element_by_name("commit").submit()

        # find the error element
        invalid_login = self.browser.find_element_by_css_selector(".errors")
        self.assertEquals(invalid_login.text,
                          "Email: Enter a valid email address.")

    def test_login(self):
        self.browser.get('%s%s' % (self.live_server_url, '/sign_in'))
        email_textbox = self.browser.find_element_by_id("id_email")
        pwd_textbox = self.browser.find_element_by_id("id_password")
        email_textbox.send_keys("test@valid.com")
        pwd_textbox.send_keys("test")

        # click sign in
        self.browser.find_element_by_name("commit").submit()

        # ensure the user box is shown, as this means we have logged in
        self.assertTrue(
            self.browser.find_element_by_id("user_info").is_displayed())
