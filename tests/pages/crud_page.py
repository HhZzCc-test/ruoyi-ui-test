"""若依 CRUD 模块通用基类 — 封装搜索、新增、弹窗、表格等通用操作"""
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from tests.core.base_page import BasePage


class CrudPage(BasePage):
    """若依后台 CRUD 页面通用基类

    子类只需定义：
      - URL 路径 (path)
      - 搜索输入框 placeholder (search_placeholder)
      - 新增按钮文本 (add_button_text)
      - 弹窗标题关键字 (dialog_title_keyword)
      - 表单字段 (form_fields: dict)
    """

    TABLE_ROWS = (By.CSS_SELECTOR, ".el-table__body-wrapper tbody tr")
    DIALOG_TITLE = (By.CSS_SELECTOR, ".el-dialog__wrapper:not([style*='display: none']) .el-dialog__title")
    MESSAGE = (By.CSS_SELECTOR, ".el-message__content")

    # 可在子类中覆盖
    path = ""
    search_placeholder = ""
    add_button_text = "新增"
    dialog_title_keyword = ""

    def goto(self, base_url):
        self.driver.get(f"{base_url}{self.path}")
        self.wait_for_url(self.path.replace("/", "").split("/")[-1] if self.path else "")
        self.find(By.CSS_SELECTOR, ".el-table__body-wrapper")

    # ---------- 搜索 ----------

    @property
    def _search_input(self):
        return (By.CSS_SELECTOR, f"input[placeholder='{self.search_placeholder}']")

    def search(self, keyword):
        el = self.find(*self._search_input)
        el.clear()
        el.send_keys(keyword)
        el.send_keys(Keys.RETURN)
        time.sleep(0.8)

    def click_reset(self):
        self.driver.execute_script(
            "arguments[0].click();",
            self.find(By.XPATH, "//button[contains(.,'重置')]"),
        )
        time.sleep(0.8)

    # ---------- 新增 ----------

    def click_add(self):
        self.driver.execute_script(
            "arguments[0].click();",
            self.find(By.XPATH, f"//button[contains(.,'{self.add_button_text}')]"),
        )
        time.sleep(0.5)

    def get_dialog_title(self):
        return self.get_text(*self.DIALOG_TITLE)

    def _form_input(self, label):
        return (By.XPATH,
            f"//div[contains(@class,'el-dialog__wrapper') and not(contains(@style,'display: none'))]"
            f"//label[contains(text(),'{label}')]/following-sibling::div//input"
        )

    def _form_select(self, label):
        return (By.XPATH,
            f"//div[contains(@class,'el-dialog__wrapper') and not(contains(@style,'display: none'))]"
            f"//label[contains(text(),'{label}')]/following-sibling::div//input"
        )

    def fill_form_field(self, label, value):
        self.input(*self._form_input(label), value)

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

    # ---------- 表格 ----------

    def get_table_row_count(self):
        return len(self.driver.find_elements(*self.TABLE_ROWS))

    def get_table_cell(self, row_index, col_index):
        cells = self.driver.find_elements(
            By.CSS_SELECTOR,
            f".el-table__body-wrapper tbody tr:nth-child({row_index + 1}) td",
        )
        if col_index < len(cells):
            return cells[col_index].text.strip()
        return ""

    def get_table_first_row_text(self):
        rows = self.driver.find_elements(*self.TABLE_ROWS)
        if rows:
            return rows[0].text.strip()
        return ""

    # ---------- 消息 ----------

    def get_message(self):
        if self.is_visible(*self.MESSAGE):
            return self.get_text(*self.MESSAGE)
        return ""

    # ---------- 删除 ----------

    def click_row_delete(self, row_index=0):
        self.driver.execute_script(
            "arguments[0].click();",
            self.find(By.XPATH,
                f"//div[contains(@class,'el-table__body-wrapper')]"
                f"//tr[{row_index + 1}]//span[contains(text(),'删除')]"
            ),
        )

    def confirm_delete(self):
        self.driver.execute_script(
            "arguments[0].click();",
            self.find(By.XPATH,
                "//div[contains(@class,'el-message-box')]//span[contains(text(),'确定')]"
            ),
        )

    def cancel_delete(self):
        self.driver.execute_script(
            "arguments[0].click();",
            self.find(By.XPATH,
                "//div[contains(@class,'el-message-box')]//span[contains(text(),'取消')]"
            ),
        )