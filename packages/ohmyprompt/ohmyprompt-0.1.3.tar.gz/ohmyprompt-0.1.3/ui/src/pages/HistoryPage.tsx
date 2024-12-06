import { useState, useEffect } from "react"
import { HistoryItem } from "@/components/history/HistoryItem"
import { Skeleton } from "@/components/ui/skeleton"

interface HistoryData {
  id: string
  timestamp: string
  data: {
    content: string
    linter: { status: string }
    tests: { status: string }
  }
}

export function HistoryPage() {
  const [history, setHistory] = useState<HistoryData[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchHistory()
  }, [])

  const fetchHistory = async () => {
    try {
      const response = await fetch('/api/history')
      const data = await response.json()
      setHistory(data)
      setLoading(false)
    } catch (error) {
      console.error('获取历史记录失败:', error)
      setLoading(false)
    }
  }

  const handleDelete = async (id: string) => {
    try {
      await fetch(`/api/history/${id}`, {
        method: 'DELETE'
      })
      setHistory(prev => prev.filter(item => item.id !== id))
    } catch (error) {
      console.error('删除历史记录失败:', error)
    }
  }

  if (loading) {
    return (
      <div className="grid grid-cols-3 gap-4 p-4">
        {[...Array(6)].map((_, i) => (
          <Skeleton key={i} className="h-[200px] rounded-xl" />
        ))}
      </div>
    )
  }

  if (history.length === 0) {
    return (
      <div className="flex h-[450px] items-center justify-center">
        <p className="text-lg text-muted-foreground">暂无历史记录</p>
      </div>
    )
  }

  return (
    <div className="grid grid-cols-3 gap-4 p-4">
      {history.map((item) => (
        <HistoryItem
          key={item.id}
          item={item}
          onDelete={() => handleDelete(item.id)}
        />
      ))}
    </div>
  )
} 