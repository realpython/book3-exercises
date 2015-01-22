from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.test.utils import override_settings

@override_settings(STATIC_ROOT='static/')
class LoginTests(LiveServerTestCase):
    
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
        user_textbox = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID,'id_emails'))) 

