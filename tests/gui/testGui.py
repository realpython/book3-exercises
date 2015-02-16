from django.test import LiveServerTestCase
from selenium import webdriver
from django.test.utils import override_settings
from payments.models import User
from tests.gui.pages.page import SignInPage, RegisterPage
import unittest

@unittest.skip("not now")
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
        self.sign_in_page = SignInPage(self.browser, self.live_server_url)

    def tearDown(self):
        self.valid_test_user.delete()

    def test_login(self):
        self.sign_in_page.go_to()
        self.sign_in_page.do_login("test@valid.com", "test")
        self.assertTrue(self.browser.find_element_by_id("user_info").is_displayed())

    def test_falied_login(self):
        self.sign_in_page.go_to()
        self.sign_in_page.do_login("test@test.com", "password")
        self.assertEquals(self.sign_in_page.error_msg, 
                          "Incorrect email address or password")

    def test_failed_login_invalid_email(self):

        self.sign_in_page.go_to()
        self.sign_in_page.do_login("test@","password")
        self.assertEquals(self.sign_in_page.error_msg,
                          "Email: Enter a valid email address.")

@override_settings(STATIC_ROOT='static/')
class RegistrationTests(LiveServerTestCase):
    
    @classmethod
    def setUpClass(cls):
        from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
        profile = FirefoxProfile()
        #profile.set_preference('geo.prompt.testing', True)
        #profile.set_preference('geo.prompt.testing.allow', True)
        cls.browser = webdriver.Firefox(profile)

        cls.browser.implicitly_wait(10)
        super(RegistrationTests, cls).setUpClass()
        
    @classmethod
    def tearDownClass(cls):
        #cls.browser.quit()
        super(RegistrationTests, cls).tearDownClass()

    def setUp(self):
        self.reg = RegisterPage(self.browser, self.live_server_url)

    def test_registration(self):
        self.reg.go_to()
        #self.reg.driver.execute_script('''window.navigator.geolocation.getCurrentPosition = 
        #        function(success){
        #            var position = {"coords" : {
        #                               "latitude": "1", 
        #                               "longitude": "2"
        #                             }
        #                 }; 
        #        success(position);}''');
        self.reg.name_textbox.send_keys("somebodynew")
        self.reg.email_textbox.send_keys("test@newtest1.com")
        self.reg.pwd_textbox.send_keys("test")
        self.reg.ver_pwd_textbox.send_keys("test")
        self.reg.cc_textbox.send_keys("4242424242424242")
        self.reg.cvc_textbox.send_keys("123")
        self.reg.expiry_month_dd.find_element_by_css_selector("option[value='4']").click()
        self.reg.expiry_year_dd.find_element_by_css_selector("option[value='2017']").click()
        self.reg.driver.execute_script('''angular.element(arguments[0])
                .scope().geoloc = {'coords' : {'latitude':
                                       '1','longitude':'2'}};
                angular.element(document.body).injector().get('$rootScope').$apply();''',
                                       self.reg.email_textbox)
        self.reg.register_button.click()


