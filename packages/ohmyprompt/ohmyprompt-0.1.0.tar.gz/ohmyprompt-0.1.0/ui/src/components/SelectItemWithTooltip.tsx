import { SelectItem } from "@/components/ui/select"
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip"

interface SelectItemWithTooltipProps extends React.ComponentProps<typeof SelectItem> {
  tooltip?: string
}

export function SelectItemWithTooltip({ tooltip, children, ...props }: SelectItemWithTooltipProps) {
  if (!tooltip) {
    return <SelectItem {...props}>{children}</SelectItem>
  }

  return (
    <TooltipProvider>
      <Tooltip>
        <div className="relative w-full">
          <TooltipTrigger className="w-full">
            <SelectItem {...props}>{children}</SelectItem>
          </TooltipTrigger>
          <TooltipContent side="right" align="center">
            <p className="text-sm">{tooltip}</p>
          </TooltipContent>
        </div>
      </Tooltip>
    </TooltipProvider>
  )
} 