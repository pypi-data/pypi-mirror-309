from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends

from ..reports.web_report_manager import WebReportManager

router = APIRouter()

def get_report_manager(project_root: str = "") -> WebReportManager:
    """获取报告管理器实例"""
    history_dir = Path(project_root) / ".ohmyprompt" / "history"
    return WebReportManager(history_dir)

@router.get("", response_model=list[dict])
async def get_history_list(
    manager: Annotated[WebReportManager, Depends(get_report_manager)]
):
    """获取报告列表"""
    return manager.get_reports()

@router.delete("/{history_id}")
async def delete_history(
    history_id: str,
    manager: Annotated[WebReportManager, Depends(get_report_manager)]
):
    """删除报告"""
    try:
        manager.remove_report(history_id)
        return True
    except Exception:
        return False
