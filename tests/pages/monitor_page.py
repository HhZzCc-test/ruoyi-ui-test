"""系统监控-数据监控/服务监控/缓存监控/缓存列表 页 Page Object"""
import time
from selenium.webdriver.common.by import By

from tests.core.base_page import BasePage


class MonitorPage(BasePage):
    """监控类页面（数据监控、服务监控、缓存监控、缓存列表）"""

    TABLE_ROWS = (By.CSS_SELECTOR, ".el-table__body-wrapper tbody tr")
    MESSAGE = (By.CSS_SELECTOR, ".el-message__content")

    def __init__(self, driver, path, timeout=10):
        super().__init__(driver, timeout=timeout)
        self.path = path

    def goto(self, base_url):
        self.driver.get(f"{base_url}{self.path}")
        time.sleep(2)

    def page_loaded(self):
        return len(self.driver.find_elements(By.CSS_SELECTOR, ".el-card, .el-table, .el-tabs")) > 0

    def get_table_row_count(self):
        return len(self.driver.find_elements(*self.TABLE_ROWS))

    def get_message(self):
        if self.is_visible(*self.MESSAGE):
            return self.get_text(*self.MESSAGE)
        return ""