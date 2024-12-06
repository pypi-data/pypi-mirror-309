import React, { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from "@/components/ui/dialog"
import { Badge } from "@/components/ui/badge"
import { Card, CardContent } from "@/components/ui/card"
import { Trash2} from "lucide-react"
import Markdown from 'marked-react'
import { highlightCode} from '@/lib/markdown'
import { cn } from "@/lib/utils"
import { Mermaid } from "@/components/ui/mermaid"

interface TocItem {
  level: number
  text: string
  id: string
}

interface TocTree {
  level: number
  text: string
  id: string
  children: TocTree[]
}

interface HistoryItemProps {
  item: {
    id: string
    timestamp: string
    data: {
      content: string
      linter: { status: string }
      tests: { status: string }
    }
  }
  onDelete: () => void
}

const TocTreeItem = ({ 
  item, 
  activeId, 
  onSelect 
}: { 
  item: TocTree
  activeId: string
  onSelect: (id: string) => void
}) => {
  return (
    <div className="flex flex-col">
      <a
        href={`#${item.id}`}
        onClick={(e) => {
          e.preventDefault()
          onSelect(item.id)
        }}
        className={cn(
          "flex items-center text-left py-1 text-sm transition-colors hover:text-primary",
          "space-x-1",
          activeId === item.id ? "text-primary font-medium" : "text-muted-foreground"
        )}
      >
        {item.children.length > 0 && (
          <svg
            className="h-4 w-4 shrink-0"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9 5l7 7-7 7"
            />
          </svg>
        )}
        <span className="truncate">{item.text}</span>
      </a>
      {item.children.length > 0 && (
        <div className="ml-4 pl-2 border-l border-border">
          {item.children.map((child, index) => (
            <TocTreeItem
              key={index}
              item={child}
              activeId={activeId}
              onSelect={onSelect}
            />
          ))}
        </div>
      )}
    </div>
  )
}

// 添加 RendererProps 接口定义
interface RendererProps {
  children: React.ReactNode[]
  ordered?: boolean
  level?: number
}

export function HistoryItem({ item, onDelete }: HistoryItemProps) {
  const [dialogOpen, setDialogOpen] = useState(false)
  const [toc, setToc] = useState<TocItem[]>([])
  const [activeId, setActiveId] = useState<string>("")
  const [headingIds] = useState(() => new Map<string, string>())

  const formatDate = (timestamp: string) => {
    return new Date(timestamp).toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit', 
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    })
  }

  const getTitle = (content: string) => {
    const lines = content.split('\n')
    const titleLine = lines.find(line => line.startsWith('# '))
    return titleLine ? titleLine.replace(/^#\s+/, '').trim() : '未命名报告'
  }

  const generateRandomId = () => `heading-${Math.random().toString(36).slice(2, 9)}`

  const generateToc = (content: string) => {
    const headings: TocItem[] = []
    const lines = content.split('\n')
    
    headingIds.clear()
    
    lines.forEach(line => {
      const match = line.match(/^(#{1,6})\s+(.+)$/)
      if (match) {
        const level = match[1].length
        const text = match[2].trim()
        const id = generateRandomId()
        headingIds.set(text, id)
        headings.push({ level, text, id })
      }
    })
    
    return headings
  }

  const generateTocTree = (headings: TocItem[]): TocTree[] => {
    const root: TocTree[] = []
    const stack: TocTree[] = []

    headings.forEach((heading) => {
      const node: TocTree = {
        ...heading,
        children: []
      }

      while (
        stack.length > 0 && 
        stack[stack.length - 1].level >= heading.level
      ) {
        stack.pop()
      }

      if (stack.length === 0) {
        root.push(node)
      } else {
        stack[stack.length - 1].children.push(node)
      }

      stack.push(node)
    })

    return root
  }

  useEffect(() => {
    if (!dialogOpen) return

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setActiveId(entry.target.id)
          }
        })
      },
      {
        root: document.querySelector('.content-container'),
        rootMargin: '-20% 0% -35% 0%',
        threshold: [0, 1]
      }
    )

    const headings = document.querySelectorAll('.content-container article h1, .content-container article h2, .content-container article h3')
    headings.forEach((heading) => observer.observe(heading))

    return () => {
      headings.forEach((heading) => observer.unobserve(heading))
    }
  }, [dialogOpen])

  useEffect(() => {
    if (dialogOpen) {
      const headings = generateToc(item.data.content)
      setToc(headings)
    }
  }, [dialogOpen, item.data.content])

  const scrollToHeading = (id: string) => {
    if (!id) return

    requestAnimationFrame(() => {
      const element = document.getElementById(id)
      if (!element) {
        console.warn('Target element not found:', id)
        return
      }

      const container = document.querySelector('.content-container')
      if (!container) return

      const elementPosition = element.offsetTop
      const offset = 20

      container.scrollTo({
        top: elementPosition - offset,
        behavior: 'smooth'
      })
    })
  }

  return (
    <>
      <Card 
        className="group cursor-pointer transition-all hover:shadow-md dark:hover:shadow-accent/10 h-full flex flex-col"
        onClick={() => setDialogOpen(true)}
      >
        <CardContent className="p-6 flex flex-col flex-1">
          <div className="flex flex-col space-y-3 h-full">
            <div className="flex items-center justify-between">
              <time className="text-sm text-muted-foreground" dateTime={item.timestamp}>
                {formatDate(item.timestamp)}
              </time>
              <Button
                variant="ghost"
                size="icon"
                className="opacity-0 group-hover:opacity-100 transition-opacity"
                onClick={(e) => {
                  e.stopPropagation()
                  if (confirm('确定要删除这条历史记录吗？')) {
                    onDelete()
                  }
                }}
              >
                <Trash2 className="h-4 w-4" />
                <span className="sr-only">删除</span>
              </Button>
            </div>
            <h3 className="font-semibold leading-none tracking-tight">
              {getTitle(item.data.content)}
            </h3>
            <div className="flex flex-wrap gap-2">
              <Badge 
                variant={item.data.linter.status === 'ok' ? 'success' : 'destructive'}
                className="rounded-md"
              >
                代码检查: {item.data.linter.status === 'ok' ? '通过' : '失败'}
              </Badge>
              <Badge 
                variant={item.data.tests.status === 'ok' ? 'success' : 'destructive'}
                className="rounded-md"
              >
                测试: {item.data.tests.status === 'ok' ? '通过' : '失败'}
              </Badge>
            </div>
          </div>
        </CardContent>
      </Card>

      <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
        <DialogContent className="max-w-5xl h-[85vh] flex flex-col p-0">
          <DialogHeader className="border-b px-6 py-4">
            <DialogTitle>
              {getTitle(item.data.content)}
            </DialogTitle>
            <DialogDescription>
              {`${getTitle(item.data.content)} 的详细分析报告`}
            </DialogDescription>
          </DialogHeader>
          <div className="flex-1 flex overflow-hidden">
            <nav className="w-64 border-r p-4 overflow-y-auto flex flex-col">
              <div className="space-y-6">
                <div>
                  <div className="font-medium mb-2">目录</div>
                  <div className="space-y-1">
                    {generateTocTree(toc).map((item, index) => (
                      <TocTreeItem
                        key={index}
                        item={item}
                        activeId={activeId}
                        onSelect={scrollToHeading}
                      />
                    ))}
                  </div>
                </div>
              </div>
            </nav>
            <div 
              className="flex-1 overflow-y-auto content-container scroll-smooth"
              style={{ scrollBehavior: 'smooth' }}
            >
              <div className="px-6 py-4">
                <article className="prose prose-sm md:prose-base dark:prose-invert max-w-none">
                  <div className="markdown-body">
                    <Markdown
                      value={item.data.content}
                      renderer={{
                        heading(text: string | React.ReactNode, level: number) {
                          const textStr = typeof text === 'string' ? text : String(text)
                          const id = headingIds.get(textStr) || generateRandomId()
                          
                          return React.createElement(`h${level}`, {
                            id,
                            children: text,
                            className: 'scroll-mt-6'
                          })
                        },
                        code(snippet, language) {
                          if (language === 'mermaid') {
                            return <Mermaid content={snippet} />
                          }
                          return (
                            <pre>
                              <code
                                className={language ? `hljs language-${language}` : ''}
                                dangerouslySetInnerHTML={{
                                  __html: highlightCode(snippet, language)
                                }}
                              />
                            </pre>
                          )
                        }
                      }}
                    />
                  </div>
                </article>
              </div>
            </div>
          </div>
        </DialogContent>
      </Dialog>
    </>
  )
} 