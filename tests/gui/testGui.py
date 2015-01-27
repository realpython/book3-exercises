from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.test.utils import override_settings
from payments.models import User

@override_settings(STATIC_ROOT='static/')
class LoginTests(LiveServerTestCase):
    
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
        self.valid_test_user = User.create("tester", "test@valid.com", "test",
                                          1234)
    def tearDown(self):
        self.valid_test_user.delete()


    def test_login(self):
        self.browser.get('%s%s' % (self.live_server_url, '/sign_in'))
        email_textbox = self.browser.find_element_by_id("id_email")
        pwd_textbox = self.browser.find_element_by_id("id_password")
        email_textbox.send_keys("test@valid.com")
        pwd_textbox.send_keys("test")

        #click signin
        self.browser.find_element_by_name("commit").submit()

        #find the error element
        self.assertTrue(self.browser.find_element_by_id("user_info").is_displayed())

    def test_falied_login(self):
        self.browser.get('%s%s' % (self.live_server_url, '/sign_in'))
        email_textbox = self.browser.find_element_by_id("id_email")
        pwd_textbox = self.browser.find_element_by_id("id_password")
        email_textbox.send_keys("test@test.com")
        pwd_textbox.send_keys("password")

        #click signin
        self.browser.find_element_by_name("commit").submit()

        #find the error element
        invalid_login = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".errors")))

        self.assertEquals(invalid_login.text, 
                          "Incorrect email address or password")

    def test_failed_login_invalid_email(self):
        self.browser.get('%s%s' % (self.live_server_url, '/sign_in'))
        email_textbox = self.browser.find_element_by_id("id_email")
        pwd_textbox = self.browser.find_element_by_id("id_password")
        email_textbox.send_keys("test@")
        pwd_textbox.send_keys("password")

        #click signin
        self.browser.find_element_by_name("commit").submit()

        #find the error element
        invalid_login = self.browser.find_element_by_css_selector(".errors")
        self.assertEquals(invalid_login.text, 
                          "Email: Enter a valid email address.")
