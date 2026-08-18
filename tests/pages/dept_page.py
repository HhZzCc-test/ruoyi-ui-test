"""系统管理-部门管理页 Page Object（树形表格）"""
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from tests.core.base_page import BasePage


class DeptPage(BasePage):
    path = "/system/dept"

    SEARCH_NAME = (By.CSS_SELECTOR, "input[placeholder='请输入部门名称']")
    SEARCH_STATUS = (By.CSS_SELECTOR, "input[placeholder='部门状态']")
    BTN_SEARCH = (By.XPATH, "//button[contains(.,'搜索')]")
    BTN_RESET = (By.XPATH, "//button[contains(.,'重置')]")
    BTN_ADD = (By.XPATH, "//button[contains(.,'新增')]")
    TABLE_ROWS = (By.CSS_SELECTOR, ".el-table__body-wrapper tbody tr")
    DIALOG_TITLE = (By.CSS_SELECTOR, ".el-dialog__wrapper:not([style*='display: none']) .el-dialog__title")
    MESSAGE = (By.CSS_SELECTOR, ".el-message__content")

    def goto(self, base_url):
        self.driver.get(f"{base_url}{self.path}")
        self.wait_for_url("dept")
        self.find(By.CSS_SELECTOR, ".el-table__body-wrapper")
        time.sleep(0.5)

    def get_table_row_count(self):
        return len(self.driver.find_elements(*self.TABLE_ROWS))

    def search_dept(self, name):
        el = self.find(*self.SEARCH_NAME)
        el.clear()
        el.send_keys(name)
        self.driver.execute_script("arguments[0].click();", self.find(*self.BTN_SEARCH))
        time.sleep(0.8)

    def click_reset(self):
        self.driver.execute_script("arguments[0].click();", self.find(*self.BTN_RESET))
        time.sleep(0.8)

    def click_add(self):
        self.driver.execute_script("arguments[0].click();", self.find(*self.BTN_ADD))
        time.sleep(0.5)

    def get_dialog_title(self):
        return self.get_text(*self.DIALOG_TITLE)

    def _form_input(self, label):
        return (By.XPATH,
            f"//div[contains(@class,'el-dialog__wrapper') and not(contains(@style,'display: none'))]"
            f"//label[contains(text(),'{label}')]/following-sibling::div//input"
        )

    def fill_dept_name(self, value):
        self.input(*self._form_input("部门名称"), value)

    def fill_order_num(self, value):
        self.input(*self._form_input("显示排序"), value)

    def submit_dialog(self):
        self.driver.execute_script(
            "arguments[0].click();",
            self.find(By.XPATH,
                "//div[contains(@class,'el-dialog__wrapper') and not(contains(@style,'display: none'))]"
                "//button[contains(.,'确')]"
            ),
        )

    def close_dialog(self):
        self.driver.execute_script(
            "arguments[0].click();",
            self.find(By.CSS_SELECTOR, ".el-dialog__headerbtn"),
        )

    def get_message(self):
        if self.is_visible(*self.MESSAGE):
            return self.get_text(*self.MESSAGE)
        return ""