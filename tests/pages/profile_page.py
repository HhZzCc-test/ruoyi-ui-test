"""系统管理-个人中心页 Page Object"""
import time
from selenium.webdriver.common.by import By

from tests.core.base_page import BasePage


class ProfilePage(BasePage):
    path = "/system/user/profile"

    PAGE_TITLE = (By.CSS_SELECTOR, ".el-tabs__item.is-active")
    TAB_PWD = (By.XPATH, "//div[contains(@class,'el-tabs__item')][contains(text(),'修改密码')]")
    AVATAR = (By.CSS_SELECTOR, ".user-avatar-img img")
    BTN_SUBMIT = (By.XPATH, "//button[contains(.,'保 存')]")

    def goto(self, base_url):
        self.driver.get(f"{base_url}{self.path}")
        time.sleep(1.5)

    def get_page_title(self):
        try:
            return self.get_text(*self.PAGE_TITLE)
        except Exception:
            return ""

    def click_tab_pwd(self):
        self.driver.execute_script("arguments[0].click();", self.find(*self.TAB_PWD))
        time.sleep(0.3)