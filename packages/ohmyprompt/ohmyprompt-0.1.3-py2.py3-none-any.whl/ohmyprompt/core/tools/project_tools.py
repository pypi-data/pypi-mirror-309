import logging
import os
import threading
import time
from typing import Any

from ...services.config_service import ConfigService
from ...utils.file_utils import get_file_structure
from ...utils.report_manager import ReportManager
from .base import BaseTool
from .mypy_tool import MypyTool
from .radon_tool import RadonTool
from .ruff_tool import RuffTool


class ToolFactory:
    """工具工厂类"""

    _tools: dict[str, type[BaseTool]] = {
        "mypy": MypyTool,
        "ruff": RuffTool,
        "radon": RadonTool,
    }

    @classmethod
    def create_tool(cls, tool_name: str, project_root: str) -> BaseTool:
        """创建工具实例"""
        tool_class = cls._tools.get(tool_name)
        if not tool_class:
            raise ValueError(f"不支持的工具类型: {tool_name}")

        return tool_class(project_root)


class ProjectTools:
    """项目分析工具主类"""

    def __init__(
        self,
        project_root: str = ".",
        update_interval: int = 3600,
        exclude_patterns: dict[str, set[str]] | None = None,
    ):
        """初始化项目分析工具"""
        self.project_root = os.path.abspath(project_root)
        
        # 初始化配置服务
        ConfigService.initialize(self.project_root)
        self.config_service = ConfigService.get_instance()
        
        self.running = False
        self.update_interval = self.config_service.get_update_interval()

        # 获取排除模式
        self.exclude_patterns = self.config_service.get_exclude_patterns()
        if exclude_patterns:
            self.exclude_patterns["directories"].update(exclude_patterns.get("directories", set()))
            self.exclude_patterns["files"].update(exclude_patterns.get("files", set()))

        # 使用 create 类方法创建 ReportManager
        self.history_manager = ReportManager.create()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def start_monitoring(self) -> None:
        """启动持续监控"""
        self.running = True

        def monitoring_loop() -> None:
            while self.running:
                try:
                    print(f"\n开始分析项目: {self.project_root}")
                    self._run_analysis()

                    for _ in range(self.update_interval):
                        if not self.running:
                            break
                        time.sleep(1)

                except Exception as e:
                    print(f"分析过程中出错: {e}")
                    time.sleep(60)

        monitor_thread = threading.Thread(target=monitoring_loop)
        monitor_thread.daemon = True
        monitor_thread.start()

    def _run_analysis(self) -> dict:
        """运行一次完整的项目分析"""
        try:
            print("\n=== 开始项目分析 ===")
            print("配置已加载")

            config = self.config_service.get_config()
            enabled_tools = config.get("tools", {})
            print(
                f"已启用工具: {[name for name, tool in enabled_tools.items() if tool.get('enabled', False)]}"
            )

            try:
                print("正在分析项目结构...")
                structure = get_file_structure(
                    self.project_root,
                    exclude_dirs=self.exclude_patterns["directories"],
                    ignore_patterns=list(self.exclude_patterns["files"]),
                )
                print("项目结构分析完成")
            except Exception as e:
                print(f"获取文件结构失败: {e}")
                structure = {"error": f"获取文件结构失败: {str(e)}"}

            print("\n开始运行工具分析...")
            results = {}

            # 统一使用 ToolFactory 创建和运行工具
            for tool_name, tool_config in enabled_tools.items():
                if tool_config.get("enabled", False):
                    print(f"运行{tool_config['name']}...")
                    try:
                        tool = ToolFactory.create_tool(tool_name, self.project_root)
                        results[tool_name] = tool.run()
                    except Exception as e:
                        results[tool_name] = {
                            "status": "error",
                            "message": f"工具运行失败: {str(e)}"
                        }

            analysis_results = {
                "structure": structure,
                "type_check": results.get("mypy", {}),
                "ruff_check": results.get("ruff", {}),
                "complexity": results.get("radon", {}),
                "timestamp": time.time(),
            }

            print("\n保存分析结果...")
            self.history_manager.save_results(analysis_results)
            print("=== 分析完成 ===\n")

            return analysis_results

        except Exception as e:
            error_msg = f"分析过程中出错: {str(e)}"
            print(f"\n错误: {error_msg}")
            return {
                "status": "error",
                "message": error_msg,
                "timestamp": time.time(),
                "structure": {},
                "type_check": {"status": "error", "message": error_msg},
                "complexity": {"status": "error", "message": error_msg},
            }

    def run_analysis(self) -> dict[str, Any]:
        """运行所有工具分析"""
        results = {}
        enabled_tools = self.config_service.get_config().get("tools", {})
        
        for tool_name, tool_config in enabled_tools.items():
            if tool_config.get("enabled", False):
                try:
                    tool = ToolFactory.create_tool(tool_name, self.project_root)
                    if tool.check_installation():
                        results[tool_name] = tool.run()
                    else:
                        results[tool_name] = {
                            "status": "error",
                            "error": f"{tool_name} 工具未安装"
                        }
                except Exception as e:
                    results[tool_name] = {
                        "status": "error",
                        "error": f"{tool_name} 工具运行失败: {str(e)}"
                    }
        return results
