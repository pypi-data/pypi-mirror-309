import logging
from datetime import datetime
from pathlib import Path

from ..services.config_service import ConfigService
from .formatters.formatter_factory import FormatterFactory

logger = logging.getLogger(__name__)


class ReportManager:
    """分析报告管理器 - 核心功能"""

    def __init__(self, history_path: Path):
        """初始化报告管理器
        
        Args:
            history_path: 历史记录目录的路径
        """
        self.config_service = ConfigService.get_instance()
        self.history_path = history_path
        self.history_path.mkdir(parents=True, exist_ok=True)

        # 从配置服务获取模板
        template_path = (
            Path(__file__).parent.parent / "templates" / "report_template.md"
        )
        if not template_path.exists():
            logger.warning(f"模板文件不存在: {template_path}")
        self.template = template_path.read_text() if template_path.exists() else ""
        self.formatter_factory = FormatterFactory()

    @classmethod
    def create(cls) -> "ReportManager":
        """创建报告管理器实例"""
        config_service = ConfigService.get_instance()
        if not config_service._config_manager:
            raise RuntimeError("配置管理器未初始化")
        history_path = Path(config_service._config_manager.get_history_path())
        return cls(history_path)

    def save_results(self, results: dict) -> None:
        """保存分析结果为 Markdown 格式"""
        try:
            timestamp = str(int(results["timestamp"]))
            result_file = self.history_path / f"{timestamp}.md"

            markdown_content = [
                "# 项目分析报告",
                "",
                "## 分析时间",
                datetime.fromtimestamp(float(timestamp)).strftime("%Y-%m-%d %H:%M:%S"),
                "",
                "## 文件结构",
                "```filetree",
            ]

            # 添加文件结构
            markdown_content.extend(self._format_structure(results["structure"]))
            markdown_content.append("```")

            # 使用对应的formatter处理各个工具的结果
            for tool_name, tool_results in results.items():
                if tool_name in ["timestamp", "structure"]:
                    continue

                if isinstance(tool_results, dict):
                    try:
                        formatter = self.formatter_factory.get_formatter(tool_name)
                        markdown_content.extend(formatter.format(tool_results))
                    except ValueError as e:
                        logger.warning(f"格式化器错误: {e}")
                    except Exception as e:
                        logger.error(f"处理 {tool_name} 结果时发生错误: {e}")

            result_file.write_text("\n".join(markdown_content))
            logger.info(f"分析结果已保存到: {result_file}")
        except Exception as e:
            logger.error(f"保存分析结果时发生错误: {e}")
            raise

    def _format_structure(self, structure: dict, indent: int = 0) -> list[str]:
        """格式化文件结构为树形结构"""
        try:
            lines = []
            items = sorted(structure.items())
            for i, (name, value) in enumerate(items):
                is_last = i == len(items) - 1
                prefix = "  " * indent
                if indent > 0:
                    prefix = prefix[:-2] + ("└─ " if is_last else "├─ ")

                if isinstance(value, dict):
                    lines.append(f"{prefix}{name}/")
                    # 为子目录添加正确的缩进前缀
                    next_indent = indent + 1
                    if indent > 0:
                        next_indent = indent + 2
                    lines.extend(self._format_structure(value, next_indent))
                else:
                    lines.append(f"{prefix}{name}")
            return lines
        except Exception as e:
            logger.error(f"格式化文件结构时发生错误: {e}")
            return []

    def generate_report(self, analysis_results: dict) -> str:
        """生成分析报告"""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # 格式化各个工具的结果
            formatted_results = {}
            for tool_name in [
                "ruff_check",
                "type_check",
                "complexity",
                "pydeps",
            ]:
                tool_results = analysis_results.get(tool_name, {})
                status = "ok" if tool_results.get("status") == "ok" else "error"

                try:
                    formatter = self.formatter_factory.get_formatter(tool_name)
                    content = formatter.format(tool_results)
                    formatted_results[f"{tool_name}_status"] = status
                    formatted_results[f"{tool_name}_content"] = "\n".join(content)
                except Exception as e:
                    logger.error(f"格式化 {tool_name} 结果时发生错误: {e}")
                    formatted_results[f"{tool_name}_status"] = "error"
                    formatted_results[f"{tool_name}_content"] = f"格式化错误: {str(e)}"

            # 格式化文件结构
            structure_lines = self._format_structure(
                analysis_results.get("structure", {})
            )
            formatted_results["structure"] = "\n".join(
                ["```filetree", *structure_lines, "```"]
            )
            formatted_results["timestamp"] = timestamp

            return self.template.format(**formatted_results)
        except Exception as e:
            logger.error(f"生成报告时发生错误: {e}")
            raise
