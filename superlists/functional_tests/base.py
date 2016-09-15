import sys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver


class FunctionalTest(StaticLiveServerTestCase):

    @classmethod
    def isRunningOnStagingServer(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                return True
        else:
            return False

    @classmethod
    def getStagingServerURL(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                server_url = 'http://' + arg.split('=')[1]
                return server_url
        else:
            return None

    @classmethod
    def setUpClass(cls):
        if cls.isRunningOnStagingServer():
            cls.server_url = cls.getStagingServerURL()
        else:
            super(StaticLiveServerTestCase, cls).setUpClass()
            cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super(StaticLiveServerTestCase, cls).tearDownClass()

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text,
                      [row.text for row in rows],
                      "New to-do item did not appear in table -- its text was:\n {}".format(
                          table.text))

    def get_item_input_box(self):
        return self.browser.find_element_by_id('id_text')
