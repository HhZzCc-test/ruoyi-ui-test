"""UI 断言工具库：统一元素存在性/文本断言，与 API 项目的断言库思路一致"""
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def assert_element_exists(driver, by, locator, timeout=10, msg=None):
    """断言元素存在（出现在 DOM 中）"""
    assert len(driver.find_elements(by, locator)) > 0, msg or f"元素不存在: {by}={locator}"


def assert_element_visible(driver, by, locator, timeout=10, msg=None):
    """断言元素可见"""
    try:
        WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((by, locator)))
        assert True
    except Exception:
        assert False, msg or f"元素不可见: {by}={locator}"


def assert_element_disappears(driver, by, locator, timeout=10, msg=None):
    """断言元素消失（如弹窗关闭、加载结束）"""
    try:
        WebDriverWait(driver, timeout).until(EC.invisibility_of_element_located((by, locator)))
        assert True
    except Exception:
        assert False, msg or f"元素应消失但仍存在: {by}={locator}"


def assert_text_contains(driver, by, locator, expected, timeout=10, msg=None):
    """断言元素文本包含期望值"""
    el = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((by, locator)))
    actual = el.text
    assert expected in actual, msg or f"元素文本应包含 [{expected}]，实际为 [{actual}]"


def assert_url_contains(driver, keyword, timeout=10, msg=None):
    """断言当前 URL 包含关键字"""
    try:
        WebDriverWait(driver, timeout).until(EC.url_contains(keyword))
        assert True
    except Exception:
        assert False, msg or f"URL 应包含 [{keyword}]，当前为 {driver.current_url}"
