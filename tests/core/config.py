"""环境配置加载模块

从项目根目录的 config.yaml 读取测试环境配置，
支持多环境切换（修改 config.yaml 即可）。
"""
from pathlib import Path

import yaml

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
CONFIG_PATH = ROOT_DIR / "config.yaml"


def load_config():
    """加载 config.yaml 并返回 dict"""
    with open(CONFIG_PATH, encoding="utf-8") as f:
        return yaml.safe_load(f)
