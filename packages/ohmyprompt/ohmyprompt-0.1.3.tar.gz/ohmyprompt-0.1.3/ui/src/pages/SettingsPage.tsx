import { useState, useEffect } from "react"
import { ExcludePatterns } from "@/components/settings/ExcludePatterns"
import { IntervalConfig } from "@/components/settings/IntervalConfig"
import { ToolCard } from "@/components/tools/ToolCard"
import { ToolConfigDialog } from "@/components/tools/ToolConfigDialog"
import { ToolCommandDialog } from "@/components/tools/ToolCommandDialog"
import { toast } from "sonner"
import type { Tool, ToolOption, Config } from "@/types"
import { Card, CardHeader, CardContent } from "@/components/ui/card"

export function SettingsPage() {
  const [config, setConfig] = useState<Config>({
    exclude_patterns: {
      directories: [],
      files: []
    },
    update_interval: 0,
    tools: {}
  })
  const [selectedTool, setSelectedTool] = useState<string | null>(null)
  const [configDialogOpen, setConfigDialogOpen] = useState(false)
  const [commandDialogOpen, setCommandDialogOpen] = useState(false)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    fetchConfig()
  }, [])

  const fetchConfig = async () => {
    try {
      setIsLoading(true)
      const response = await fetch('/api/config')
      if (!response.ok) {
        throw new Error('获取配置失败')
      }
      const data = await response.json()
      setConfig({
        ...data,
        tools: data.tools || {}
      })
    } catch (error) {
      console.error('获取配置失败:', error)
      toast.error("获取配置失败")
    } finally {
      setIsLoading(false)
    }
  }

  const updateConfig = async (partialConfig: Partial<Config>) => {
    try {
      const newConfig = { ...config, ...partialConfig }
      await fetch('/api/config', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newConfig)
      })
      setConfig(newConfig)
      return true
    } catch (error) {
      console.error('更新配置失败:', error)
      toast.error("更新配置失败")
      return false
    }
  }

  const handleIntervalUpdate = async (interval: number) => {
    const success = await updateConfig({ update_interval: interval })
    if (success) {
      toast.success("更新间隔已保存")
    }
  }

  const handleToolToggle = async (id: string, enabled: boolean) => {
    const updatedTools = {
      ...config.tools,
      [id]: {
        ...config.tools[id],
        enabled
      }
    }
    
    const success = await updateConfig({ tools: updatedTools })
    if (success) {
      toast.success(`${config.tools[id].name} ${enabled ? '已启用' : '已禁用'}`)
    }
  }

  const handleToolConfigSave = async (options: Record<string, ToolOption>) => {
    if (!selectedTool) return

    const updatedTools = {
      ...config.tools,
      [selectedTool]: {
        ...config.tools[selectedTool],
        options
      }
    }

    const success = await updateConfig({ tools: updatedTools })
    if (success) {
      toast.success("工具配置已保存")
    }
  }

  if (isLoading) {
    return (
      <div className="container py-6">
        <Card>
          <CardContent className="py-6">
            <div className="flex justify-center">
              <p className="text-muted-foreground">加载中...</p>
            </div>
          </CardContent>
        </Card>
      </div>
    )
  }

  const tools = config.tools || {}
  const hasTools = Object.keys(tools).length > 0

  return (
    <div className="container py-6 space-y-8">
      <Card>
        <CardHeader>
          <h2 className="text-lg font-semibold">工具配置</h2>
          <p className="text-sm text-muted-foreground">
            配置代码分析工具的运行参数和启用状态
          </p>
        </CardHeader>
        <CardContent>
          {hasTools ? (
            <div className="grid gap-4 md:grid-cols-2">
              {Object.entries(tools).map(([id, tool]) => (
                <ToolCard
                  key={id}
                  id={id}
                  tool={tool}
                  onConfigClick={(id) => {
                    setSelectedTool(id)
                    setConfigDialogOpen(true)
                  }}
                  onWhichClick={(id) => {
                    setSelectedTool(id)
                    setCommandDialogOpen(true)
                  }}
                  onToggle={handleToolToggle}
                />
              ))}
            </div>
          ) : (
            <div className="flex justify-center py-6">
              <p className="text-muted-foreground">暂无可用的工具配置</p>
            </div>
          )}
        </CardContent>
      </Card>

      <ExcludePatterns
        patterns={config.exclude_patterns}
        onUpdate={async (patterns) => {
          const success = await updateConfig({ exclude_patterns: patterns })
          if (success) {
            toast.success("排除模式已保存")
          }
        }}
      />

      <IntervalConfig
        interval={config.update_interval}
        onUpdate={handleIntervalUpdate}
      />

      <ToolConfigDialog
        open={configDialogOpen}
        onOpenChange={setConfigDialogOpen}
        tool={selectedTool ? config.tools[selectedTool] : null}
        onSave={handleToolConfigSave}
      />

      <ToolCommandDialog
        open={commandDialogOpen}
        onOpenChange={setCommandDialogOpen}
        name={selectedTool ? config.tools[selectedTool].name : ''}
        command={selectedTool ? config.tools[selectedTool].command : ''}
      />
    </div>
  )
} 