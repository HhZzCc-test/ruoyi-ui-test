"""用户管理功能测试 - 增/查/边界（对应 doc/testcases/TC-USER-用户管理.md）"""
import time
import pytest
import allure

from tests.pages.login_page import LoginPage
from tests.pages.user_page import UserPage


@allure.feature("系统管理-用户管理")
class TestUserManagement:
    """前置：登录并进入用户管理页"""

    @pytest.fixture(autouse=True)
    def _setup(self, driver, config):
        self._base_url = config.get("base_url", "http://localhost:80")
        login_cfg = config.get("login", {})
        page = LoginPage(driver, timeout=config.get("timeout", 10), config=config)
        page.login(login_cfg.get("username"), login_cfg.get("password"), self._base_url)
        page.wait_login_success()
        self._page = UserPage(driver, timeout=config.get("timeout", 10))
        self._page.goto(self._base_url)

    def _unique_name(self, prefix="aitest"):
        """生成唯一用户名，避免重复执行数据冲突"""
        return f"{prefix}_{int(time.time())}"

    @allure.story("新增用户")
    @allure.title("用户管理 - 正常场景: 新增用户成功并可查询到")
    @pytest.mark.smoke
    def test_add_user(self):
        """TC-USER-001: 新增用户"""
        self._page.click_add()
        assert "添加" in self._page.get_dialog_title(), f"点击新增应弹出新增弹窗, 实际: {self._page.get_dialog_title()}"
        name = self._unique_name()
        self._page.fill_nickname(name)
        self._page.fill_username(name)
        self._page.fill_password("Test@123")
        self._page.submit_dialog()
        msg = self._page.get_message()
        assert "成功" in msg, f"新增应提示成功，实际提示: {msg}"
        # 回查：新增的用户应能查询到
        self._page.search_username(name)
        assert self._page.get_table_row_count() >= 1, "新增后应能查询到该用户"

    @allure.story("查询用户")
    @allure.title("用户管理 - 正常场景: 搜索存在的用户返回记录")
    def test_search_existing_user(self):
        """TC-USER-002: 搜索存在的用户"""
        self._page.search_username("admin")
        assert self._page.get_table_row_count() >= 1, "搜索 admin 应返回记录"

    @allure.story("查询用户")
    @allure.title("用户管理 - 边界场景: 搜索不存在的用户无记录")
    def test_search_nonexistent_user(self):
        """TC-USER-003: 搜索不存在的用户"""
        self._page.search_username("nonexistent_user_zzz")
        assert self._page.get_table_row_count() == 0, "搜索不存在的用户应无记录"

    @allure.story("重置查询")
    @allure.title("用户管理 - 正常场景: 重置后恢复全量列表")
    def test_reset_search(self):
        """TC-USER-004: 重置查询条件"""
        self._page.search_username("nonexistent_user_zzz")
        assert self._page.get_table_row_count() == 0, "搜索不存在用户应无记录"
        self._page.click_reset()
        assert self._page.get_table_row_count() > 0, "重置后应恢复全量列表"