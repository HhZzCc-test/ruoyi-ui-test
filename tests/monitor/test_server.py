"""服务监控功能测试"""
import pytest
import allure

from tests.pages.dashboard_page import DashboardPage
from tests.pages.login_page import LoginPage
from tests.pages.monitor_page import MonitorPage


@allure.feature("系统监控")
class TestServer:

    @pytest.fixture(autouse=True)
    def _setup(self, driver, config):
        self._base_url = config.get("base_url", "http://localhost:80")
        login_cfg = config.get("login", {})
        page = LoginPage(driver, timeout=config.get("timeout", 10), config=config)
        page.login(login_cfg.get("username"), login_cfg.get("password"), self._base_url)
        page.wait_login_success()
        dashboard = DashboardPage(driver, timeout=10)
        dashboard.click_menu("服务监控")
        self._page = MonitorPage(driver, path="/monitor/server", timeout=config.get("timeout", 10))

    @allure.story("服务监控展示")
    @allure.title("服务监控 - 正常场景: 页面加载")
    @pytest.mark.smoke
    def test_server_page_load(self):
        assert self._page.page_loaded(), "服务监控页面应正常加载"