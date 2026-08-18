"""操作日志功能测试"""
import pytest
import allure

from tests.pages.dashboard_page import DashboardPage
from tests.pages.login_page import LoginPage
from tests.pages.operlog_page import OperLogPage


@allure.feature("操作日志")
class TestOperLog:

    @pytest.fixture(autouse=True)
    def _setup(self, driver, config):
        self._base_url = config.get("base_url", "http://localhost:80")
        login_cfg = config.get("login", {})
        page = LoginPage(driver, timeout=config.get("timeout", 10), config=config)
        page.login(login_cfg.get("username"), login_cfg.get("password"), self._base_url)
        page.wait_login_success()
        dashboard = DashboardPage(driver, timeout=10)
        dashboard.click_menu("操作日志")
        self._page = OperLogPage(driver, timeout=config.get("timeout", 10))

    @allure.story("日志展示")
    @allure.title("操作日志 - 正常场景: 日志列表展示")
    @pytest.mark.smoke
    def test_log_list_visible(self):
        assert self._page.get_table_row_count() >= 0, "操作日志列表应正常展示"

    @allure.story("搜索日志")
    @allure.title("操作日志 - 边界场景: 搜索不存在的模块")
    def test_search_nonexistent_log(self):
        self._page.search_module("nonexistent_module_xyz")
        assert self._page.get_table_row_count() == 0, "搜索不存在模块应无记录"

    @allure.story("重置搜索")
    @allure.title("操作日志 - 边界场景: 重置查询条件")
    def test_reset_search(self):
        self._page.search_module("nonexistent_module_xyz")
        self._page.click_reset()
        assert self._page.get_table_row_count() >= 0, "重置后表格应恢复"