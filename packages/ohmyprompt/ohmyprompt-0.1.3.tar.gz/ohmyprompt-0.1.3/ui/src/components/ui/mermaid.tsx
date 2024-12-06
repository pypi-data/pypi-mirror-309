"use client"

import * as React from "react"
import mermaid from "mermaid"
import { cn } from "@/lib/utils"

interface MermaidProps extends React.HTMLAttributes<HTMLDivElement> {
  content: string
}

// 全局初始化 mermaid
mermaid.initialize({
  startOnLoad: true,
  theme: "default",
  securityLevel: 'loose',
  flowchart: {
    useMaxWidth: true,
    htmlLabels: true,
    curve: 'basis',
    defaultRenderer: 'dagre',
    width: '100%',
    height: '100%'
  },
  graph: {
    useMaxWidth: true,
    width: '100%',
    height: '100%'
  },
  classDiagram: {
    useMaxWidth: true,
    diagramPadding: 8,
    htmlLabels: true,
    curve: 'basis'
  }
})

const Mermaid = React.forwardRef<HTMLDivElement, MermaidProps>(
  ({ content, className, ...props }, ref) => {
    const [svg, setSvg] = React.useState<string>("")
    const elementId = React.useId().replace(/:/g, "-")

    React.useEffect(() => {
      const renderDiagram = async () => {
        try {
          let processedContent = content.trim()
          
          // 处理包依赖图
          if (processedContent.includes('graph TD')) {
            // 确保只有一个 graph TD 声明
            const lines = processedContent.split('\n')
            const graphContent = lines
              .filter(line => 
                !line.includes('classDiagram') && 
                !line.includes('class') &&
                !line.trim().startsWith('{') &&
                !line.trim().startsWith('}') &&
                line.trim()
              )
              .filter(line => 
                line.includes('-->') || 
                line.includes('["') ||  // 保留节点定义
                line.trim() === 'graph TD'  // 只保留第一个 graph TD
              )
            
            // 确保只有一个 graph TD 开头
            processedContent = 'graph TD\n' + graphContent
              .filter(line => !line.trim().startsWith('graph TD'))
              .join('\n')
          } 
          // 处理类图
          else if (processedContent.includes('classDiagram')) {
            processedContent = processedContent
              .replace(/classDiagram\s+classDiagram/, 'classDiagram')
          }

          // 渲染图表
          const uniqueId = `mermaid-${elementId}-${Date.now()}`
          const { svg } = await mermaid.render(uniqueId, processedContent)
          
          // 处理 SVG 尺寸
          const processedSvg = svg
            .replace(/width="[^"]*"/, 'width="100%"')
            .replace(/height="[^"]*"/, 'height="100%"')
            .replace(/style="[^"]*"/, 'style="max-width: 100%; min-width: 300px;"')
          
          setSvg(processedSvg)
        } catch (error) {
          console.error("Mermaid 渲染错误:", error)
          console.error("失败的内容:", content)
        }
      }

      renderDiagram()
    }, [content, elementId])

    if (!svg) {
      return (
        <div
          ref={ref}
          className={cn("mermaid overflow-x-auto my-4 p-4 border border-red-500 rounded min-h-[200px]", className)}
        >
          <pre className="text-sm whitespace-pre-wrap">{content}</pre>
        </div>
      )
    }

    return (
      <div
        ref={ref}
        className={cn("mermaid overflow-x-auto my-4 min-h-[200px]", className)}
        dangerouslySetInnerHTML={{ __html: svg }}
        {...props}
      />
    )
  }
)
Mermaid.displayName = "Mermaid"

export { Mermaid } 