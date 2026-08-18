"""主布局/侧边栏导航 Page Object"""
import time

from selenium.webdriver.common.by import By

from tests.core.base_page import BasePage


class DashboardPage(BasePage):
    """若依主布局页面（登录后）——提供侧边栏菜单与登出操作"""

    SIDEBAR_ITEM = (By.CSS_SELECTOR, ".el-menu-item, .el-submenu__title")
    AVATAR = (By.CSS_SELECTOR, ".avatar-wrapper")
    LOGOUT_ITEM = (By.XPATH, "//span[contains(text(),'退出登录')]")

    def get_menus(self):
        """返回侧边栏可见菜单文本列表（使用 textContent 兼容折叠状态）"""
        elements = self.driver.find_elements(*self.SIDEBAR_ITEM)
        result = []
        for el in elements:
            text = (el.get_attribute('textContent') or '').strip()
            if text:
                result.append(text)
        return result

    def expand_sidebar(self):
        """如果侧边栏是折叠状态，点击 hamburger 按钮展开"""
        collapsed = self.driver.find_elements(By.CSS_SELECTOR, '.el-menu--collapse')
        if collapsed:
            self.click(By.CSS_SELECTOR, '.hamburger-container')
            time.sleep(0.5)

    def click_menu(self, menu_text):
        """点击侧边栏菜单项，自动展开侧边栏和父级子菜单（通过 JS 点击，兼容折叠状态）"""
        self.expand_sidebar()
        time.sleep(0.5)
        js = f"""
        (function() {{
            var target = '{menu_text}';
            var allItems = document.querySelectorAll('.el-menu-item, .el-submenu__title');
            for (var i = 0; i < allItems.length; i++) {{
                var text = (allItems[i].textContent || '').trim();
                if (text === target) {{
                    allItems[i].click();
                    return 'clicked';
                }}
            }}
            return 'not found';
        }})();
        """
        result = self.driver.execute_script(js)
        if 'not found' in str(result):
            raise Exception(f"菜单项 [{menu_text}] 未找到")

    def click_profile(self):
        """点击头像下拉 → 个人中心"""
        self.click(*self.AVATAR)
        time.sleep(0.4)
        js = """
        (function() {
            var items = document.querySelectorAll('.el-dropdown-menu__item');
            for (var i = 0; i < items.length; i++) {
                if (items[i].textContent.indexOf('个人中心') >= 0) {
                    items[i].click();
                    return 'clicked';
                }
            }
            return 'not found';
        })();
        """
        self.driver.execute_script(js)
        time.sleep(0.5)

    def logout(self):
        """点击头像 → 退出登录，等待回到登录页"""
        self.click(*self.AVATAR)
        time.sleep(0.5)
        # 通过 JS 调用 Vuex store 的 FedLogOut 并跳转到登录页
        js_code = """
        (function() {
            var app = document.querySelector('#app');
            if (!app || !app.__vue__) return 'vue not found';
            var store = app.__vue__.$store;
            if (store) {
                store.dispatch('FedLogOut');
                location.href = '/login';
                return 'FedLogOut dispatched';
            }
            return 'store not found';
        })();
        """
        self.driver.execute_script(js_code)
        self.wait_for_url("login")