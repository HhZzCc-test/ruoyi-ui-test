"""登录功能测试（对应 doc/testcases/TC-LOGIN-登录.md）"""
import pytest
import allure

from tests.core.assertions import assert_url_contains
from tests.pages.dashboard_page import DashboardPage
from tests.pages.login_page import LoginPage


@allure.feature("登录功能")
class TestLogin:

    @pytest.fixture(autouse=True)
    def _setup(self, driver, config):
        self._base_url = config.get("base_url", "http://localhost:80")
        self._username = config.get("login", {}).get("username", "admin")
        self._password = config.get("login", {}).get("password", "admin123")
        self._page = LoginPage(driver, timeout=config.get("timeout", 10), config=config)

    @allure.story("正常登录")
    @allure.title("登录 - 正常场景: 正确账号密码登录成功")
    @pytest.mark.smoke
    def test_login_success(self, driver):
        """TC-LOGIN-001: 正确账号密码登录成功"""
        self._page.login(self._username, self._password, self._base_url)
        self._page.wait_login_success()
        assert_url_contains(driver, "index", msg="登录成功应跳转到首页")
        menus = DashboardPage(driver, timeout=10).get_menus()
        assert len(menus) > 0, "登录成功后侧边栏应展示系统菜单"

    @allure.story("异常登录")
    @allure.title("登录 - 异常场景: 错误密码登录失败")
    @pytest.mark.critical
    def test_login_wrong_password(self, driver):
        """TC-LOGIN-002: 错误密码登录失败"""
        self._page.open(self._base_url)
        self._page.fill_username(self._username)
        self._page.fill_password("wrong_password_123")
        if self._page.is_captcha_visible():
            self._page.fill_captcha_from_redis()
        self._page.submit()
        assert "login" in self._page.get_url(), "登录失败应停留在登录页"
        msg = self._page.get_error_message()
        assert msg, "登录失败应出现错误提示"

    @allure.story("参数校验")
    @allure.title("登录 - 边界场景: 空账号密码提交")
    def test_login_empty_fields(self, driver):
        """TC-LOGIN-003: 空账号密码提交"""
        self._page.open(self._base_url)
        self._page.submit()
        assert "login" in self._page.get_url(), "空表单提交应停留在登录页"
        msg = self._page.get_error_message()
        assert msg, "空表单提交应出现校验提示"

    @allure.story("退出登录")
    @allure.title("登录 - 正常场景: 登录后退出回到登录页")
    @pytest.mark.smoke
    def test_logout(self, driver):
        """TC-LOGIN-004: 登录后退出"""
        self._page.login(self._username, self._password, self._base_url)
        self._page.wait_login_success()
        DashboardPage(driver, timeout=10).logout()
        assert_url_contains(driver, "login", msg="退出后应回到登录页")