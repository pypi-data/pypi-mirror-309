import json
import subprocess
from typing import Any, TypedDict, cast

from ...utils.shell_utils import execute_bash
from .base import BaseTool


class CommandValue(TypedDict):
    """命令值类型"""
    value: list[str]


class CommandOption(TypedDict):
    """命令选项类型"""
    value: CommandValue


class RadonTool(BaseTool):
    """Radon 代码复杂度分析工具"""

    def get_tool_name(self) -> str:
        return "radon"

    def check_installation(self) -> bool:
        """检查 radon 是否已安装"""
        cmd = f"cd {self.project_root} && rye run radon --version"
        stdout, stderr, code = execute_bash(cmd)
        return code == 0

    def run(self) -> dict[str, Any]:
        """运行工具"""
        try:
            tool_config = self.config_service.get_tool_config("radon")
            options = tool_config.get("options", {})
            
            # 获取命令列表，使用类型安全的方式
            commands_option = cast(CommandOption, options.get("commands", {}))
            value_dict = commands_option.get("value", {})
            commands = value_dict.get("value", ["cc", "mi"]) if isinstance(value_dict, dict) else ["cc", "mi"]

            results = {}
            for cmd in commands:
                raw_output = self._run_radon_command(cmd, options)
                try:
                    results[cmd] = self._handle_command_output(cmd, raw_output)
                except Exception as e:
                    results[cmd] = self._create_error_result(str(e))

            return {"status": "ok", **results}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def _run_radon_command(self, cmd: str, options: dict[str, Any]) -> str:
        """运行指定的 radon 命令"""
        cmd_args = self._prepare_radon_args(cmd, options)
        cmd_args.append(self.project_root)

        result = subprocess.run(cmd_args, capture_output=True, text=True)
        return result.stdout

    def _prepare_radon_args(self, cmd: str, options: dict[str, Any]) -> list[str]:
        """准备 radon 命令的参数"""
        cmd_args = ["radon", cmd]

        if cmd == "cc":
            for option in [
                "cc_min",
                "cc_max",
                "show_complexity",
                "average",
                "total_average",
            ]:
                option_value = options.get(option, {}).get("value", {}).get("value")
                if option_value:
                    if option in ["cc_min", "cc_max"]:
                        cmd_args.extend(
                            [f"--{option.replace('_', '-')}", str(option_value)]
                        )
                    else:
                        cmd_args.append(f"--{option.replace('_', '-')}")

        elif cmd == "mi":
            for option in ["multi", "show"]:
                if options.get(option, {}).get("value", {}).get("value"):
                    cmd_args.append(f"--{option}")

        # 添加通用选项
        if options.get("json", {}).get("value", {}).get("value"):
            cmd_args.append("--json")

        return cmd_args

    def _handle_command_output(self, cmd: str, raw_output: str) -> dict[str, Any]:
        """处理命令输出"""
        handlers = {
            "cc": self._handle_cc_output,
            "mi": self._handle_mi_output,
            "raw": self._handle_raw_output,
            "hal": self._handle_hal_output,
        }

        handler = handlers.get(cmd)
        if not handler:
            return self._create_error_result(f"不支持的命令: {cmd}")

        return handler(raw_output)

    def _handle_cc_output(self, raw_output: str) -> dict[str, Any]:
        """处理圈复杂度输出"""
        try:
            data = json.loads(raw_output)
            complexity_data = self._process_complexity_data(data)
            stats = self._calculate_complexity_stats(complexity_data)

            return {
                "summary": {
                    "average_complexity": stats["average"],
                    "total_functions": stats["total_functions"],
                    "c_grade_count": stats["c_grade_count"],
                },
                "details": complexity_data,
            }
        except Exception as e:
            return self._create_error_result(f"处理 CC 输出失败: {str(e)}")

    def _handle_mi_output(self, raw_output: str) -> dict[str, Any]:
        """处理可维护性指数输出"""
        try:
            mi_data = json.loads(raw_output)
            mi_values = [
                float(value)
                for value in mi_data.values()
                if self._is_valid_number(value)
            ]
            average_mi = sum(mi_values) / len(mi_values) if mi_values else 0

            return {
                "summary": {
                    "average_mi": round(average_mi, 2),
                    "total_files": len(mi_data),
                },
                "details": mi_data,
            }
        except Exception as e:
            return self._create_error_result(f"处理 MI 输出失败: {str(e)}")

    def _handle_raw_output(self, raw_output: str) -> dict[str, Any]:
        """处理原始指标输出"""
        try:
            return {"summary": {}, "details": json.loads(raw_output)}
        except Exception as e:
            return self._create_error_result(f"处理 RAW 输出失败: {str(e)}")

    def _handle_hal_output(self, raw_output: str) -> dict[str, Any]:
        """处理 Halstead 指标输出"""
        try:
            return {"summary": {}, "details": json.loads(raw_output)}
        except Exception as e:
            return self._create_error_result(f"处理 HAL 输出失败: {str(e)}")

    def _process_complexity_data(self, data: dict[str, Any]) -> dict[str, Any]:
        """处理复杂度数据"""
        result = {}
        for file_path, functions in data.items():
            if not functions:
                continue

            result[file_path] = [
                {
                    "name": func["name"],
                    "line": func["lineno"],
                    "complexity": func["complexity"],
                    "type": self._get_function_type(func),
                }
                for func in functions
            ]
        return result

    def _calculate_complexity_stats(
        self, complexity_data: dict[str, Any]
    ) -> dict[str, Any]:
        """计算复杂度统计信息"""
        all_complexities = []
        c_grade_count = 0

        for file_functions in complexity_data.values():
            for func in file_functions:
                complexity = func["complexity"]
                all_complexities.append(complexity)
                if complexity >= 5:  # C 级别的复杂度阈值
                    c_grade_count += 1

        total_functions = len(all_complexities)
        if not total_functions:
            return {"average": 0, "total_functions": 0, "c_grade_count": 0}

        return {
            "average": round(sum(all_complexities) / total_functions, 2),
            "total_functions": total_functions,
            "c_grade_count": c_grade_count,
        }

    def _get_function_type(self, func: dict[str, Any]) -> str:
        """确定函数类型"""
        if func.get("type") == "class":
            return "class"
        return "method" if func.get("classname") else "function"

    def _is_valid_number(self, value: Any) -> bool:
        """检查值是否可以转换为数字"""
        try:
            float(value)
            return True
        except (ValueError, TypeError):
            return False

    def _create_error_result(self, error_message: str) -> dict[str, Any]:
        """创建统一的错误结果格式"""
        return {"summary": {}, "details": {}, "error": {"message": error_message}}
