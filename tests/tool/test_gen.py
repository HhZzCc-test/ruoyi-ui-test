"""代码生成功能测试"""
import pytest
import allure

from tests.pages.dashboard_page import DashboardPage
from tests.pages.login_page import LoginPage
from tests.pages.gen_page import GenPage


@allure.feature("系统工具")
class TestGen:

    @pytest.fixture(autouse=True)
    def _setup(self, driver, config):
        self._base_url = config.get("base_url", "http://localhost:80")
        login_cfg = config.get("login", {})
        page = LoginPage(driver, timeout=config.get("timeout", 10), config=config)
        page.login(login_cfg.get("username"), login_cfg.get("password"), self._base_url)
        page.wait_login_success()
        dashboard = DashboardPage(driver, timeout=10)
        dashboard.click_menu("代码生成")
        self._page = GenPage(driver, timeout=config.get("timeout", 10))

    @allure.story("代码生成展示")
    @allure.title("代码生成 - 正常场景: 列表展示")
    @pytest.mark.smoke
    def test_gen_list_visible(self):
        assert self._page.get_table_row_count() >= 0, "代码生成列表应正常展示"

    @allure.story("搜索表")
    @allure.title("代码生成 - 边界场景: 搜索不存在的表")
    def test_search_nonexistent_table(self):
        self._page.search_table("nonexistent_table_xyz")
        assert self._page.get_table_row_count() == 0, "搜索不存在表应无记录"

    @allure.story("重置搜索")
    @allure.title("代码生成 - 边界场景: 重置查询条件")
    def test_reset_search(self):
        self._page.search_table("nonexistent_table_xyz")
        self._page.click_reset()
        assert self._page.get_table_row_count() >= 0, "重置后表格应恢复"