import { Settings, History, PanelLeft } from "lucide-react"
import { Link, useLocation } from "react-router-dom"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"

export function RootLayout({ children }: { children: React.ReactNode }) {
  const location = useLocation()

  return (
    <div className="flex min-h-screen">
      {/* 侧边栏 */}
      <aside className="w-64 border-r border-border bg-card">
        <div className="flex h-full flex-col">
          <div className="p-6">
            <h1 className="text-lg font-semibold">OhMyPrompt</h1>
            <p className="text-sm text-muted-foreground">项目分析与监控工具</p>
          </div>
          <nav className="flex-1 space-y-1 p-4">
            <Link
              to="/"
              className={cn(
                "flex items-center gap-2 rounded-md px-3 py-2 text-sm transition-colors",
                location.pathname === "/" 
                  ? "bg-accent text-accent-foreground" 
                  : "hover:bg-accent hover:text-accent-foreground"
              )}
            >
              <Settings className="h-4 w-4" />
              <span>设置</span>
            </Link>
            <Link
              to="/history"
              className={cn(
                "flex items-center gap-2 rounded-md px-3 py-2 text-sm transition-colors",
                location.pathname === "/history" 
                  ? "bg-accent text-accent-foreground" 
                  : "hover:bg-accent hover:text-accent-foreground"
              )}
            >
              <History className="h-4 w-4" />
              <span>历史记录</span>
            </Link>
          </nav>
        </div>
      </aside>

      {/* 主内容区 */}
      <main className="flex-1 min-w-0 overflow-auto bg-background">
        <div className="h-full p-8">
          <div className="mx-auto max-w-7xl space-y-8">
            <Button
              variant="ghost"
              size="icon"
              className="h-7 w-7"
            >
              <PanelLeft className="h-4 w-4" />
              <span className="sr-only">Toggle Sidebar</span>
            </Button>
            {children}
          </div>
        </div>
      </main>
    </div>
  )
} 