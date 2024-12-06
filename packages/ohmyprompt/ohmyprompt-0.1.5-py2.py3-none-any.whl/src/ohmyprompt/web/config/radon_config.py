from ..config_types import ToolConfig, ToolOptionType

RADON_CONFIG: ToolConfig = {
    "name": "Radon",
    "description": "Python 代码复杂度分析工具",
    "enabled": True,
    "command": "radon",
    "options": {
        "commands": {
            "name": "分析命令",
            "description": "选择要执行的分析命令(可多选)",
            "value": {
                "type": ToolOptionType.MULTI_SELECT,
                "value": ["cc", "mi", "raw"],
                "choices": ["cc", "mi", "raw", "hal"],
                "choices_desc": {
                    "cc": "圈复杂度分析 - 计算代码的复杂度评分(A-F)",
                    "mi": "可维护性指标 - 计算代码的可维护性评分(A-C)",
                    "raw": "原始指标 - 计算代码行数等基础指标",
                    "hal": "Halstead复杂度 - 计算代码的Halstead复杂度指标",
                },
            },
        },
        "paths": {
            "name": "分析路径",
            "description": "要分析的文件或目录路径，多个路径用空格分隔",
            "value": {
                "type": ToolOptionType.TEXT,
                "value": "src/",
            },
        },
        "cc_min": {
            "name": "CC最低复杂度等级",
            "description": "只显示大于等于此复杂度等级的函数",
            "value": {
                "type": ToolOptionType.SELECT,
                "value": "C",
                "choices": ["A", "B", "C", "D", "E", "F"],
                "choices_desc": {
                    "A": "1-5 分 - 低复杂度(简单代码块)",
                    "B": "6-10 分 - 低复杂度(结构良好且稳定)",
                    "C": "11-20 分 - 中等复杂度(稍微复杂)",
                    "D": "21-30 分 - 较高复杂度(更复杂)",
                    "E": "31-40 分 - 高复杂度(复杂,需警惕)",
                    "F": "41+ 分 - 极高复杂度(容易出错,不稳定)",
                },
            },
        },
        "cc_max": {
            "name": "CC最高复杂度等级",
            "description": "只显示小于等于此复杂度等级的函数",
            "value": {
                "type": ToolOptionType.SELECT,
                "value": "F",
                "choices": ["A", "B", "C", "D", "E", "F"],
            },
        },
        "show_complexity": {
            "name": "显示复杂度分数",
            "description": "显示具体的复杂度分数",
            "value": {"type": str(ToolOptionType.BOOLEAN), "value": True},
        },
        "average": {
            "name": "显示平均复杂度",
            "description": "显示分析范围内的平均复杂度",
            "value": {"type": str(ToolOptionType.BOOLEAN), "value": True},
        },
        "total_average": {
            "name": "显示总体平均复杂度",
            "description": "显示所有代码块的平均复杂度，不受min/max限制",
            "value": {"type": str(ToolOptionType.BOOLEAN), "value": True},
        },
        "no_assert": {
            "name": "忽略断言",
            "description": "不计算断言语句的复杂度",
            "value": {"type": str(ToolOptionType.BOOLEAN), "value": True},
        },
        "order": {
            "name": "排序方式",
            "description": "结果排序方式",
            "value": {
                "type": ToolOptionType.SELECT,
                "value": "SCORE",
                "choices": ["SCORE", "LINES", "ALPHA"],
                "choices_desc": {
                    "SCORE": "按复杂度分数排序",
                    "LINES": "按代码行数排序",
                    "ALPHA": "按名称字母顺序排序",
                },
            },
        },
        "mi_min": {
            "name": "MI最低等级",
            "description": "只显示大于等于此可维护性等级的结果",
            "value": {
                "type": ToolOptionType.SELECT,
                "value": "A",
                "choices": ["A", "B", "C"],
                "choices_desc": {
                    "A": "20-100分 - 非常好维护",
                    "B": "10-19分 - 一般可维护",
                    "C": "0-9分 - 难以维护",
                },
            },
        },
        "mi_max": {
            "name": "MI最高等级",
            "description": "只显示小于等于此可维护性等级的结果",
            "value": {
                "type": ToolOptionType.SELECT,
                "value": "C",
                "choices": ["A", "B", "C"],
            },
        },
        "multi": {
            "name": "多行字符串处理",
            "description": "不将多行字符串计入注释",
            "value": {"type": str(ToolOptionType.BOOLEAN), "value": True},
        },
        "show_mi": {
            "name": "显示MI值",
            "description": "显示具体的可维护性指标值",
            "value": {"type": str(ToolOptionType.BOOLEAN), "value": True},
        },
        "summary": {
            "name": "显示汇总",
            "description": "在分析结束时显示指标汇总",
            "value": {"type": str(ToolOptionType.BOOLEAN), "value": True},
        },
        "functions": {
            "name": "函数级别分析",
            "description": "在函数级别而不是文件级别计算指标",
            "value": {"type": str(ToolOptionType.BOOLEAN), "value": False},
        },
        "json": {
            "name": "JSON输出",
            "description": "以JSON格式输出结果",
            "value": {"type": str(ToolOptionType.BOOLEAN), "value": True},
        },
        "xml": {
            "name": "XML输出",
            "description": "以XML格式输出结果(专门用于Jenkins的CCM插件)",
            "value": {"type": str(ToolOptionType.BOOLEAN), "value": False},
        },
        "exclude": {
            "name": "排除模式",
            "description": "排除匹配这些glob模式的文件路径",
            "value": {
                "type": ToolOptionType.TEXT,
                "value": "tests/*,docs/*,**/migrations/*,**/venv/*",
            },
        },
        "ignore": {
            "name": "忽略目录",
            "description": "忽略匹配这些glob模式的目录",
            "value": {
                "type": ToolOptionType.TEXT,
                "value": "tests,docs",
            },
        },
        "include_ipynb": {
            "name": "包含Jupyter笔记本",
            "description": "在分析中包含IPython Notebook中的Python代码",
            "value": {"type": str(ToolOptionType.BOOLEAN), "value": False},
        },
        "ipynb_cells": {
            "name": "分析Notebook单元格",
            "description": "单独报告.ipynb文件中的各个单元格",
            "value": {"type": str(ToolOptionType.BOOLEAN), "value": False},
        },
        "output_file": {
            "name": "输出文件",
            "description": "将输出保存到指定文件",
            "value": {
                "type": ToolOptionType.TEXT,
                "value": "",
            },
        },
    },
}
