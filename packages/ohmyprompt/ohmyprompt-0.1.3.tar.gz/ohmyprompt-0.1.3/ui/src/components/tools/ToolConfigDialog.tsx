import { useState, useEffect } from "react"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Switch } from "@/components/ui/switch"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Input } from "@/components/ui/input"
import type { Tool, ToolOption, ToolOptionValue } from "@/types"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"

interface ToolConfigDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  tool: Tool | null
  onSave: (options: Record<string, ToolOption>) => void
}

export function ToolConfigDialog({ open, onOpenChange, tool, onSave }: ToolConfigDialogProps) {
  if (!tool) return null

  const [options, setOptions] = useState<Record<string, ToolOption>>(tool.options)

  useEffect(() => {
    if (tool) {
      setOptions(tool.options)
    }
  }, [tool])

  const handleSave = async () => {
    try {
      // 直接更新整个配置
      await fetch('/api/config', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          tools: {
            [tool.id]: {
              ...tool,
              options
            }
          }
        })
      })
      
      onSave(options)
      onOpenChange(false)
    } catch (error) {
      console.error('保存配置失败:', error)
    }
  }

  const updateOption = (id: string, value: any) => {
    setOptions(prev => ({
      ...prev,
      [id]: {
        ...prev[id],
        value: {
          ...prev[id].value,
          value: value
        }
      }
    }))
  }

  // 渲染不同类型的配置项
  const renderOptionInput = (id: string, option: ToolOption) => {
    const { type, value: optionValue } = option.value as ToolOptionValue

    switch (type) {
      case 'boolean':
        return (
          <Switch
            checked={optionValue as boolean}
            onCheckedChange={(checked) => updateOption(id, checked)}
          />
        )

      case 'select':
        const selectValue = option.value as ToolOptionValue
        return (
          <Select
            value={String(selectValue.value)}
            onValueChange={(value) => updateOption(id, value)}
          >
            <SelectTrigger className="w-[180px]">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              {selectValue.choices?.map((choice) => (
                <SelectItem 
                  key={choice}
                  value={choice}
                >
                  <div className="flex items-center justify-between w-full">
                    <span>{choice}</span>
                    {(option.value as any).choices_desc?.[choice] && (
                      <span className="ml-2 text-xs text-muted-foreground">
                        {(option.value as any).choices_desc?.[choice]}
                      </span>
                    )}
                  </div>
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        )

      case 'number':
        return (
          <Input
            type="number"
            value={optionValue as number}
            onChange={(e) => updateOption(id, Number(e.target.value))}
            min={option.value.min}
            max={option.value.max}
            step={option.value.step}
            className="w-[100px]"
          />
        )

      case 'text':
        return (
          <Input
            type="text"
            value={optionValue as string}
            onChange={(e) => updateOption(id, e.target.value)}
            className="w-full"
          />
        )

      case 'multi_select':
        const multiSelectValue = option.value as ToolOptionValue
        return (
          <div className="flex flex-wrap gap-2 justify-end">
            {multiSelectValue.choices?.map((choice) => (
              <TooltipProvider key={choice}>
                <Tooltip>
                  <TooltipTrigger asChild>
                    <Button
                      variant={(multiSelectValue.value as string[]).includes(choice) ? "default" : "outline"}
                      size="sm"
                      onClick={() => {
                        const currentValues = multiSelectValue.value as string[]
                        const newValues = currentValues.includes(choice)
                          ? currentValues.filter(v => v !== choice)
                          : [...currentValues, choice]
                        updateOption(id, newValues)
                      }}
                    >
                      {choice}
                    </Button>
                  </TooltipTrigger>
                  {(option.value as any).choices_desc?.[choice] && (
                    <TooltipContent side="bottom" className="tooltip-content">
                      <p>{(option.value as any).choices_desc?.[choice]}</p>
                    </TooltipContent>
                  )}
                </Tooltip>
              </TooltipProvider>
            ))}
          </div>
        )

      default:
        return <div>不支持的配置类型: {type}</div>
    }
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[700px] max-h-[85vh] flex flex-col">
        <DialogHeader>
          <DialogTitle>{tool.name} 配置</DialogTitle>
        </DialogHeader>
        <div className="flex-1 overflow-y-auto">
          <div className="grid gap-6 py-4">
            {Object.entries(options).map(([id, option]) => (
              <div key={id}>
                {option.value.type === 'multi_select' ? (
                  <div className="space-y-2">
                    <div className="space-y-1.5">
                      <div>
                        <h4 className="text-sm font-medium flex items-center gap-2">
                          {option.name}
                          <span className="text-xs text-muted-foreground">
                            ({id})
                          </span>
                        </h4>
                      </div>
                      <p className="text-sm text-muted-foreground">
                        {option.description}
                      </p>
                    </div>
                    {renderOptionInput(id, option)}
                  </div>
                ) : (
                  <div className="grid grid-cols-[1fr,auto] gap-4 items-start">
                    <div className="space-y-1.5">
                      <div>
                        <h4 className="text-sm font-medium flex items-center gap-2">
                          {option.name}
                          <span className="text-xs text-muted-foreground">
                            ({id})
                          </span>
                        </h4>
                      </div>
                      <p className="text-sm text-muted-foreground">
                        {option.description}
                      </p>
                    </div>
                    <div className="flex-shrink-0">
                      {renderOptionInput(id, option)}
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
        <DialogFooter className="flex-shrink-0">
          <Button variant="outline" onClick={() => onOpenChange(false)}>
            取消
          </Button>
          <Button onClick={handleSave}>保存</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
} 