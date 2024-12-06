import { useState, useEffect } from "react"
import { HistoryItem } from "@/components/history/HistoryItem"
import { toast } from "sonner"
import { fetchHomeData } from "@/lib/api"
import type { HistoryItem as HistoryItemType } from "@/types"

export function HomePage() {
  const [loading, setLoading] = useState(true)
  const [recentHistory, setRecentHistory] = useState<HistoryItemType[]>([])
  const [totalCount, setTotalCount] = useState(0)

  useEffect(() => {
    loadHomeData()
  }, [])

  const loadHomeData = async () => {
    const result = await fetchHomeData()
    if (result.success && result.data) {
      setRecentHistory(result.data.recent_history)
      setTotalCount(result.data.total_count)
    } else {
      toast.error(result.error || "加载数据失败")
    }
    setLoading(false)
  }

  if (loading) {
    return (
      <div className="text-center py-12">
        <p className="text-muted-foreground">加载中...</p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold tracking-tight">最近分析</h2>
        <p className="text-muted-foreground">
          共有 {totalCount} 条历史记录
        </p>
      </div>

      <div className="grid gap-4">
        {recentHistory.map((item) => (
          <HistoryItem
            key={item.id}
            item={item}
            onDelete={() => loadHomeData()}  // 删除后重新加载数据
          />
        ))}
      </div>
    </div>
  )
} 