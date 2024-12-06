import json
from typing import Any

from .base import ReportFormatter


class RadonFormatter(ReportFormatter):
    """Radon复杂度分析结果格式化器"""

    def format(self, complexity: dict[str, Any]) -> list[str]:
        lines = self._format_basic_info(complexity)

        if complexity.get("status") == "ok":
            if "cc" in complexity:
                lines.extend(self._format_cc_data(complexity["cc"]))

            if "mi" in complexity:
                lines.extend(self._format_mi_data(complexity["mi"]))
        elif "message" in complexity:
            lines.extend(["", complexity["message"]])

        return lines

    def _format_basic_info(self, complexity: dict[str, Any]) -> list[str]:
        """格式化基础信息"""
        return [
            "",
            "## 代码复杂度分析",
            f"状态: {complexity.get('status', 'unknown')}",
        ]

    def _format_cc_data(self, cc_data: dict[str, Any]) -> list[str]:
        """格式化圈复杂度数据"""
        lines = [
            "",
            "### 圈复杂度分析",
            "#### 摘要",
            f"- 平均复杂度: {cc_data['summary'].get('average_complexity', 'N/A')}",
            f"- 总体平均复杂度: {cc_data['summary'].get('total_average', 'N/A')}",
            f"- 总函数数量: {cc_data['summary'].get('total_functions', 0)}",
        ]

        if "details" in cc_data:
            complex_funcs = self._filter_complex_functions(cc_data["details"])
            if complex_funcs:
                lines.extend(
                    [
                        "",
                        "#### 需要关注的函数 (复杂度 >= C级别)",
                        "```json",
                        json.dumps(complex_funcs, indent=2, ensure_ascii=False),
                        "```",
                    ]
                )
        return lines

    def _format_mi_data(self, mi_data: dict[str, Any]) -> list[str]:
        """格式化可维护性指标"""
        lines = [
            "",
            "### 可维护性指标",
            "#### 摘要",
            f"- 平均可维护性指标: {mi_data['summary'].get('average_mi', 'N/A')}",
            f"- 分析的文件数: {mi_data['summary'].get('total_files', 0)}",
        ]

        if "details" in mi_data:
            problematic_files = self._filter_problematic_files(mi_data["details"])
            if problematic_files:
                lines.extend(
                    [
                        "",
                        "#### 需要关注的文件",
                        "```json",
                        json.dumps(problematic_files, indent=2, ensure_ascii=False),
                        "```",
                    ]
                )
            else:
                lines.append("\n所有文件的可维护性指标良好 (rank A)")
        return lines

    def _filter_complex_functions(self, details: dict) -> dict:
        """过滤出复杂度较高的函数"""
        filtered = {}
        for file, funcs in details.items():
            complex_funcs = [
                func
                for func in funcs
                if (
                    isinstance(func.get("complexity"), int | float)
                    and func["complexity"] >= 11
                )
                or func.get("rank", "A") >= "C"
            ]
            if complex_funcs:
                filtered[file] = complex_funcs
        return filtered

    def _filter_problematic_files(self, details: dict) -> dict:
        """过滤出需要关注的文件"""
        return {
            path: info for path, info in details.items() if info.get("rank", "A") != "A"
        }
