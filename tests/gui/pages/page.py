from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SeleniumPage(object):
    '''Place to allow for any site wide configuration you may want 
    for you GUI testing.
    ''' 

    def __init__(self, driver, base_url=None, wait_time=10):
        self.driver = driver
        self.base_url= base_url
        self.wait_time= wait_time

class SeleniumElement(object):

    def __init__(self, locator):
        self.locator = locator


    def __get__(self,obj, owner):
        driver = obj.driver
        wait_time = obj.wait_time
        return WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located(self.locator))
            

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

    @property
    def rel_url(self):
        return '/register'
        
    def go_to(self):
        self.driver.get('%s%s' % (self.base_url, self.rel_url))
        assert self.register_title.text == "Register Today!"
       


