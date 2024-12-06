export type ToolOptionType = 
  | "boolean"
  | "string"
  | "number"
  | "select"
  | "multi_select"
  | "text"

export interface ToolOptionValue {
  type: ToolOptionType
  value: string | number | boolean | string[]
  choices?: string[]
  choices_desc?: Record<string, string>
  min?: number
  max?: number
  step?: number
}

export interface ToolOption {
  name: string
  description: string
  value: ToolOptionValue
}

export interface Tool {
  id: string
  name: string
  description: string
  enabled: boolean
  command: string
  options: Record<string, ToolOption>
}

export interface Config {
  tools: Record<string, Tool>;
  exclude_patterns: {
    directories: string[];
    files: string[];
  };
  update_interval: number;
}

export interface HistoryItem {
  id: string;
  timestamp: string;
  data: {
    content: string;
    linter: { status: string };
    tests: { status: string };
  };
}

// 全局状态类型
export interface InitialState {
  config: Config;
  history: HistoryItem[];
}

// 扩展 Window 接口
declare global {
  interface Window {
    __INITIAL_STATE__: InitialState;
  }
} 