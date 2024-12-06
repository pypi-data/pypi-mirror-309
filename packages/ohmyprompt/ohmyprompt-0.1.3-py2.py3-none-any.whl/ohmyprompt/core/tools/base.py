import logging
from abc import ABC, abstractmethod
from typing import Any

from ...services.config_service import ConfigService

logger = logging.getLogger(__name__)


class BaseTool(ABC):
    """工具基类"""

    def __init__(self, project_root: str):
        self.project_root = project_root
        self.config_service = ConfigService.get_instance()

    @abstractmethod
    def run(self) -> dict[str, Any]:
        """运行工具分析"""
        pass

    @abstractmethod
    def check_installation(self) -> bool:
        """检查工具是否已安装"""
        pass

    def build_command(self) -> str:
        """构建工具命令"""
        tool_name = self.get_tool_name()
        tool_config = self.config_service.get_tool_config(tool_name)
        
        base_command = tool_config["command"]
        options = []

        # 处理选项
        for option_id, option in tool_config["options"].items():
            if not isinstance(option, dict) or "value" not in option:
                continue

            value = option.get("value", {})
            if not isinstance(value, dict) or "value" not in value:
                continue

            actual_value = value.get("value")

            # 跳过空值参数
            if actual_value is None or actual_value == "":
                continue
                
            # 跳过特定选项
            if (tool_name == "pyreverse" and option_id == "paths") or \
               (tool_name == "mypy" and option_id == "paths"):
                continue

            # 根据工具特殊处理
            if tool_name == "mypy":
                if isinstance(actual_value, bool) and actual_value:
                    options.append(f"--{option_id}")
                elif isinstance(actual_value, str | int | float) and actual_value:
                    options.extend([f"--{option_id}", str(actual_value)])
            elif tool_name == "ruff":
                if isinstance(actual_value, bool) and actual_value:
                    options.append(f"--{option_id}")
                elif isinstance(actual_value, str | int | float) and actual_value:
                    options.extend([f"--{option_id}", str(actual_value)])
                elif isinstance(actual_value, list | tuple) and actual_value:
                    options.extend([f"--{option_id}", ",".join(str(v) for v in actual_value)])
            elif tool_name == "pyreverse":
                if isinstance(actual_value, bool) and actual_value:
                    options.append(f"--{option_id}")
                elif isinstance(actual_value, str | int | float) and actual_value:
                    if option_id == "output_directory":
                        options.extend(["-d", str(actual_value)])
                    else:
                        options.extend([f"--{option_id}", str(actual_value)])
            elif tool_name == "radon":
                if isinstance(actual_value, bool) and actual_value:
                    options.append(f"--{option_id}")
                elif isinstance(actual_value, str | int | float) and actual_value:
                    options.extend([f"--{option_id}", str(actual_value)])

        # 构建完整命令
        cmd_parts = [base_command]
        
        # 特殊处理 pyreverse 的路径参数
        if tool_name == "pyreverse":
            cmd_parts.append("src/")  # 先添加源代码路径
            cmd_parts.extend(options)  # 然后添加选项
        else:
            cmd_parts.extend(options)
            cmd_parts.append("src/")  # 其他工具在最后添加路径

        cmd = " ".join(cmd_parts)
        print(f"执行命令: {cmd}")
        return cmd

    @abstractmethod
    def get_tool_name(self) -> str:
        """获取工具名称"""
        pass
