"""个人中心功能测试"""
import pytest
import allure

from tests.pages.dashboard_page import DashboardPage
from tests.pages.login_page import LoginPage
from tests.pages.profile_page import ProfilePage


@allure.feature("个人中心")
class TestProfile:

    @pytest.fixture(autouse=True)
    def _setup(self, driver, config):
        self._base_url = config.get("base_url", "http://localhost:80")
        login_cfg = config.get("login", {})
        page = LoginPage(driver, timeout=config.get("timeout", 10), config=config)
        page.login(login_cfg.get("username"), login_cfg.get("password"), self._base_url)
        page.wait_login_success()
        dashboard = DashboardPage(driver, timeout=10)
        dashboard.click_profile()
        self._page = ProfilePage(driver, timeout=config.get("timeout", 10))

    @allure.story("个人信息展示")
    @allure.title("个人中心 - 正常场景: 个人信息页加载")
    @pytest.mark.smoke
    def test_profile_page_load(self):
        title = self._page.get_page_title()
        assert title == "基本资料", "默认Tab应为基本资料"

    @allure.story("修改密码")
    @allure.title("个人中心 - 边界场景: 修改密码Tab切换")
    def test_switch_to_pwd_tab(self):
        self._page.click_tab_pwd()
        assert self._page.find(*self._page.TAB_PWD).is_displayed(), "修改密码Tab应可见"