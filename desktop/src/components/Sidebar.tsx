import { LayoutTemplate, Settings, Video, Image as ImageIcon } from 'lucide-react'
import { cn } from '@/lib/utils'

interface SidebarProps {
  currentView: string
  onNavigate: (view: string) => void
  onOpenSettings: () => void
}

export default function Sidebar({ currentView, onNavigate, onOpenSettings }: SidebarProps) {
  const navItems = [
    { id: 'generator', label: '草稿生成', icon: Video },
    // Placeholder for future features
    { id: 'templates', label: '模板管理', icon: LayoutTemplate },
  ]

  return (
    <aside className="w-64 bg-slate-900 text-white flex flex-col h-full border-r border-slate-800">
      <div className="p-6 border-b border-slate-800">
        <h1 className="text-xl font-bold flex items-center gap-2">
          <ImageIcon className="w-6 h-6 text-blue-500" />
          <span>AutoCut</span>
        </h1>
      </div>

      <nav className="flex-1 p-4 space-y-2">
        {navItems.map((item) => (
          <button
            key={item.id}
            onClick={() => onNavigate(item.id)}
            className={cn(
              "w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors text-sm font-medium",
              currentView === item.id 
                ? "bg-blue-600 text-white" 
                : "text-slate-400 hover:bg-slate-800 hover:text-white"
            )}
          >
            <item.icon className="w-5 h-5" />
            {item.label}
          </button>
        ))}
      </nav>

      <div className="p-4 border-t border-slate-800">
        <button
          onClick={onOpenSettings}
          className="w-full flex items-center gap-3 px-4 py-3 rounded-lg text-slate-400 hover:bg-slate-800 hover:text-white transition-colors text-sm font-medium"
        >
          <Settings className="w-5 h-5" />
          设置
        </button>
      </div>
    </aside>
  )
}
