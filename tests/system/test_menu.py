"""菜单管理功能测试"""
import pytest
import allure

from tests.pages.dashboard_page import DashboardPage
from tests.pages.login_page import LoginPage
from tests.pages.menu_page import MenuPage


@allure.feature("菜单管理")
class TestMenuManagement:

    @pytest.fixture(autouse=True)
    def _setup(self, driver, config):
        self._base_url = config.get("base_url", "http://localhost:80")
        login_cfg = config.get("login", {})
        page = LoginPage(driver, timeout=config.get("timeout", 10), config=config)
        page.login(login_cfg.get("username"), login_cfg.get("password"), self._base_url)
        page.wait_login_success()
        dashboard = DashboardPage(driver, timeout=10)
        dashboard.click_menu("菜单管理")
        self._page = MenuPage(driver, timeout=config.get("timeout", 10))

    @allure.story("新增菜单")
    @allure.title("菜单管理 - 正常场景: 新增菜单")
    @pytest.mark.smoke
    def test_add_menu(self):
        self._page.click_add()
        assert "添加" in self._page.get_dialog_title(), "点击新增应弹出添加弹窗"
        self._page.close_dialog()
        assert self._page.get_table_row_count() > 0, "菜单列表应展示数据"

    @allure.story("搜索菜单")
    @allure.title("菜单管理 - 边界场景: 搜索不存在的菜单")
    def test_search_nonexistent_menu(self):
        self._page.search_menu_name("nonexistent_menu_xyz")
        assert self._page.get_table_row_count() == 0, "搜索不存在菜单应无记录"

    @allure.story("重置搜索")
    @allure.title("菜单管理 - 边界场景: 重置查询条件")
    def test_reset_search(self):
        self._page.search_menu_name("nonexistent_menu_xyz")
        self._page.click_reset()
        assert self._page.get_table_row_count() > 0, "重置后应恢复全量列表"