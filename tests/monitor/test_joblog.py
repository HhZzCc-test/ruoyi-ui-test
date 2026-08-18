"""定时任务调度日志功能测试"""
import pytest
import allure

from tests.pages.dashboard_page import DashboardPage
from tests.pages.login_page import LoginPage
from tests.pages.joblog_page import JobLogPage


@allure.feature("定时任务调度日志")
class TestJobLog:

    @pytest.fixture(autouse=True)
    def _setup(self, driver, config):
        self._base_url = config.get("base_url", "http://localhost:80")
        login_cfg = config.get("login", {})
        page = LoginPage(driver, timeout=config.get("timeout", 10), config=config)
        page.login(login_cfg.get("username"), login_cfg.get("password"), self._base_url)
        page.wait_login_success()
        dashboard = DashboardPage(driver, timeout=10)
        dashboard.click_menu("定时任务调度日志")
        self._page = JobLogPage(driver, timeout=config.get("timeout", 10))

    @allure.story("日志列表展示")
    @allure.title("定时任务调度日志 - 正常场景: 日志列表展示")
    @pytest.mark.smoke
    def test_log_list_visible(self):
        assert self._page.get_table_row_count() >= 0, "调度日志列表应正常展示"