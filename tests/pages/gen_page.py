"""系统工具-代码生成 页 Page Object"""
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from tests.core.base_page import BasePage


class GenPage(BasePage):
    path = "/tool/gen"

    SEARCH_TABLE = (By.CSS_SELECTOR, "input[placeholder='请输入表名称']")
    BTN_SEARCH = (By.XPATH, "//button[contains(.,'搜索')]")
    BTN_RESET = (By.XPATH, "//button[contains(.,'重置')]")
    BTN_IMPORT = (By.XPATH, "//button[contains(.,'导入')]")
    TABLE_ROWS = (By.CSS_SELECTOR, ".el-table__body-wrapper tbody tr")
    MESSAGE = (By.CSS_SELECTOR, ".el-message__content")

    def goto(self, base_url):
        self.driver.get(f"{base_url}{self.path}")
        self.wait_for_url("gen")
        self.find(By.CSS_SELECTOR, ".el-table__body-wrapper")

    def search_table(self, keyword):
        el = self.find(*self.SEARCH_TABLE)
        el.clear()
        el.send_keys(keyword)
        el.send_keys(Keys.RETURN)
        time.sleep(0.8)

    def click_reset(self):
        self.driver.execute_script("arguments[0].click();", self.find(*self.BTN_RESET))
        time.sleep(0.8)

    def get_table_row_count(self):
        return len(self.driver.find_elements(*self.TABLE_ROWS))

    def get_message(self):
        if self.is_visible(*self.MESSAGE):
            return self.get_text(*self.MESSAGE)
        return ""