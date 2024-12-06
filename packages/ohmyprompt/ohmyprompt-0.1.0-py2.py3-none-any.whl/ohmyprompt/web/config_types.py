from enum import Enum
from typing import Any, TypedDict


class ToolOptionType(Enum):
    """工具选项类型"""

    BOOLEAN = "boolean"
    STRING = "string"
    NUMBER = "number"
    SELECT = "select"
    MULTI_SELECT = "multi_select"
    TEXT = "text"

    def __str__(self) -> str:
        return self.value


class BooleanOptionValue(TypedDict):
    type: str
    value: bool


class ChoiceOptionValue(TypedDict):
    type: str
    value: str
    choices: list[str]
    choices_desc: list[str]


class NumberOptionValue(TypedDict):
    type: str
    value: float
    min: float
    max: float
    step: float


class ToolOptionValue(TypedDict, total=False):
    """工具选项值"""

    type: str | ToolOptionType
    value: Any
    choices: list[str] | None
    choices_desc: dict[str, str] | None
    min: int | float | None
    max: int | float | None
    step: int | float | None


class ToolOption(TypedDict):
    """工具选项"""

    name: str
    description: str
    value: ToolOptionValue


class ToolConfig(TypedDict):
    """工具配置"""

    name: str
    description: str
    enabled: bool
    command: str
    options: dict[str, ToolOption]


class Tools(TypedDict):
    """工具配置集合"""
    mypy: ToolConfig
    radon: ToolConfig
    ruff: ToolConfig
