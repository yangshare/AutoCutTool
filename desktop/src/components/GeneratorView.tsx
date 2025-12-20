import { useState, useEffect, useRef } from 'react'
import { Folder, Zap, AlertCircle, CheckCircle2, Image as ImageIcon, LayoutTemplate } from 'lucide-react'
import { cn } from '@/lib/utils'
import ReactCrop, { type Crop, type PixelCrop } from 'react-image-crop'
import 'react-image-crop/dist/ReactCrop.css'

interface Template {
  id: string
  name: string
}

export default function GeneratorView() {
  const [videoDirectory, setVideoDirectory] = useState('')
  const [audioDirectory, setAudioDirectory] = useState('')
  const [imageDirectory, setImageDirectory] = useState('')
  const [draftName, setDraftName] = useState('')
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')
  const [backendUrl, setBackendUrl] = useState('http://127.0.0.1:9001')
  const [draftDirectory, setDraftDirectory] = useState('')
  
  const [templates, setTemplates] = useState<Template[]>([])
  const [selectedTemplateId, setSelectedTemplateId] = useState<string>('')

  const [sampleImage, setSampleImage] = useState('')
  const [crop, setCrop] = useState<Crop>()
  const [completedCrop, setCompletedCrop] = useState<Crop>()
  const imgRef = useRef<HTMLImageElement>(null)

  const isElectron = typeof window !== 'undefined' && !!(window as any).ipcRenderer && typeof (window as any).ipcRenderer.invoke === 'function'

  useEffect(() => {
    const savedUrl = localStorage.getItem('backendUrl')
    if (savedUrl) setBackendUrl(savedUrl)
    
    const savedDraftDir = localStorage.getItem('draftDirectory')
    if (savedDraftDir) setDraftDirectory(savedDraftDir)
    
    fetchTemplates(savedUrl || 'http://127.0.0.1:9001')
  }, [])

  const fetchTemplates = async (url: string) => {
    try {
      const res = await fetch(`${url}/templates`)
      const data = await res.json()
      if (data.success) {
        setTemplates(data.output)
      }
    } catch (err) {
      console.error('Failed to fetch templates:', err)
    }
  }

  const selectDirectory = async (setter: (path: string) => void, isImage = false) => {
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
        if (isImage) {
          fetchFirstImage(path)
        }
      }
    } catch (err: any) {
      console.error(err)
      alert('目录选择失败：' + (err.message || err))
    }
  }

  const fetchFirstImage = async (dirPath: string) => {
    if (!isElectron) return
    try {
      const imageData = await (window as any).ipcRenderer.invoke('get-first-image', dirPath)
      if (imageData) {
        setSampleImage(imageData)
        setCrop(undefined)
        setCompletedCrop(undefined)
      } else {
        setSampleImage('')
      }
    } catch (err) {
      console.error('Error fetching image:', err)
    }
  }

  const generateDraft = async () => {
    setLoading(true)
    setMessage('')
    setError('')

    if (!draftDirectory) {
      setError('请先在设置中配置草稿目录。')
      setLoading(false)
      return
    }

    if (!videoDirectory || !audioDirectory) {
      setError('请选择视频和音频目录。')
      setLoading(false)
      return
    }

    try {
      let imageCropSettings = undefined
      if (completedCrop && completedCrop.width > 0 && completedCrop.height > 0) {
         const x = completedCrop.x / 100
         const y = completedCrop.y / 100
         const w = completedCrop.width / 100
         const h = completedCrop.height / 100
         
         imageCropSettings = {
           upper_left_x: x,
           upper_left_y: y,
           upper_right_x: x + w,
           upper_right_y: y,
           lower_left_x: x,
           lower_left_y: y + h,
           lower_right_x: x + w,
           lower_right_y: y + h
         }
      }

      const response = await fetch(`${backendUrl}/generate_batch_draft`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          video_dir: videoDirectory,
          audio_dir: audioDirectory,
          draft_folder: draftDirectory,
          draft_name: draftName || undefined,
          image_dir: imageDirectory || undefined,
          image_crop_settings: imageCropSettings,
          template_id: selectedTemplateId || undefined
        })
      })

      const data = await response.json()

      if (data.success) {
        setMessage(`草稿生成成功! ID: ${data.output.draft_id}`)
      } else {
        setError(`失败: ${data.error}`)
      }
    } catch (err: any) {
      setError(`网络错误: ${err.message}`)
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
            <label className="block text-sm font-semibold text-slate-700">视频素材目录</label>
            <div className="flex gap-2">
              <input 
                type="text" 
                value={videoDirectory}
                onChange={(e) => setVideoDirectory(e.target.value)}
                placeholder="选择视频目录..."
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
            <label className="block text-sm font-semibold text-slate-700">音频素材目录</label>
            <div className="flex gap-2">
              <input 
                type="text" 
                value={audioDirectory}
                onChange={(e) => setAudioDirectory(e.target.value)}
                placeholder="选择音频目录..."
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
            <label className="block text-sm font-semibold text-slate-700">图片素材目录 (选填)</label>
            <div className="flex gap-2">
              <input 
                type="text" 
                value={imageDirectory}
                onChange={(e) => setImageDirectory(e.target.value)}
                placeholder="选择图片目录..."
                className="flex-1 px-4 py-2 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
              />
              <button 
                onClick={() => selectDirectory(setImageDirectory, true)}
                className="p-2 bg-slate-100 text-slate-600 rounded-lg hover:bg-slate-200 transition-colors"
              >
                <Folder className="w-5 h-5" />
              </button>
            </div>
          </div>

          <div className="space-y-2">
            <label className="block text-sm font-semibold text-slate-700">选择模板 (选填)</label>
            <div className="relative">
              <select 
                value={selectedTemplateId}
                onChange={(e) => setSelectedTemplateId(e.target.value)}
                className="w-full px-4 py-2 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm appearance-none bg-white"
              >
                <option value="">默认模板 (内置效果)</option>
                {templates.map(t => (
                  <option key={t.id} value={t.id}>{t.name}</option>
                ))}
              </select>
              <LayoutTemplate className="w-4 h-4 text-slate-400 absolute right-3 top-3 pointer-events-none" />
            </div>
          </div>

          <div className="space-y-2">
            <label className="block text-sm font-semibold text-slate-700">草稿名称 (选填)</label>
            <input 
              type="text" 
              value={draftName}
              onChange={(e) => setDraftName(e.target.value)}
              placeholder="输入草稿名称..." 
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
            {loading ? '生成中...' : '生成内容'}
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

        {/* Right: Preview */}
        <div className="bg-white p-8 rounded-2xl shadow-sm border border-slate-100 flex flex-col items-center justify-center min-h-[400px] text-slate-400 overflow-hidden relative">
          {sampleImage ? (
            <div className="w-full h-full flex flex-col items-center">
              <p className="text-slate-700 font-medium mb-4">请框选图片需要保留的区域</p>
              <ReactCrop
                crop={crop}
                onChange={(c, p) => setCrop(p)}
                onComplete={(c, p) => setCompletedCrop(p)}
                className="max-h-[500px]"
              >
                <img 
                  ref={imgRef}
                  src={sampleImage} 
                  alt="Sample" 
                  className="max-w-full max-h-[500px] object-contain"
                />
              </ReactCrop>
            </div>
          ) : (
            <>
              <div className="w-24 h-24 bg-slate-100 rounded-full flex items-center justify-center mb-4">
                 <ImageIcon className="w-10 h-10 text-slate-300" />
              </div>
              <p className="font-medium">图片预览区域</p>
              <p className="text-sm mt-2 text-slate-400">选择图片目录后，在此处设置裁剪区域</p>
            </>
          )}
        </div>
      </div>
    </div>
  )
}
