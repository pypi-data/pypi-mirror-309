from typing import cast

from fastapi import APIRouter, HTTPException

from ...services.config_service import ConfigService
from ...web.config import Config, ExcludePatterns

router = APIRouter()


@router.get("")
async def get_exclude_patterns() -> ExcludePatterns:
    """获取排除模式"""
    try:
        config_service = ConfigService.get_instance()
        exclude_patterns = config_service.get_exclude_patterns()
        
        # 转换 set 为 list，以符合 ExcludePatterns 类型
        return cast(ExcludePatterns, {
            "directories": list(exclude_patterns["directories"]),
            "files": list(exclude_patterns["files"]),
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("")
async def update_exclude_patterns(patterns: ExcludePatterns) -> dict[str, str]:
    """更新排除模式"""
    try:
        config_service = ConfigService.get_instance()
        config = config_service.get_config()
        
        # 更新排除模式
        config["exclude_patterns"] = patterns
        config_service.save_config(cast(Config, config))
        
        return {"message": "排除模式已更新"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
