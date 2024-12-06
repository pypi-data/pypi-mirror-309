import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"

interface ToolCommandDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  name: string
  command: string
}

export function ToolCommandDialog({ open, onOpenChange, name, command }: ToolCommandDialogProps) {
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>{name} 命令</DialogTitle>
        </DialogHeader>
        <div className="mt-4">
          <pre className="rounded-lg bg-muted p-4 text-sm font-mono">
            {command}
          </pre>
        </div>
        <DialogFooter>
          <Button onClick={() => onOpenChange(false)}>关闭</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
} 