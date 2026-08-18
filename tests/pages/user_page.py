"""系统管理-用户管理页 Page Object"""
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from tests.core.base_page import BasePage


class UserPage(BasePage):
    """若依用户管理页（/system/user）

    注：不同版本若依前端部分元素 id/class 可能不同，若定位失败，
    依据当前版本微调下方选择器即可，页面动作封装不变。
    """

    TABLE_ROWS = (By.CSS_SELECTOR, ".el-table__body-wrapper tbody tr")

    # 搜索区
    SEARCH_USERNAME = (By.CSS_SELECTOR, "input[placeholder='请输入用户名称']")

    # 操作按钮
    BTN_ADD = (By.XPATH, "//button[contains(.,'新增')]")
    BTN_SEARCH = (By.XPATH, "//button[contains(.,'搜索')]")
    BTN_RESET = (By.XPATH, "//button[contains(.,'重置')]")

    # 新增/编辑弹窗（可见弹窗的标题）
    DIALOG_TITLE = (By.CSS_SELECTOR, ".el-dialog__wrapper:not([style*='display: none']) .el-dialog__title")

    # 顶部提示消息
    MESSAGE = (By.CSS_SELECTOR, ".el-message__content")

    def goto(self, base_url):
        self.driver.get(f"{base_url}/system/user")
        self.wait_for_url("system/user")
        self.find(By.CSS_SELECTOR, ".el-table__body-wrapper")

    # ---------- 表单输入：通过 el-form-item 的 label 定位输入框（限定在可见弹窗内） ----------

    def _form_input(self, label):
        return (By.XPATH, f"//div[contains(@class,'el-dialog__wrapper') and not(contains(@style,'display: none'))]//label[contains(text(),'{label}')]/following-sibling::div//input")

    def fill_nickname(self, nickname):
        self.input(*self._form_input("用户昵称"), nickname)

    def fill_username(self, username):
        self.input(*self._form_input("用户名称"), username)

    def fill_phone(self, phone):
        self.input(*self._form_input("手机号码"), phone)

    def fill_password(self, password):
        self.input(*self._form_input("用户密码"), password)

    # ---------- 弹窗操作 ----------

    def click_add(self):
        self.click(*self.BTN_ADD)

    def get_dialog_title(self):
        return self.get_text(*self.DIALOG_TITLE)

    def submit_dialog(self):
        """点击弹窗底部【确定】按钮（button 文本为"确 定"含空格）"""
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

    # ---------- 查询 ----------

    def search_username(self, username):
        """搜索用户名：清空输入框→输入→按 Enter 触发搜索→等待表格刷新"""
        el = self.find(*self.SEARCH_USERNAME)
        el.clear()
        el.send_keys(username)
        el.send_keys(Keys.RETURN)
        time.sleep(0.8)

    def click_reset(self):
        """点击重置按钮"""
        self.driver.execute_script("arguments[0].click();", self.find(*self.BTN_RESET))
        time.sleep(0.8)

    def get_table_row_count(self):
        return len(self.driver.find_elements(*self.TABLE_ROWS))

    # ---------- 删除 ----------

    def click_row_delete(self, row_index=0):
        self.click(
            By.XPATH,
            f"//div[contains(@class,'el-table__body-wrapper')]//tr[{row_index + 1}]//span[contains(text(),'删除')]",
        )

    def confirm_delete(self):
        """确认删除（el-message-box 确定按钮）"""
        self.click(By.XPATH, "//div[contains(@class,'el-message-box')]//span[contains(text(),'确定')]")

    def get_message(self):
        """获取操作提示消息（el-message），等待最多 5s"""
        if self.is_visible(*self.MESSAGE):
            return self.get_text(*self.MESSAGE)
        return ""