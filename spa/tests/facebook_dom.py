import dom_helper

FBEMAIL = '#email'
FBPASS = '#pass'
FBLOGIN = 'input[name="login"]'
FBGRANT = 'input[name="grant_clicked"]'


class FacebookDom(dom_helper.DomHelper):
    def is_window_open(self):
        return len(self.driver.window_handles) > 1

    def select_window(self):
        self.driver.switch_to_window(self.driver.window_handles[-1])

    def reset_window(self):
        self.driver.switch_to_window(self.driver.window_handles[0])

    def login(self):
        self.enter_text_field(FBEMAIL, 'nancy_jymsykb_greenberg@tfbnw.net')
        self.enter_text_field(FBPASS, 'LoELw09qtAWwA')
        self.click_button(FBLOGIN)

    def do_login_flow(self):
        self.select_window()
        if self.is_window_open():
            self.login()
        self.reset_window()

    def do_authorize_flow(self):
        self.select_window()
        if self.is_window_open():
            self.login()
        if self.is_window_open() and self.is_el_present(FBGRANT):
            self.click_button(FBGRANT)
        self.reset_window()