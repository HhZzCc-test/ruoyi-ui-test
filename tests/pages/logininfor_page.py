"""系统管理-登录日志页 Page Object（只读）"""
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from tests.core.base_page import BasePage


class LoginLogPage(BasePage):
    path = "/system/log/logininfor"

    SEARCH_USER = (By.CSS_SELECTOR, "input[placeholder='请输入用户名称']")
    BTN_SEARCH = (By.XPATH, "//button[contains(.,'搜索')]")
    BTN_RESET = (By.XPATH, "//button[contains(.,'重置')]")
    BTN_CLEAR = (By.XPATH, "//button[contains(.,'清空')]")
    TABLE_ROWS = (By.CSS_SELECTOR, ".el-table__body-wrapper tbody tr")
    MESSAGE = (By.CSS_SELECTOR, ".el-message__content")

    def goto(self, base_url):
        self.driver.get(f"{base_url}{self.path}")
        self.wait_for_url("logininfor")
        self.find(By.CSS_SELECTOR, ".el-table__body-wrapper")

    def search_user(self, keyword):
        el = self.find(*self.SEARCH_USER)
        el.clear()
        el.send_keys(keyword)
        time.sleep(0.3)
        self.driver.execute_script("arguments[0].click();", self.find(*self.BTN_SEARCH))
        time.sleep(0.8)

    def click_reset(self):
        self.driver.execute_script("arguments[0].click();", self.find(*self.BTN_RESET))
        time.sleep(0.8)

    def click_clear(self):
        self.driver.execute_script("arguments[0].click();", self.find(*self.BTN_CLEAR))
        time.sleep(0.5)

    def confirm_dialog(self):
        self.driver.execute_script(
            "arguments[0].click();",
            self.find(By.XPATH, "//div[contains(@class,'el-message-box')]//span[contains(text(),'确定')]"),
        )

    def get_table_row_count(self):
        return len(self.driver.find_elements(*self.TABLE_ROWS))

    def get_message(self):
        if self.is_visible(*self.MESSAGE):
            return self.get_text(*self.MESSAGE)
        return ""