"""配置管理器"""

from typing import Any, cast

from ...utils.config_utils import ConfigManager
from . import DEFAULT_CONFIG, Config


class ConfigManagerSingleton:
    _instance: ConfigManager | None = None
    _initialized: bool = False

    @classmethod
    def init(cls, root_path: str) -> None:
        """初始化配置管理器"""
        if not cls._initialized:
            cls._instance = ConfigManager(root_path)

            # 如果配置文件不存在，创建默认配置
            config = cls._instance.load_config()
            if not config:
                print("初始化默认配置...")
                cls._instance.save_config(cast(dict[str, Any], DEFAULT_CONFIG))
                # 重新加载以确保配置正确
                config = cls._instance.load_config()
                if not config:
                    raise RuntimeError("配置初始化失败")
            cls._initialized = True

    @classmethod
    def get_instance(cls) -> ConfigManager | None:
        """获取配置管理器实例"""
        return cls._instance


def init_config(root_path: str) -> None:
    """初始化配置管理器"""
    ConfigManagerSingleton.init(root_path)


def get_config_manager() -> ConfigManager | None:
    """获取配置管理器实例"""
    return ConfigManagerSingleton.get_instance()


def get_project_root() -> str:
    """获取项目根目录"""
    config_manager = get_config_manager()
    if not config_manager:
        raise RuntimeError("配置管理器未初始化")
    return str(config_manager.project_root)


def get_default_config() -> Config:
    """获取默认配置的字典版本"""
    return cast(Config, DEFAULT_CONFIG)
