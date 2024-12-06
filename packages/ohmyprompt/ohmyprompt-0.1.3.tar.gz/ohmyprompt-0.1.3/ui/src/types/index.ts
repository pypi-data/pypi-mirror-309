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
  exclude_patterns: {
    directories: string[]
    files: string[]
  }
  update_interval: number
  tools: Record<string, Tool>
} 