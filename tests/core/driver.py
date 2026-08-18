"""WebDriver 管理模块：按配置创建浏览器驱动实例"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

# 支持的浏览器及对应 Options 类
_BROWSER_OPTIONS = {
    "edge": EdgeOptions,
    "chrome": ChromeOptions,
    "firefox": FirefoxOptions,
}


def _build_options(browser, headless, binary_location=None):
    if browser not in _BROWSER_OPTIONS:
        raise ValueError(f"不支持的浏览器: {browser}，支持 edge/chrome/firefox")
    options = _BROWSER_OPTIONS[browser]()
    if binary_location:
        options.binary_location = binary_location
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--lang=zh-CN")
    return options


def create_driver(browser="edge", headless=True, binary_location=None):
    """创建 WebDriver 实例（依赖 Selenium 内置的 Selenium Manager 自动解析驱动）"""
    options = _build_options(browser, headless, binary_location)
    if browser == "edge":
        return webdriver.Edge(options=options)
    if browser == "chrome":
        return webdriver.Chrome(options=options)
    return webdriver.Firefox(options=options)