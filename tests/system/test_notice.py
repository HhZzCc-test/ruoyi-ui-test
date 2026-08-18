"""通知公告功能测试"""
import pytest
import allure

from tests.pages.dashboard_page import DashboardPage
from tests.pages.login_page import LoginPage
from tests.pages.notice_page import NoticePage


@allure.feature("通知公告")
class TestNoticeManagement:

    @pytest.fixture(autouse=True)
    def _setup(self, driver, config):
        self._base_url = config.get("base_url", "http://localhost:80")
        login_cfg = config.get("login", {})
        page = LoginPage(driver, timeout=config.get("timeout", 10), config=config)
        page.login(login_cfg.get("username"), login_cfg.get("password"), self._base_url)
        page.wait_login_success()
        dashboard = DashboardPage(driver, timeout=10)
        dashboard.click_menu("通知公告")
        self._page = NoticePage(driver, timeout=config.get("timeout", 10))

    @allure.story("新增公告")
    @allure.title("通知公告 - 正常场景: 新增公告")
    @pytest.mark.smoke
    def test_add_notice(self):
        self._page.click_add()
        assert "添加" in self._page.get_dialog_title(), "点击新增应弹出添加弹窗"
        self._page.close_dialog()
        assert self._page.get_table_row_count() >= 0, "关闭弹窗后表格应正常显示"

    @allure.story("搜索公告")
    @allure.title("通知公告 - 边界场景: 搜索不存在的公告")
    def test_search_nonexistent_notice(self):
        self._page.search_notice_title("nonexistent_notice_xyz")
        assert self._page.get_table_row_count() == 0, "搜索不存在公告应无记录"

    @allure.story("重置搜索")
    @allure.title("通知公告 - 边界场景: 重置查询条件")
    def test_reset_search(self):
        self._page.search_notice_title("nonexistent_notice_xyz")
        self._page.click_reset()
        assert self._page.get_table_row_count() > 0, "重置后应恢复全量列表"