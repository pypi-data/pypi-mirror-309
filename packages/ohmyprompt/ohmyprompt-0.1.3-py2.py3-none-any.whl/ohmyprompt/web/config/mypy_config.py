from ...utils.config_utils import get_platform, get_python_version
from ..config_types import ToolConfig, ToolOptionType

# 获取Python版本和平台
python_version = get_python_version()
current_platform = get_platform()

MYPY_CONFIG: ToolConfig = {
    "name": "Mypy",
    "description": "Python 静态类型检查器",
    "enabled": True,
    "command": "mypy",
    "options": {
        "paths": {
            "name": "检查路径",
            "description": "要检查的文件或目录路径，多个路径用空格分隔",
            "value": {
                "type": ToolOptionType.TEXT,
                "value": "src/",
            },
        },
        "show-error-codes": {
            "name": "显示错误代码",
            "description": "在错误消息中显示错误代码",
            "value": {"type": str(ToolOptionType.BOOLEAN), "value": True},
        },
        "pretty": {
            "name": "美化输出",
            "description": "使用彩色和格式化的输出",
            "value": {"type": str(ToolOptionType.BOOLEAN), "value": True},
        },
        "python-version": {
            "name": "Python 版本",
            "description": "指定 Python 版本",
            "value": {
                "type": ToolOptionType.SELECT,
                "value": python_version,
                "choices": ["3.7", "3.8", "3.9", "3.10", "3.11", "3.12"],
                "choices_desc": {
                    "3.7": "使用 Python 3.7 的类型检查规则",
                    "3.8": "使用 Python 3.8 的类型检查规则",
                    "3.9": "使用 Python 3.9 的类型检查规则",
                    "3.10": "使用 Python 3.10 的类型检查规则",
                    "3.11": "使用 Python 3.11 的类型检查规则",
                    "3.12": "使用 Python 3.12 的类型检查规则",
                },
            },
        },
        "ignore-missing-imports": {
            "name": "忽略缺失导入",
            "description": "忽略未找到的导入模块",
            "value": {"type": str(ToolOptionType.BOOLEAN), "value": True},
        },
        "check-untyped-defs": {
            "name": "检查未标注类型的函数",
            "description": "检查没有类型注解的函数",
            "value": {"type": str(ToolOptionType.BOOLEAN), "value": True},
        },
        "warn-unused-configs": {
            "name": "警告未使用的配置",
            "description": "显示未使用的配置项警告",
            "value": {"type": str(ToolOptionType.BOOLEAN), "value": True},
        },
        "strict": {
            "name": "严格模式",
            "description": "启用所有严格的类型检查选项",
            "value": {"type": str(ToolOptionType.BOOLEAN), "value": False},
        },
        "disallow-any-generics": {
            "name": "禁止泛型使用 Any",
            "description": "禁止在泛型类型中使用 Any",
            "value": {"type": str(ToolOptionType.BOOLEAN), "value": False},
        },
        "disallow-subclassing-any": {
            "name": "禁止继承 Any",
            "description": "禁止继承 Any 类型",
            "value": {"type": str(ToolOptionType.BOOLEAN), "value": False},
        },
        "disallow-untyped-decorators": {
            "name": "禁止无类型装饰器",
            "description": "禁止使用未标注类型的装饰器",
            "value": {"type": str(ToolOptionType.BOOLEAN), "value": False},
        },
        "disallow-untyped-calls": {
            "name": "禁止调用无类型函数",
            "description": "禁止调用未标注类型的函数",
            "value": {"type": str(ToolOptionType.BOOLEAN), "value": False},
        },
        "follow-imports": {
            "name": "导入跟踪模式",
            "description": "设置如何处理导入模块",
            "value": {
                "type": ToolOptionType.SELECT,
                "value": "normal",
                "choices": ["normal", "silent", "skip", "error"],
                "choices_desc": {
                    "normal": "正常跟踪和检查导入",
                    "silent": "跟踪导入但不报告错误",
                    "skip": "不跟踪导入",
                    "error": "将导入标记为错误",
                },
            },
        },
        "no-namespace-packages": {
            "name": "禁用命名空间包",
            "description": "禁用 PEP 420 命名空间包支持",
            "value": {"type": str(ToolOptionType.BOOLEAN), "value": False},
        },
        "show-column-numbers": {
            "name": "显示列号",
            "description": "在错误消息中显示列号",
            "value": {"type": str(ToolOptionType.BOOLEAN), "value": True},
        },
        "show-error-context": {
            "name": "显示错误上下文",
            "description": "显示导致错误的代码上下文",
            "value": {"type": str(ToolOptionType.BOOLEAN), "value": True},
        },
        "show-traceback": {
            "name": "显示回溯",
            "description": "显示错误的完整回溯信息",
            "value": {"type": str(ToolOptionType.BOOLEAN), "value": False},
        },
        "incremental": {
            "name": "增量检查",
            "description": "启用增量类型检查",
            "value": {"type": str(ToolOptionType.BOOLEAN), "value": True},
        },
        "cache-dir": {
            "name": "缓存目录",
            "description": "设置增量检查缓存目录",
            "value": {
                "type": ToolOptionType.TEXT,
                "value": ".mypy_cache",
            },
        },
        "strict-optional": {
            "name": "严格可选类型",
            "description": "启用严格的可选类型检查",
            "value": {"type": str(ToolOptionType.BOOLEAN), "value": True},
        },
        "warn-redundant-casts": {
            "name": "警告冗余转换",
            "description": "警告不必要的类型转换",
            "value": {"type": str(ToolOptionType.BOOLEAN), "value": True},
        },
        "warn-unused-ignores": {
            "name": "警告未使用的忽略",
            "description": "警告未使用的 # type: ignore 注释",
            "value": {"type": str(ToolOptionType.BOOLEAN), "value": True},
        },
        "allow-redefinition": {
            "name": "允许重定义",
            "description": "允许在同一个块中重定义变量",
            "value": {"type": str(ToolOptionType.BOOLEAN), "value": False},
        },
        "implicit-reexport": {
            "name": "隐式重导出",
            "description": "允许在 __init__.py 隐式重导出",
            "value": {"type": str(ToolOptionType.BOOLEAN), "value": True},
        },
        "strict-equality": {
            "name": "严格相等性",
            "description": "对不兼容类型使用 == 和 != 时发出警告",
            "value": {"type": str(ToolOptionType.BOOLEAN), "value": True},
        },
        "html-report": {
            "name": "HTML报告目录",
            "description": "生成HTML格式的类检查报告",
            "value": {
                "type": ToolOptionType.TEXT,
                "value": "",
            },
        },
        "txt-report": {
            "name": "文本报告目录",
            "description": "生成文本格式的类型检查报告",
            "value": {
                "type": ToolOptionType.TEXT,
                "value": "",
            },
        },
        "junit-xml": {
            "name": "JUnit XML报告",
            "description": "生成JUnit XML格式的测试报告",
            "value": {
                "type": ToolOptionType.TEXT,
                "value": "",
            },
        },
        "platform": {
            "name": "目标平台",
            "description": "设置目标平台(操作系统)",
            "value": {
                "type": ToolOptionType.SELECT,
                "value": current_platform,
                "choices": ["linux", "darwin", "win32"],
                "choices_desc": {
                    "linux": "Linux 平台",
                    "darwin": "macOS 平台",
                    "win32": "Windows 平台",
                },
            },
        },
    },
}
