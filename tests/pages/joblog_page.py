"""系统监控-定时任务调度日志页 Page Object"""
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from tests.core.base_page import BasePage


class JobLogPage(BasePage):
    path = "/monitor/jobLog"

    SEARCH_INPUT = (By.CSS_SELECTOR, ".el-input__inner[placeholder]")
    BTN_SEARCH = (By.XPATH, "//button[contains(.,'搜索')]")
    BTN_RESET = (By.XPATH, "//button[contains(.,'重置')]")
    BTN_CLEAN = (By.XPATH, "//button[contains(.,'清空')]")
    BTN_EXPORT = (By.XPATH, "//button[contains(.,'导出')]")
    BTN_DETAIL = (By.XPATH, "//button[contains(.,'详细')]")
    TABLE_ROWS = (By.CSS_SELECTOR, ".el-table__body-wrapper tbody tr")
    DIALOG_TITLE = (By.CSS_SELECTOR, ".el-dialog__wrapper:not([style*='display: none']) .el-dialog__title")
    MESSAGE = (By.CSS_SELECTOR, ".el-message__content")

    def goto(self, base_url):
        self.driver.get(f"{base_url}{self.path}")
        time.sleep(1.5)
        self.find(By.CSS_SELECTOR, ".el-table__body-wrapper")

    def get_table_row_count(self):
        return len(self.driver.find_elements(*self.TABLE_ROWS))

    def search_job(self, name):
        inputs = self.driver.find_elements(*self.SEARCH_INPUT)
        for inp in inputs:
            try:
                if inp.is_displayed() and inp.is_enabled():
                    inp.clear()
                    inp.send_keys(name)
                    break
            except Exception:
                continue
        time.sleep(0.3)
        self.driver.execute_script("arguments[0].click();", self.find(*self.BTN_SEARCH))
        time.sleep(0.8)

    def click_reset(self):
        self.driver.execute_script("arguments[0].click();", self.find(*self.BTN_RESET))
        time.sleep(0.8)

    def click_clean(self):
        self.driver.execute_script("arguments[0].click();", self.find(*self.BTN_CLEAN))
        time.sleep(0.5)