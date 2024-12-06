from pathlib import Path
from typing import Any, Optional, cast

from ..utils.config_utils import ConfigManager
from ..web.config import DEFAULT_CONFIG
from ..web.config_types import ToolConfig


class ConfigService:
    """统一的配置管理服务"""

    _instance: Optional["ConfigService"] = None
    _config_manager: ConfigManager | None = None
    _config: dict[str, Any] = {}

    def __init__(self):
        raise RuntimeError("使用 get_instance() 获取实例")

    @classmethod
    def initialize(cls, project_root: str | Path) -> None:
        """初始化配置服务"""
        if cls._instance is None:
            cls._instance = object.__new__(cls)
            cls._config_manager = ConfigManager(str(project_root))
            cls._load_or_create_config()

    @classmethod
    def get_instance(cls) -> "ConfigService":
        """获取配置服务实例"""
        if cls._instance is None:
            raise RuntimeError("配置服务未初始化")
        return cls._instance

    @classmethod
    def _load_or_create_config(cls) -> None:
        """加载或创建配置"""
        if not cls._config_manager:
            raise RuntimeError("配置管理器未初始化")

        config = cls._config_manager.load_config()
        if not config:
            print("首次运行，使用默认配置")
            config = dict(DEFAULT_CONFIG)
            cls._config_manager.save_config(config)
            # 重新加载以确保配置正确
            config = cls._config_manager.load_config()
            if not config:
                raise RuntimeError("配置初始化失败")

        # 确保配置完整性
        cls._ensure_config_integrity(config)
        cls._config = config

    @classmethod
    def _ensure_config_integrity(cls, config: dict[str, Any]) -> None:
        """确保配置完整性"""
        # 确保所有工具配置存在
        for tool_name, tool_config in DEFAULT_CONFIG["tools"].items():
            if tool_name not in config.get("tools", {}):
                if "tools" not in config:
                    config["tools"] = {}
                config["tools"][tool_name] = tool_config
                print(f"添加缺失的工具配置: {tool_name}")

        if cls._config_manager:
            cls._config_manager.save_config(config)

    def get_tool_config(self, tool_name: str) -> ToolConfig:
        """获取工具配置"""
        tools_config = self._config.get("tools", {})
        tool_config = tools_config.get(tool_name)

        if not tool_config:
            print(f"[{tool_name}] 配置不存在，使用默认配置")
            default_tools = DEFAULT_CONFIG["tools"]
            tool_config = default_tools.get(tool_name)
            if tool_config is None:
                raise ValueError(f"未知的工具名称: {tool_name}")

        return cast(ToolConfig, tool_config)

    def get_config(self) -> dict[str, Any]:
        """获取完整配置"""
        return self._config

    def save_config(self, config: dict[str, Any]) -> None:
        """保存配置"""
        if not self._config_manager:
            raise RuntimeError("配置管理器未初始化")
        self._ensure_config_integrity(config)
        self._config_manager.save_config(config)
        self._config = config

    def get_exclude_patterns(self) -> dict[str, set[str]]:
        """获取排除模式"""
        config_exclude = self._config.get("exclude_patterns", {})
        return {
            "directories": set(config_exclude.get("directories", [])),
            "files": set(config_exclude.get("files", [])),
        }

    def get_update_interval(self) -> int:
        """获取更新间隔"""
        return self._config.get("update_interval", 3600)
