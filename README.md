# RuoYi Web 功能自动化测试

## 项目介绍

本项目是**若依（RuoYi）后台管理系统**的 Web UI 功能自动化测试框架，基于 **Selenium + Pytest + Allure** 技术栈从零搭建，采用 **Page Object Model（POM）** 设计模式，覆盖登录、用户管理、菜单导航等核心功能场景，实现 UI 功能回归自动化与可视化报告输出。



### 技术栈

| 组件 | 版本 | 用途 |
|------|------|------|
| Python | 3.8+ | 开发语言 |
| selenium | >=4.15 | 浏览器自动化，驱动 Web UI |
| pytest | >=7.4 | 测试框架，用例组织、fixture 管理 |
| allure-pytest | >=2.13 | 生成 Allure 可视化测试报告 |
| PyYAML | >=6.0 | 多环境配置管理 |
| redis | >=4.0 | 直连 Redis 读取登录验证码答案 |

### 设计亮点

- **Page Object Model**：页面对象（`tests/pages/`）与测试逻辑（`tests/test_*.py`）完全分离，页面元素变更只改页面类，不动测试用例
- **BasePage 统一封装**：显式等待、点击/输入/取文本等操作收敛到基类，消除样板代码
- **验证码全自动**：直连 Redis 读取验证码答案（key: `captcha_codes:{uuid}`），登录流程无需人工干预
- **失败自动截图**：`pytest_runtest_makereport` 钩子捕获失败瞬间截图，自动附加到 Allure 报告并落盘
- **显式等待机制**：所有操作基于 `WebDriverWait` 显式等待，消除隐式等待的时序问题
- **多浏览器支持**：通过 `config.yaml` 一键切换 `edge / chrome / firefox`，支持 headless 模式
- **多环境配置**：环境、账号、超时等集中在 `config.yaml`，修改即生效
- **用例文档驱动**：`doc/testcases/` 用例规格文档与测试代码一一对应（TC 编号贯穿）

### 测试覆盖范围

| 模块 | 测试文件 | 覆盖场景 |
|------|---------|---------|
| **登录功能** | `test_login.py` | 正确登录、错误密码、空表单校验、退出登录 |
| **用户管理** | `test_user_mgmt.py` | 新增用户、搜索存在/不存在用户、重置查询 |
| **菜单导航** | `test_navigation.py` | 侧边栏菜单展示、点击菜单路由跳转 |

---

## 环境准备

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动若依前端

测试默认连接 `http://localhost:80`（若依 Vue 前端默认端口），请确保前端与后端服务已启动。

### 3. 配置浏览器

`config.yaml` 中 `browser` 支持 `edge / chrome / firefox`。驱动由 Selenium 内置的 **Selenium Manager** 自动解析下载，无需手动配置。

### 4. 验证码处理

`login.captcha_enabled` 为 `true` 时，框架自动从 Redis（`captcha_codes:{uuid}`）读取验证码答案。若测试环境后端关闭了验证码，保持默认即可自动跳过。

---

## 项目结构

```
ruoyi-ui-test/
├── config.yaml                  # 环境配置（地址/浏览器/账号/超时）
├── conftest.py                  # 全局 fixtures + 失败截图钩子
├── pytest.ini                   # pytest 全局配置
├── requirements.txt             # 依赖清单
├── README.md                    # 项目说明
│
├── tests/
│   ├── core/                    # 核心基础设施
│   │   ├── driver.py            # WebDriver 管理（多浏览器/headless）
│   │   ├── base_page.py         # BasePage 页面基类
│   │   ├── assertions.py        # UI 断言工具库
│   │   └── config.py            # 配置加载
│   ├── pages/                   # 页面对象（POM）
│   │   ├── login_page.py        # 登录页
│   │   ├── dashboard_page.py    # 主布局/侧边栏导航
│   │   └── user_page.py         # 用户管理页
│   ├── test_login.py            # 登录功能测试
│   ├── test_user_mgmt.py        # 用户管理测试
│   └── test_navigation.py       # 菜单导航测试
│
├── doc/testcases/               # 测试用例文档
│   ├── README.md                # 用例汇总索引
│   ├── TC-LOGIN-登录.md
│   ├── TC-USER-用户管理.md
│   └── TC-NAV-导航.md
│
└── allure-results/              # Allure 原始结果数据
```

---

## 运行测试

### 运行所有测试

```bash
pytest
```

### 按模块运行

```bash
pytest tests/test_login.py        # 登录功能
pytest tests/test_user_mgmt.py    # 用户管理
pytest tests/test_navigation.py   # 菜单导航
```

### 按标记筛选

| 标记 | 说明 | 示例 |
|------|------|------|
| `smoke` | 冒烟测试 | `pytest -m smoke` |
| `critical` | 关键测试 | `pytest -m critical` |

### 本机调试（非 headless）

```bash
# 修改 config.yaml 中 headless: false 后
pytest tests/test_login.py::TestLogin::test_login_success -v
```

### 生成 Allure 报告

```bash
allure serve allure-results
```

---

## 配置说明

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `base_url` | `http://localhost:80` | 若依前端地址 |
| `browser` | `edge` | 浏览器类型（edge/chrome/firefox） |
| `headless` | `true` | 无头模式 |
| `timeout` | `10` | 显式等待超时（秒） |
| `login.username/password` | `admin` / `admin123` | 默认登录账号 |
| `redis.host/port` | `localhost` / `6379` | 验证码 Redis 缓存地址 |

---

## 常见问题

### 元素定位失败

不同版本的若依前端元素 id/class 可能存在差异。若定位失败，依据实际页面微调 `tests/pages/` 中对应页面类的定位器即可，页面动作与测试逻辑无需改动。

### 验证码读取失败

请确认 Redis 正常运行且测试环境可访问；或检查 `login.captcha_enabled` 与实际后端配置是否一致。

### headless 模式点击不生效

部分若依弹窗在 headless 下存在动画时序问题，可将 `config.yaml` 中 `headless` 设为 `false` 调试，或适当增大 `timeout`。
