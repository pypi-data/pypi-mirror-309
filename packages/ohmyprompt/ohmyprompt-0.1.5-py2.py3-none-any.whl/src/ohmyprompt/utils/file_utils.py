import fnmatch
import os
from typing import Any

from ..services.config_service import ConfigService


def _should_ignore(
    path: str, ignore_patterns: list[str], exclude_dirs: set[str]
) -> bool:
    """
    检查是否应该忽略该路径

    Args:
        path: 文件或目录路径
        ignore_patterns: 要忽略的文件模式列表
        exclude_dirs: 要排除的目录集合

    Returns:
        bool: 是否应该忽略
    """
    # 获取相对路径的每个部分
    path_parts = path.split(os.sep)

    # 检查路径中的每个部分是否在排除目录列表中
    for part in path_parts:
        if part in exclude_dirs:
            return True

    basename = os.path.basename(path)

    # 忽略所有以点号开头的目录和文件
    if basename.startswith("."):
        return True

    # 忽略所有以双下划线开头的目录和文件
    if basename.startswith("__"):
        return True

    # 检查文件是否匹配忽略模式
    return any(fnmatch.fnmatch(basename, pattern) for pattern in ignore_patterns)


def get_file_structure(
    root_path: str,
    exclude_dirs: set[str] | None = None,
    ignore_patterns: list[str] | None = None,
) -> dict[str, Any]:
    """
    获取项目文件结构

    Args:
        root_path: 项目根目录
        exclude_dirs: 要排除的目录集合
        ignore_patterns: 要忽略的文件/目录模式

    Returns:
        Dict: 文件结构字典
    """
    if ignore_patterns is None or exclude_dirs is None:
        # 从配置服务获取排除模式
        config_service = ConfigService.get_instance()
        exclude_patterns = config_service.get_exclude_patterns()
        
        if ignore_patterns is None:
            ignore_patterns = list(exclude_patterns["files"])
        if exclude_dirs is None:
            exclude_dirs = exclude_patterns["directories"]

    structure: dict[str, Any] = {}

    def _walk(directory: str, struct: dict) -> None:
        try:
            for item in os.listdir(directory):
                path = os.path.join(directory, item)
                if _should_ignore(path, ignore_patterns, exclude_dirs):
                    continue

                if os.path.isfile(path):
                    struct[item] = "file"
                elif os.path.isdir(path) and not os.path.islink(path):
                    struct[item] = {}
                    _walk(path, struct[item])
        except PermissionError:
            struct["error"] = "权限不足"

    _walk(root_path, structure)
    return structure


def should_exclude(
    path: str, project_root: str, exclude_dirs: set[str], exclude_files: list[str]
) -> bool:
    """统一的排除检查逻辑"""
    rel_path = os.path.relpath(path, project_root)
    base_name = os.path.basename(path)
    path_is_dir = os.path.isdir(path)

    # 检查是否是目录
    if path_is_dir:
        # 检查目录排除模式
        for pattern in exclude_dirs:
            # 支持通配符匹配
            if fnmatch.fnmatch(base_name, pattern):
                return True
            # 检查路径中的每个部分
            for part in rel_path.split(os.sep):
                if fnmatch.fnmatch(part, pattern):
                    return True
    else:
        # 检查文件排除模式
        for pattern in exclude_files:
            if fnmatch.fnmatch(base_name, pattern):
                return True

    return False
