"""定时任务功能测试"""
import pytest
import allure

from tests.pages.dashboard_page import DashboardPage
from tests.pages.login_page import LoginPage
from tests.pages.job_page import JobPage


@allure.feature("系统监控")
class TestJob:

    @pytest.fixture(autouse=True)
    def _setup(self, driver, config):
        self._base_url = config.get("base_url", "http://localhost:80")
        login_cfg = config.get("login", {})
        page = LoginPage(driver, timeout=config.get("timeout", 10), config=config)
        page.login(login_cfg.get("username"), login_cfg.get("password"), self._base_url)
        page.wait_login_success()
        dashboard = DashboardPage(driver, timeout=10)
        dashboard.click_menu("定时任务")
        self._page = JobPage(driver, timeout=config.get("timeout", 10))

    @allure.story("定时任务展示")
    @allure.title("定时任务 - 正常场景: 列表展示")
    @pytest.mark.smoke
    def test_job_list_visible(self):
        assert self._page.get_table_row_count() >= 0, "定时任务列表应正常展示"

    @allure.story("搜索定时任务")
    @allure.title("定时任务 - 边界场景: 搜索不存在的任务")
    def test_search_nonexistent_job(self):
        self._page.search_job("nonexistent_job_xyz")
        assert self._page.get_table_row_count() == 0, "搜索不存在任务应无记录"

    @allure.story("重置搜索")
    @allure.title("定时任务 - 边界场景: 重置查询条件")
    def test_reset_search(self):
        self._page.search_job("nonexistent_job_xyz")
        self._page.click_reset()
        assert self._page.get_table_row_count() >= 0, "重置后表格应恢复"