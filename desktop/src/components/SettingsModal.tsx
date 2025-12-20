import { useState, useEffect } from 'react'
import { X, Folder, Save } from 'lucide-react'

interface SettingsModalProps {
  onClose: () => void
}

export default function SettingsModal({ onClose }: SettingsModalProps) {
  const [backendUrl, setBackendUrl] = useState('http://127.0.0.1:9001')
  const [draftDirectory, setDraftDirectory] = useState('')
  const isElectron = typeof window !== 'undefined' && !!(window as any).ipcRenderer && typeof (window as any).ipcRenderer.invoke === 'function'

  useEffect(() => {
    const savedUrl = localStorage.getItem('backendUrl')
    if (savedUrl) setBackendUrl(savedUrl)
    
    const savedDraftDir = localStorage.getItem('draftDirectory')
    if (savedDraftDir) setDraftDirectory(savedDraftDir)
  }, [])

  const selectDraftDirectory = async () => {
    if (!isElectron) {
      alert('当前在浏览器预览环境中，无法调用系统目录选择器。请手动输入路径。')
      return
    }
    try {
      console.log('Invoking open-directory-dialog')
      const path = await (window as any).ipcRenderer.invoke('open-directory-dialog')
      console.log('Selected path:', path)
      if (path) {
        setDraftDirectory(path)
      }
    } catch (error: any) {
      console.error('Failed to open directory dialog:', error)
      alert(`目录选择器调用失败: ${error.message || error}`)
    }
  }

  const saveSettings = () => {
    localStorage.setItem('backendUrl', backendUrl)
    localStorage.setItem('draftDirectory', draftDirectory)
    onClose()
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm" onClick={onClose}>
      <div 
        className="w-[500px] bg-white rounded-xl shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-200"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-100">
          <h3 className="text-lg font-semibold text-slate-800">系统设置</h3>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-600 transition-colors">
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="p-6 space-y-6">
          <div className="space-y-2">
            <label className="text-sm font-medium text-slate-700">API Base URL</label>
            <input 
              type="text" 
              value={backendUrl}
              onChange={(e) => setBackendUrl(e.target.value)}
              placeholder="http://127.0.0.1:9001"
              className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
            />
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium text-slate-700">下载路径 (Jianying Draft Directory)</label>
            <div className="flex gap-2">
              <input 
                type="text" 
                value={draftDirectory}
                onChange={(e) => setDraftDirectory(e.target.value)}
                className="flex-1 px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
              />
              <button 
                onClick={selectDraftDirectory}
                className="px-3 py-2 bg-slate-100 text-slate-600 rounded-lg hover:bg-slate-200 transition-colors border border-slate-200"
              >
                <Folder className="w-4 h-4" />
              </button>
            </div>
            {!isElectron && (
              <p className="text-xs text-slate-500 mt-1">提示：浏览器预览不支持系统目录选择，请手动输入完整路径或在桌面应用中操作。</p>
            )}
          </div>

          <div className="pt-4 border-t border-slate-100 flex justify-between items-center text-xs text-slate-500">
            <span>当前版本: v1.0.0</span>
            <a href="#" className="hover:text-blue-600">打开日志目录</a>
          </div>
        </div>

        <div className="px-6 py-4 bg-slate-50 border-t border-slate-100 flex justify-end">
          <button 
            onClick={saveSettings}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium shadow-sm hover:shadow"
          >
            <Save className="w-4 h-4" />
            保存设置
          </button>
        </div>
      </div>
    </div>
  )
}
