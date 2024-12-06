"""配置包"""

from typing import TypedDict

from ..config_types import ToolConfig
from .mypy_config import MYPY_CONFIG
from .radon_config import RADON_CONFIG
from .ruff_config import RUFF_CONFIG


class ExcludePatterns(TypedDict):
    directories: list[str]
    files: list[str]


class Tools(TypedDict, total=False):
    mypy: ToolConfig
    radon: ToolConfig
    ruff: ToolConfig


class DefaultConfigType(TypedDict):
    exclude_patterns: ExcludePatterns
    tools: Tools
    update_interval: int


# 配置类型别名
Config = dict[str, ExcludePatterns | Tools | int]


# 默认配置
DEFAULT_CONFIG: DefaultConfigType = {
    "exclude_patterns": {
        "directories": [
            ".*",
            "__*",
            ".git",
            ".venv",
            "__pycache__",
            "node_modules",
            "dist",
            "build",
        ],
        "files": [
            "*.pyc",
            "*.pyo",
            "*.pyd",
            ".DS_Store",
            ".env",
        ],
    },
    "tools": {
        "mypy": MYPY_CONFIG,
        "radon": RADON_CONFIG,
        "ruff": RUFF_CONFIG,
    },
    "update_interval": 3600,
}

# 导入配置管理相关的函数和类
from .manager import (  # noqa: E402
    get_config_manager,
    get_default_config,
    get_project_root,
    init_config,
)

__all__ = [
    "MYPY_CONFIG",
    "RADON_CONFIG",
    "RUFF_CONFIG",
    "DEFAULT_CONFIG",
    "ExcludePatterns",
    "Tools",
    "DefaultConfigType",
    "Config",
    "init_config",
    "get_config_manager",
    "get_project_root",
    "get_default_config",
]
