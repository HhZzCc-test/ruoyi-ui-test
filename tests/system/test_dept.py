"""部门管理功能测试"""
import pytest
import allure

from tests.pages.dashboard_page import DashboardPage
from tests.pages.login_page import LoginPage
from tests.pages.dept_page import DeptPage


@allure.feature("部门管理")
class TestDeptManagement:

    @pytest.fixture(autouse=True)
    def _setup(self, driver, config):
        self._base_url = config.get("base_url", "http://localhost:80")
        login_cfg = config.get("login", {})
        page = LoginPage(driver, timeout=config.get("timeout", 10), config=config)
        page.login(login_cfg.get("username"), login_cfg.get("password"), self._base_url)
        page.wait_login_success()
        dashboard = DashboardPage(driver, timeout=10)
        dashboard.click_menu("部门管理")
        self._page = DeptPage(driver, timeout=config.get("timeout", 10))
        self._page.goto(self._base_url)

    @allure.story("部门列表展示")
    @allure.title("部门管理 - 正常场景: 部门列表展示")
    @pytest.mark.smoke
    def test_dept_list_visible(self):
        count = self._page.get_table_row_count()
        assert count > 0, "部门列表应展示数据"

    @allure.story("搜索部门")
    @allure.title("部门管理 - 边界场景: 搜索不存在的部门")
    def test_search_nonexistent_dept(self):
        self._page.search_dept("nonexistent_dept_xyz")
        count = self._page.get_table_row_count()
        assert count == 0, "搜索不存在部门应无记录"

    @allure.story("重置搜索")
    @allure.title("部门管理 - 边界场景: 重置查询条件")
    def test_reset_search(self):
        self._page.search_dept("nonexistent_dept_xyz")
        self._page.click_reset()
        assert self._page.get_table_row_count() > 0, "重置后应恢复部门列表"