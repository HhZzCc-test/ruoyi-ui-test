"""系统接口功能测试"""
import pytest
import allure

from tests.pages.dashboard_page import DashboardPage
from tests.pages.login_page import LoginPage
from tests.pages.tool_page import ToolPage


@allure.feature("系统工具")
class TestSwagger:

    @pytest.fixture(autouse=True)
    def _setup(self, driver, config):
        self._base_url = config.get("base_url", "http://localhost:80")
        login_cfg = config.get("login", {})
        page = LoginPage(driver, timeout=config.get("timeout", 10), config=config)
        page.login(login_cfg.get("username"), login_cfg.get("password"), self._base_url)
        page.wait_login_success()
        dashboard = DashboardPage(driver, timeout=10)
        dashboard.click_menu("系统接口")
        self._page = ToolPage(driver, path="/tool/swagger", timeout=config.get("timeout", 10))

    @allure.story("系统接口展示")
    @allure.title("系统接口 - 正常场景: 页面加载")
    @pytest.mark.smoke
    def test_swagger_page_load(self):
        assert self._page.page_loaded(), "系统接口页面应正常加载"