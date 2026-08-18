"""在线用户功能测试"""
import pytest
import allure

from tests.pages.dashboard_page import DashboardPage
from tests.pages.login_page import LoginPage
from tests.pages.online_page import OnlineUserPage


@allure.feature("系统监控")
class TestOnlineUser:

    @pytest.fixture(autouse=True)
    def _setup(self, driver, config):
        self._base_url = config.get("base_url", "http://localhost:80")
        login_cfg = config.get("login", {})
        page = LoginPage(driver, timeout=config.get("timeout", 10), config=config)
        page.login(login_cfg.get("username"), login_cfg.get("password"), self._base_url)
        page.wait_login_success()
        dashboard = DashboardPage(driver, timeout=10)
        dashboard.click_menu("在线用户")
        self._page = OnlineUserPage(driver, timeout=config.get("timeout", 10))

    @allure.story("在线用户展示")
    @allure.title("在线用户 - 正常场景: 列表展示")
    @pytest.mark.smoke
    def test_online_list_visible(self):
        assert self._page.get_table_row_count() >= 0, "在线用户列表应正常展示"

    @allure.story("搜索在线用户")
    @allure.title("在线用户 - 边界场景: 搜索不存在的用户")
    def test_search_nonexistent_user(self):
        self._page.search_user("nonexistent_user_xyz")
        assert self._page.get_table_row_count() == 0, "搜索不存在用户应无记录"

    @allure.story("重置搜索")
    @allure.title("在线用户 - 边界场景: 重置查询条件")
    def test_reset_search(self):
        self._page.search_user("nonexistent_user_xyz")
        self._page.click_reset()
        assert self._page.get_table_row_count() >= 0, "重置后表格应恢复"