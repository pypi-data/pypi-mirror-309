import json
from pathlib import Path
from typing import TypedDict

from fastapi import APIRouter, HTTPException


class ConfigResult(TypedDict):
    status: str
    message: str


class ApiConfigManager:
    def __init__(self, config_file: Path):
        self.config_file = config_file
        self._ensure_config_file()

    def _ensure_config_file(self):
        """确保配置文件存在"""
        if not self.config_file.exists():
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            self.config_file.write_text("{}")

    def load_config(self) -> dict:
        """加载配置"""
        try:
            return json.loads(self.config_file.read_text())
        except Exception:
            return {}

    def save_config(self, config: dict):
        """保存配置"""
        self.config_file.write_text(json.dumps(config, indent=2))


config_manager: ApiConfigManager | None = None


def init_config(project_root: str) -> None:
    """初始化配置管理器"""
    global config_manager
    config_file = Path(project_root) / ".ohmyprompt" / "config.json"
    config_manager = ApiConfigManager(config_file)


# API 路由
router = APIRouter()


@router.get("", response_model=dict)
async def get_config():
    """获取配置"""
    if not config_manager:
        raise HTTPException(status_code=500, detail="配置管理器未初始化")
    return config_manager.load_config()


@router.post("", response_model=dict)
async def update_config(config: dict):
    """更新配置"""
    if not config_manager:
        raise HTTPException(status_code=500, detail="配置管理器未初始化")
    config_manager.save_config(config)
    return {"success": True, "message": "配置已更新"}
