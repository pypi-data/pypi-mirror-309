import { Input } from "@/components/ui/input"
import { Card, CardHeader, CardContent } from "@/components/ui/card"

interface IntervalConfigProps {
  interval: number
  onUpdate: (interval: number) => void
}

export function IntervalConfig({ interval, onUpdate }: IntervalConfigProps) {
  return (
    <Card>
      <CardHeader>
        <h3 className="text-lg font-semibold">更新间隔</h3>
        <p className="text-sm text-muted-foreground">
          设置自动更新的时间间隔
        </p>
      </CardHeader>
      <CardContent>
        <div className="flex items-end gap-4">
          <div className="flex-1">
            <Input
              type="number"
              value={interval}
              onChange={(e) => onUpdate(Number(e.target.value))}
            />
          </div>
        </div>
      </CardContent>
    </Card>
  )
} 