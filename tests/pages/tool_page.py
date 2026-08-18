"""系统工具-表单构建/系统接口 页 Page Object"""
import time
from selenium.webdriver.common.by import By

from tests.core.base_page import BasePage


class ToolPage(BasePage):
    """工具类页面（表单构建、系统接口）"""

    def __init__(self, driver, path, timeout=10):
        super().__init__(driver, timeout=timeout)
        self.path = path

    def goto(self, base_url):
        self.driver.get(f"{base_url}{self.path}")
        time.sleep(2)

    def page_loaded(self):
        return len(self.driver.find_elements(
            By.CSS_SELECTOR, ".el-card, .el-table, .el-form, iframe, .swagger"
        )) > 0