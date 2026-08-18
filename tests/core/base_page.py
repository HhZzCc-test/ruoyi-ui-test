"""BasePage - 所有页面对象的基类

统一封装 Selenium 常用操作与显式等待，页面类只需声明元素定位器与业务动作，
测试逻辑与页面细节完全分离（Page Object Model）。
"""
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    """页面对象基类：提供查找/点击/输入/等待等公共能力"""

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout

    # ---------- 定位与等待 ----------

    def find(self, by, locator, timeout=None):
        """等待元素出现并返回（出现即返回，不要求可见）"""
        return WebDriverWait(self.driver, timeout or self.timeout).until(
            EC.presence_of_element_located((by, locator)),
            message=f"元素定位超时: {by}={locator}",
        )

    def find_clickable(self, by, locator, timeout=None):
        """等待元素可见且可点击"""
        return WebDriverWait(self.driver, timeout or self.timeout).until(
            EC.element_to_be_clickable((by, locator)),
            message=f"元素不可点击: {by}={locator}",
        )

    def is_visible(self, by, locator, timeout=5):
        """判断元素是否在指定时间内可见"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((by, locator))
            )
            return True
        except Exception:
            return False

    # ---------- 常用操作 ----------

    def click(self, by, locator, timeout=None):
        self.find_clickable(by, locator, timeout).click()

    def input(self, by, locator, text, timeout=None):
        el = self.find(by, locator, timeout)
        el.clear()
        el.send_keys(text)

    def get_text(self, by, locator, timeout=None):
        return self.find(by, locator, timeout).text

    def get_url(self):
        return self.driver.current_url

    # ---------- 页面跳转等待 ----------

    def wait_for_url(self, keyword, timeout=None):
        """等待当前 URL 包含指定关键字"""
        WebDriverWait(self.driver, timeout or self.timeout).until(
            EC.url_contains(keyword),
            message=f"等待 URL 包含 [{keyword}] 超时，当前: {self.driver.current_url}",
        )

    def wait_for_text(self, by, locator, text, timeout=None):
        """等待元素文本包含指定内容"""
        WebDriverWait(self.driver, timeout or self.timeout).until(
            EC.text_to_be_present_in_element((by, locator), text),
            message=f"等待元素文本包含 [{text}] 超时: {by}={locator}",
        )
