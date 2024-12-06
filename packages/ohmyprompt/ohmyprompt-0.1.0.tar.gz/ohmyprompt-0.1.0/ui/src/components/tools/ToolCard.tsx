import { Button } from "@/components/ui/button"
import { Switch } from "@/components/ui/switch"
import { Settings, Info } from "lucide-react"
import { Card } from "@/components/ui/card"
import type { Tool } from "@/types"

interface ToolCardProps {
  id: string
  tool: Tool
  onConfigClick: (id: string) => void
  onWhichClick: (id: string) => void
  onToggle: (id: string, enabled: boolean) => void
}

export function ToolCard({
  id,
  tool,
  onConfigClick,
  onWhichClick,
  onToggle,
}: ToolCardProps) {
  return (
    <Card className="p-6 transition-colors hover:border-primary/20">
      <div className="flex items-start justify-between">
        <div className="space-y-1">
          <h3 className="text-lg font-semibold">{tool.name}</h3>
          <p className="text-sm text-muted-foreground">{tool.description}</p>
        </div>
        <div className="flex items-center gap-2">
          <Button
            variant="ghost"
            size="icon"
            onClick={() => onWhichClick(id)}
          >
            <Info className="h-4 w-4" />
            <span className="sr-only">查看命令</span>
          </Button>
          <Button
            variant="ghost"
            size="icon"
            onClick={() => onConfigClick(id)}
          >
            <Settings className="h-4 w-4" />
            <span className="sr-only">配置</span>
          </Button>
          <Switch
            checked={tool.enabled}
            onCheckedChange={(checked: boolean) => onToggle(id, checked)}
          />
        </div>
      </div>
    </Card>
  )
} 