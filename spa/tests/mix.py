import uuid
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import LiveServerTestCase
from django.test.client import Client
import unittest
from django.test.utils import override_settings
from selenium.webdriver.support.wait import WebDriverWait
from dss import settings
from spa.tests import facebook_dom
from spa.tests.webdriver import CustomWebDriver
from utils import here

class TestUploadMix(LiveServerTestCase):
    TIMEOUT = 20

    def setUp(self):
        User.objects.create_superuser(username='admin',
                                      password='pw',
                                      email='fergal.moran@gmail.com')
        self.wd = CustomWebDriver()
        self.wd.implicitly_wait(100)
        self.wd.set_page_load_timeout(100)

        self.waiter = WebDriverWait(self.wd, self.TIMEOUT)

    def tearDown(self):
        self.wd.quit()


    @override_settings(DEBUG=True)
    def test_upload(self):
        self.login()
        self.open('/mix/upload')

        self.wd.find_css('.btn-next').click()
        self.
        print "Tests completed"


    def open(self, url):
        self.wd.get("%s%s" % (self.live_server_url, url))


    def login(self):
        self.open(reverse('admin:index'))
        self.wd.find_css('#id_username').send_keys("admin")
        self.wd.find_css("#id_password").send_keys('pw')
        self.wd.find_element_by_xpath('//input[@value="Log in"]').click()
        self.wd.find_css("#grp-content-container")