"""菜单导航功能测试（对应 doc/testcases/TC-NAV-导航.md）"""
import pytest
import allure

from tests.core.assertions import assert_url_contains
from tests.pages.dashboard_page import DashboardPage
from tests.pages.login_page import LoginPage


@allure.feature("菜单导航")
class TestNavigation:
    """前置：登录成功"""

    @pytest.fixture(autouse=True)
    def _setup(self, driver, config):
        self._base_url = config.get("base_url", "http://localhost:80")
        login_cfg = config.get("login", {})
        page = LoginPage(driver, timeout=config.get("timeout", 10), config=config)
        page.login(login_cfg.get("username"), login_cfg.get("password"), self._base_url)
        page.wait_login_success()
        self._dashboard = DashboardPage(driver, timeout=config.get("timeout", 10))

    @allure.story("菜单展示")
    @allure.title("导航 - 正常场景: 登录后侧边栏展示核心菜单")
    @pytest.mark.smoke
    def test_sidebar_menus_visible(self):
        """TC-NAV-001: 登录后侧边栏展示菜单"""
        menus = self._dashboard.get_menus()
        assert len(menus) >= 3, f"侧边栏应展示核心菜单，实际: {menus}"
        core = ["系统管理", "系统监控"]
        for keyword in core:
            assert any(keyword in m for m in menus), f"侧边栏应包含菜单 [{keyword}]"

    @allure.story("菜单跳转")
    @allure.title("导航 - 正常场景: 点击菜单跳转对应路由")
    def test_click_menu_route(self, driver):
        """TC-NAV-002: 点击【用户管理】跳转 /system/user"""
        self._dashboard.click_menu("用户管理")
        assert_url_contains(driver, "system/user", msg="点击用户管理应跳转到 /system/user")
