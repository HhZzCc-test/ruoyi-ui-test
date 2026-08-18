"""登录页 Page Object"""
from redis import Redis
from selenium.webdriver.common.by import By

from tests.core.base_page import BasePage


class LoginPage(BasePage):
    """若依后台登录页（/login）"""

    # ---------- 元素定位器 ----------

    USERNAME = (By.XPATH, '//input[@placeholder="账号"]')
    PASSWORD = (By.XPATH, '//input[@placeholder="密码"]')
    CODE = (By.XPATH, '//input[@placeholder="验证码"]')
    CODE_IMG = (By.CLASS_NAME, "login-code-img")
    LOGIN_BTN = (By.XPATH, '//button[contains(.,"登")]')
    ERROR_MSG = (By.CLASS_NAME, "el-message__content")
    FORM_ERROR = (By.CLASS_NAME, "el-form-item__error")

    def __init__(self, driver, timeout=10, config=None):
        super().__init__(driver, timeout)
        self.config = config or {}

    def open(self, base_url):
        self.driver.get(f"{base_url}/login")

    def fill_username(self, username):
        self.input(*self.USERNAME, username)

    def fill_password(self, password):
        self.input(*self.PASSWORD, password)

    def fill_captcha(self, code):
        self.input(*self.CODE, code)

    def is_captcha_visible(self):
        """验证码输入框是否可见（后端开启验证码时为 True）"""
        return self.is_visible(*self.CODE)

    def submit(self):
        self.click(*self.LOGIN_BTN)

    def wait_login_success(self):
        """登录成功后前端路由跳转至 /index"""
        self.wait_for_url("index")

    def get_error_message(self):
        """获取错误/校验提示（el-message 后端错误 或 el-form-item__error 前端校验）"""
        if self.is_visible(*self.ERROR_MSG):
            return self.get_text(*self.ERROR_MSG)
        if self.is_visible(*self.FORM_ERROR):
            return self.get_text(*self.FORM_ERROR)
        return ""

    # ---------- 验证码自动读取（从 Vue 组件获取 uuid + Redis 读取答案） ----------

    def _get_captcha_uuid_from_page(self):
        """从页面 Vue 组件的 loginForm 中提取验证码 uuid"""
        js_code = """
        function findLoginComponent(vm) {
            if (!vm) return null;
            var name = (vm.$options && vm.$options.name) || '';
            if (name === 'Login') return vm;
            if (vm.$children) {
                for (var i = 0; i < vm.$children.length; i++) {
                    var result = findLoginComponent(vm.$children[i]);
                    if (result) return result;
                }
            }
            return null;
        }
        var app = document.querySelector('#app');
        if (!app || !app.__vue__) return null;
        var loginVm = findLoginComponent(app.__vue__);
        if (loginVm && loginVm.$data && loginVm.$data.loginForm) {
            return loginVm.$data.loginForm.uuid;
        }
        return null;
        """
        uuid = self.driver.execute_script(js_code)
        if not uuid:
            raise RuntimeError("无法从页面 Vue 组件中获取验证码 uuid")
        return uuid

    def fill_captcha_from_redis(self):
        """直连 Redis 读取验证码答案（key: captcha_codes:{uuid}），实现全自动化"""
        redis_cfg = self.config.get("redis", {})
        r = Redis(
            host=redis_cfg.get("host", "localhost"),
            port=redis_cfg.get("port", 6379),
            protocol=2,
            decode_responses=True,
        )
        uuid = self._get_captcha_uuid_from_page()
        code = r.get(f"captcha_codes:{uuid}")
        if code is None:
            raise RuntimeError("无法从 Redis 读取验证码，请确认 Redis 运行或关闭验证码")
        self.fill_captcha(code.strip('"'))

    # ---------- 完整登录流程 ----------

    def login(self, username, password, base_url):
        """一键登录：填账号密码，验证码可见时自动从 Redis 读取"""
        self.open(base_url)
        self.fill_username(username)
        self.fill_password(password)
        if self.is_captcha_visible():
            self.fill_captcha_from_redis()
        self.submit()