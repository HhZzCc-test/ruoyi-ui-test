"""根级 conftest：全局 fixtures 与失败自动截图钩子"""
import os
import allure
import pytest

from tests.core.driver import create_driver
from tests.core.config import load_config


@pytest.fixture(scope="session")
def config():
    """加载环境配置（config.yaml）"""
    return load_config()


@pytest.fixture(scope="function")
def driver(config):
    """创建并销毁 WebDriver 实例"""
    browser = config.get("browser", "edge")
    headless = config.get("headless", True)
    binary = config.get("binary_location", None)
    web = create_driver(browser=browser, headless=headless, binary_location=binary)
    web.maximize_window()
    yield web
    web.quit()


@pytest.fixture(scope="function")
def base_url(config):
    """若依前端基础地址"""
    return config.get("base_url", "http://localhost:80")


def pytest_runtest_makereport(item, call):
    """测试失败时自动截图：附加到 Allure 报告并落盘 allure-results/screenshots/"""
    if call.when == "call" and call.excinfo is not None:
        driver = item.funcargs.get("driver")
        if driver is not None:
            try:
                screenshot = driver.get_screenshot_as_png()
                allure.attach(
                    screenshot,
                    name=f"{item.name}_failure_screenshot",
                    attachment_type=allure.attachment_type.PNG,
                )
                shot_dir = os.path.join("allure-results", "screenshots")
                os.makedirs(shot_dir, exist_ok=True)
                path = os.path.join(shot_dir, f"{item.name}_failure.png")
                with open(path, "wb") as f:
                    f.write(screenshot)
            except Exception:
                # 截图失败不应影响测试结论
                pass