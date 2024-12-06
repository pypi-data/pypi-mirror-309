import { useState } from "react"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Card, CardHeader, CardContent } from "@/components/ui/card"
import { X } from "lucide-react"
import { toast } from "sonner"

interface ExcludePatternsProps {
  patterns: {
    directories: string[]
    files: string[]
  }
  onUpdate: (patterns: { directories: string[], files: string[] }) => void
}

export function ExcludePatterns({ patterns, onUpdate }: ExcludePatternsProps) {
  const [directoryInput, setDirectoryInput] = useState("")
  const [fileInput, setFileInput] = useState("")

  const handleAddPattern = async (type: "directories" | "files", pattern: string) => {
    if (!pattern.trim()) return

    try {
      const newPatterns = {
        ...patterns,
        [type]: [...patterns[type], pattern.trim()]
      }
      
      await fetch('/api/config', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ exclude_patterns: newPatterns })
      })

      onUpdate(newPatterns)
      toast.success("添加成功")
      
      if (type === "directories") {
        setDirectoryInput("")
      } else {
        setFileInput("")
      }
    } catch (error) {
      console.error('添加排除模式失败:', error)
      toast.error("添加失败")
    }
  }

  const handleRemovePattern = async (type: "directories" | "files", pattern: string) => {
    try {
      const newPatterns = {
        ...patterns,
        [type]: patterns[type].filter(p => p !== pattern)
      }
      
      await fetch('/api/config', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ exclude_patterns: newPatterns })
      })

      onUpdate(newPatterns)
      toast.success("删除成功")
    } catch (error) {
      console.error('删除排除模式失败:', error)
      toast.error("删除失败")
    }
  }

  return (
    <Card>
      <CardHeader>
        <h3 className="text-lg font-semibold">排除模式</h3>
        <p className="text-sm text-muted-foreground">
          设置需要排除的目录和文件模式
        </p>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-2 gap-6">
          {/* 目录排除模式 */}
          <div>
            <h4 className="text-sm font-medium mb-2">目录</h4>
            <form
              className="flex gap-2 mb-4"
              onSubmit={(e) => {
                e.preventDefault()
                handleAddPattern("directories", directoryInput)
              }}
            >
              <Input
                value={directoryInput}
                onChange={(e) => setDirectoryInput(e.target.value)}
                placeholder="输入目录名，例如：node_modules"
              />
              <Button type="submit">添加</Button>
            </form>
            <div className="space-y-2">
              {patterns.directories.map((pattern) => (
                <div
                  key={pattern}
                  className="flex items-center justify-between py-1 px-3 bg-muted/50 rounded-md"
                >
                  <span className="text-sm">{pattern}</span>
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => handleRemovePattern("directories", pattern)}
                  >
                    <X className="h-4 w-4" />
                  </Button>
                </div>
              ))}
            </div>
          </div>

          {/* 文件排除模式 */}
          <div>
            <h4 className="text-sm font-medium mb-2">文件</h4>
            <form
              className="flex gap-2 mb-4"
              onSubmit={(e) => {
                e.preventDefault()
                handleAddPattern("files", fileInput)
              }}
            >
              <Input
                value={fileInput}
                onChange={(e) => setFileInput(e.target.value)}
                placeholder="输入文件模式，例如：*.pyc"
              />
              <Button type="submit">添加</Button>
            </form>
            <div className="space-y-2">
              {patterns.files.map((pattern) => (
                <div
                  key={pattern}
                  className="flex items-center justify-between py-1 px-3 bg-muted/50 rounded-md"
                >
                  <span className="text-sm">{pattern}</span>
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => handleRemovePattern("files", pattern)}
                  >
                    <X className="h-4 w-4" />
                  </Button>
                </div>
              ))}
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
} 