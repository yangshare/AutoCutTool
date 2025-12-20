import { useState, useEffect } from 'react'
import { Folder, Zap, AlertCircle, CheckCircle2 } from 'lucide-react'
import { cn } from '@/lib/utils'

export default function GeneratorView() {
  const [videoDirectory, setVideoDirectory] = useState('')
  const [audioDirectory, setAudioDirectory] = useState('')
  const [draftName, setDraftName] = useState('')
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')
  const [backendUrl, setBackendUrl] = useState('http://127.0.0.1:9001')
  const [draftDirectory, setDraftDirectory] = useState('')
  const isElectron = typeof window !== 'undefined' && !!(window as any).ipcRenderer && typeof (window as any).ipcRenderer.invoke === 'function'

  useEffect(() => {
    const savedUrl = localStorage.getItem('backendUrl')
    if (savedUrl) setBackendUrl(savedUrl)
    
    const savedDraftDir = localStorage.getItem('draftDirectory')
    if (savedDraftDir) setDraftDirectory(savedDraftDir)
  }, [])

  const selectDirectory = async (setter: (path: string) => void) => {
    if (!isElectron) {
      alert('当前在浏览器预览环境中，无法调用系统目录选择器。请手动输入路径。')
      return
    }
    try {
      console.log('Invoking open-directory-dialog')
      const path = await (window as any).ipcRenderer.invoke('open-directory-dialog')
      console.log('Selected path:', path)
      if (path) {
        setter(path)
      }
    } catch (err: any) {
      console.error(err)
      alert('目录选择失败：' + (err.message || err))
    }
  }

  const generateDraft = async () => {
    setLoading(true)
    setMessage('')
    setError('')

    if (!draftDirectory) {
      setError('Please configure Draft Directory in Settings first.')
      setLoading(false)
      return
    }

    if (!videoDirectory || !audioDirectory) {
      setError('Please select video and audio directories.')
      setLoading(false)
      return
    }

    try {
      const response = await fetch(`${backendUrl}/generate_batch_draft`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          video_dir: videoDirectory,
          audio_dir: audioDirectory,
          draft_folder: draftDirectory,
          draft_name: draftName || undefined
        })
      })

      const data = await response.json()

      if (data.success) {
        setMessage(`Draft generated successfully! ID: ${data.output.draft_id}`)
      } else {
        setError(`Failed: ${data.error}`)
      }
    } catch (err: any) {
      setError(`Network error: ${err.message}`)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="p-10 h-full flex flex-col bg-slate-50 text-slate-900">
      <header className="text-center mb-10">
        <h1 className="text-3xl font-bold text-slate-800 mb-2">剪映草稿生成器</h1>
        <p className="text-slate-500">选好视频和音频素材，一键生成精美草稿 </p>
      </header>

      <div className="max-w-5xl mx-auto w-full grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Left: Inputs */}
        <div className="bg-white p-8 rounded-2xl shadow-sm border border-slate-100 space-y-6">
          <div className="space-y-2">
            <label className="block text-sm font-semibold text-slate-700">Video Materials Directory</label>
            <div className="flex gap-2">
              <input 
                type="text" 
                value={videoDirectory}
                onChange={(e) => setVideoDirectory(e.target.value)}
                placeholder="Select video directory..."
                className="flex-1 px-4 py-2 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
              />
              <button 
                onClick={() => selectDirectory(setVideoDirectory)}
                className="p-2 bg-slate-100 text-slate-600 rounded-lg hover:bg-slate-200 transition-colors"
              >
                <Folder className="w-5 h-5" />
              </button>
            </div>
          </div>

          <div className="space-y-2">
            <label className="block text-sm font-semibold text-slate-700">Audio Materials Directory</label>
            <div className="flex gap-2">
              <input 
                type="text" 
                value={audioDirectory}
                onChange={(e) => setAudioDirectory(e.target.value)}
                placeholder="Select audio directory..."
                className="flex-1 px-4 py-2 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
              />
              <button 
                onClick={() => selectDirectory(setAudioDirectory)}
                className="p-2 bg-slate-100 text-slate-600 rounded-lg hover:bg-slate-200 transition-colors"
              >
                <Folder className="w-5 h-5" />
              </button>
            </div>
          </div>

          <div className="space-y-2">
            <label className="block text-sm font-semibold text-slate-700">Draft Name (Optional)</label>
            <input 
              type="text" 
              value={draftName}
              onChange={(e) => setDraftName(e.target.value)}
              placeholder="Enter draft name..." 
              className="w-full px-4 py-2 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
            />
          </div>

          <button 
            onClick={generateDraft} 
            disabled={loading}
            className={cn(
              "w-full py-3 rounded-xl text-white font-semibold flex items-center justify-center gap-2 transition-all shadow-md hover:shadow-lg",
              loading ? "bg-blue-400 cursor-not-allowed" : "bg-blue-600 hover:bg-blue-700 hover:-translate-y-0.5"
            )}
          >
            <Zap className="w-5 h-5 fill-current" />
            {loading ? 'Generating...' : '生成内容'}
          </button>

          {message && (
            <div className="p-4 bg-green-50 text-green-700 rounded-xl flex items-start gap-3 border border-green-100">
              <CheckCircle2 className="w-5 h-5 shrink-0 mt-0.5" />
              <p className="text-sm font-medium">{message}</p>
            </div>
          )}

          {error && (
            <div className="p-4 bg-red-50 text-red-700 rounded-xl flex items-start gap-3 border border-red-100">
              <AlertCircle className="w-5 h-5 shrink-0 mt-0.5" />
              <p className="text-sm font-medium">{error}</p>
            </div>
          )}
        </div>

        {/* Right: Preview (Placeholder) */}
        <div className="bg-white p-8 rounded-2xl shadow-sm border border-slate-100 flex flex-col items-center justify-center min-h-[400px] text-slate-400">
          <div className="w-24 h-24 bg-slate-100 rounded-full flex items-center justify-center mb-4">
             <Folder className="w-10 h-10 text-slate-300" />
          </div>
          <p className="font-medium">预览区域 (待开发)</p>
          <p className="text-sm mt-2 text-slate-400">生成的内容将在此处显示预览</p>
        </div>
      </div>
    </div>
  )
}
