from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from payments.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django_ecommerce.guitest_settings import SERVER_ADDR


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


class RegistrationTests(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
        profile = FirefoxProfile()
        profile.set_preference('geo.prompt.testing', True)
        profile.set_preference('geo.prompt.testing.allow', True)
        cls.browser = webdriver.Firefox(profile)

        cls.browser.implicitly_wait(10)
        super(RegistrationTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(RegistrationTests, cls).tearDownClass()

    def setUp(self):
        self.reg = RegisterPage(self.browser, "http://" + SERVER_ADDR)

    def test_registration(self):
        self.reg.go_to()
        self.reg.do_reg(name="somebodynew", email="test@newtest.com",
                        pwd="test", pwd2="test", cc="4242424242424242",
                        cvc="123", expiry_month="4", expiry_year="2020")
        self.assertTrue(
            self.browser.find_element_by_id("user_info").is_displayed())

    def test_failed_registration(self):
        self.reg.go_to()
        self.reg.do_reg(name="somebodynew", email="test@newtest2.com",
                        pwd="test", pwd2="test2", cc="4242424242424242",
                        cvc="123", expiry_month="4", expiry_year="2020")
        self.assertIn("Passwords do not match", self.reg.error_msg)


class SeleniumPage(object):
    '''Place to allow for any site-wide configuration you may want
    for you GUI testing.
    '''

    def __init__(self, driver, base_url=None, wait_time=10):
        self.driver = driver
        self.base_url = base_url
        self.wait_time = wait_time


class SeleniumElement(object):

    def __init__(self, locator):
        self.locator = locator

    def __get__(self, obj, owner):
        driver = obj.driver
        wait_time = obj.wait_time
        return WebDriverWait(driver, wait_time).until(
            EC.visibility_of_element_located(self.locator))


class SignInPage(SeleniumPage):

    email_textbox = SeleniumElement((By.ID, "id_email"))
    pwd_textbox = SeleniumElement((By.ID, "id_password"))
    sign_in_button = SeleniumElement((By.NAME, "commit"))
    error_msg_elem = SeleniumElement((By.CSS_SELECTOR, ".errors"))
    sign_in_title = SeleniumElement((By.CSS_SELECTOR, ".form-signin-heading"))

    def do_login(self, email, pwd):
        self.email_textbox.send_keys(email)
        self.pwd_textbox.send_keys(pwd)
        self.sign_in_button.submit()

    @property
    def error_msg(self):
        return self.error_msg_elem.text

    @property
    def rel_url(self):
        return '/sign_in'

    def go_to(self):
        self.driver.get('%s%s' % (self.base_url, self.rel_url))
        assert self.sign_in_title.text == "Sign in"


class RegisterPage(SeleniumPage):

    name_textbox = SeleniumElement((By.ID, 'id_name'))
    email_textbox = SeleniumElement((By.ID, 'id_email'))
    pwd_textbox = SeleniumElement((By.ID, 'id_password'))
    ver_pwd_textbox = SeleniumElement((By.ID, 'id_ver_password'))
    cc_textbox = SeleniumElement((By.ID, 'credit_card_number'))
    cvc_textbox = SeleniumElement((By.ID, 'cvc'))
    expiry_month_dd = SeleniumElement((By.ID, 'expiry_month'))
    expiry_year_dd = SeleniumElement((By.ID, 'expiry_year'))
    register_title = SeleniumElement((By.CSS_SELECTOR, '.form-signin-heading'))
    register_button = SeleniumElement((By.ID, 'user_submit'))
    errors_div = SeleniumElement((By.CSS_SELECTOR, ".alert"))

    @property
    def error_msg(self):
        '''the errors div has a 'x' to close it
        let's not return that
        '''
        return self.errors_div.text[2:]

    @property
    def rel_url(self):
        return '/register'

    def go_to(self):
        self.driver.get('%s%s' % (self.base_url, self.rel_url))
        assert self.register_title.text == "Register Today!"

    def mock_geoloc(self, lat, lon):
        self.driver.execute_script('''angular.element($('#id_email'))
                .scope().geoloc = {
                    'coords': {'latitude': '%s','longitude':'%s'}};
                angular.element(document.body).injector().get('$rootScope').$apply();
                ''' % (lat, lon))

    def set_expiry_month(self, month_as_int):
        selector = "option[value='%s']" % (month_as_int)
        self.expiry_month_dd.find_element_by_css_selector(selector).click()

    def set_expiry_year(self, year_as_int):
        selector = "option[value='%s']" % (year_as_int)
        self.expiry_year_dd.find_element_by_css_selector(selector).click()

    def do_reg(self, name, email, pwd, pwd2, cc, cvc,
               expiry_month, expiry_year, lat=1, lon=2):

        self.name_textbox.send_keys(name)
        self.email_textbox.send_keys(email)
        self.pwd_textbox.send_keys(pwd)
        self.ver_pwd_textbox.send_keys(pwd2)
        self.cc_textbox.send_keys(cc)
        self.cvc_textbox.send_keys(cvc)
        self.set_expiry_month(expiry_month)
        self.set_expiry_year(expiry_year)
        self.mock_geoloc(lat, lon)
        self.register_button.click()
