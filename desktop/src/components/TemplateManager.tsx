import { useState, useEffect } from 'react'
import { Plus, Trash2, Edit2, Save, X, ChevronDown, ChevronUp, Type, Sparkles, Filter } from 'lucide-react'
import { cn } from '@/lib/utils'

interface Template {
  id: string
  name: string
  tracks: {
    texts: TextTrack[]
    effects: EffectTrack[]
    filters: FilterTrack[]
  }
  updated_at?: number
}

interface TextTrack {
  text: string
  start: number
  end: number
  is_full_duration?: boolean
  font?: string
  font_size: number
  font_color: string
  font_alpha?: number
  bold?: boolean
  italic?: boolean
  underline?: boolean
  transform_x?: number
  transform_y?: number
  vertical?: boolean
  style?: any // For complex styles if needed
}

interface EffectTrack {
  effect_type: string
  start: number
  end: number
  is_full_duration?: boolean
  track_name?: string
}

interface FilterTrack {
  effect_type: string
  start: number
  end: number
  is_full_duration?: boolean
  track_name?: string
}

const DEFAULT_TEXT_TRACK: TextTrack = {
  text: '新文本',
  start: 0,
  end: 5,
  is_full_duration: true,
  font_size: 8.0,
  font_color: '#FFFFFF',
  font_alpha: 1.0,
  bold: false,
  transform_x: 0,
  transform_y: 0
}

const DEFAULT_EFFECT_TRACK: EffectTrack = {
  effect_type: '圣诞星光',
  start: 0,
  end: 5,
  is_full_duration: true
}

const DEFAULT_FILTER_TRACK: FilterTrack = {
  effect_type: '高清',
  start: 0,
  end: 5,
  is_full_duration: true
}

export default function TemplateManager() {
  const [templates, setTemplates] = useState<Template[]>([])
  const [loading, setLoading] = useState(false)
  const [editingTemplate, setEditingTemplate] = useState<Template | null>(null)
  const [isCreating, setIsCreating] = useState(false)
  const [backendUrl] = useState(localStorage.getItem('backendUrl') || 'http://127.0.0.1:9001')

  useEffect(() => {
    fetchTemplates()
  }, [])

  const fetchTemplates = async () => {
    try {
      setLoading(true)
      const res = await fetch(`${backendUrl}/templates`)
      const data = await res.json()
      if (data.success) {
        setTemplates(data.output)
      }
    } catch (error) {
      console.error('Failed to fetch templates:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (id: string) => {
    if (!confirm('确定要删除这个模板吗？')) return
    try {
      const res = await fetch(`${backendUrl}/templates/${id}`, { method: 'DELETE' })
      const data = await res.json()
      if (data.success) {
        fetchTemplates()
      }
    } catch (error) {
      console.error('Failed to delete template:', error)
    }
  }

  const handleSave = async () => {
    if (!editingTemplate) return
    
    try {
      const isNew = !editingTemplate.id
      const url = isNew ? `${backendUrl}/templates` : `${backendUrl}/templates/${editingTemplate.id}`
      const method = isNew ? 'POST' : 'PUT'
      
      const res = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: editingTemplate.name,
          tracks: editingTemplate.tracks
        })
      })
      
      const data = await res.json()
      if (data.success) {
        setEditingTemplate(null)
        setIsCreating(false)
        fetchTemplates()
      } else {
        alert('保存失败: ' + data.error)
      }
    } catch (error) {
      alert('保存出错')
      console.error(error)
    }
  }

  const startCreate = () => {
    setEditingTemplate({
      id: '',
      name: '新模板',
      tracks: {
        texts: [],
        effects: [],
        filters: []
      }
    })
    setIsCreating(true)
  }

  if (editingTemplate) {
    return (
      <div className="p-10 h-full flex flex-col bg-slate-50 text-slate-900 overflow-auto">
        <div className="max-w-4xl mx-auto w-full space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-2xl font-bold">{isCreating ? '创建模板' : '编辑模板'}</h2>
            <div className="flex gap-2">
              <button onClick={() => { setEditingTemplate(null); setIsCreating(false) }} className="px-4 py-2 rounded-lg border border-slate-200 hover:bg-slate-100">取消</button>
              <button onClick={handleSave} className="px-4 py-2 rounded-lg bg-blue-600 text-white hover:bg-blue-700 flex items-center gap-2">
                <Save className="w-4 h-4" /> 保存
              </button>
            </div>
          </div>

          <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-100 space-y-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">模板名称</label>
              <input 
                value={editingTemplate.name}
                onChange={e => setEditingTemplate({...editingTemplate, name: e.target.value})}
                className="w-full px-4 py-2 border rounded-lg"
              />
            </div>
          </div>

          {/* Texts Section */}
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-semibold flex items-center gap-2"><Type className="w-5 h-5"/> 文字轨道</h3>
              <button 
                onClick={() => setEditingTemplate({
                  ...editingTemplate,
                  tracks: {
                    ...editingTemplate.tracks,
                    texts: [...(editingTemplate.tracks.texts || []), { ...DEFAULT_TEXT_TRACK }]
                  }
                })}
                className="text-sm text-blue-600 hover:underline flex items-center gap-1"
              >
                <Plus className="w-4 h-4"/> 添加文字
              </button>
            </div>
            {editingTemplate.tracks.texts?.map((track, idx) => (
              <div key={idx} className="bg-white p-4 rounded-xl shadow-sm border border-slate-100 relative group">
                <button 
                  onClick={() => {
                    const newTexts = [...editingTemplate.tracks.texts]
                    newTexts.splice(idx, 1)
                    setEditingTemplate({
                      ...editingTemplate,
                      tracks: { ...editingTemplate.tracks, texts: newTexts }
                    })
                  }}
                  className="absolute top-4 right-4 text-slate-400 hover:text-red-500 opacity-0 group-hover:opacity-100 transition-opacity"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
                <div className="grid grid-cols-2 gap-4">
                  <div className="col-span-2">
                    <label className="text-xs text-slate-500">内容</label>
                    <input 
                      value={track.text}
                      onChange={e => {
                        const newTexts = [...editingTemplate.tracks.texts]
                        newTexts[idx] = { ...track, text: e.target.value }
                        setEditingTemplate({ ...editingTemplate, tracks: { ...editingTemplate.tracks, texts: newTexts } })
                      }}
                      className="w-full px-3 py-1.5 border rounded text-sm"
                    />
                  </div>
                  <div>
                    <label className="text-xs text-slate-500">字体大小</label>
                    <input 
                      type="number"
                      value={track.font_size}
                      onChange={e => {
                        const newTexts = [...editingTemplate.tracks.texts]
                        newTexts[idx] = { ...track, font_size: parseFloat(e.target.value) }
                        setEditingTemplate({ ...editingTemplate, tracks: { ...editingTemplate.tracks, texts: newTexts } })
                      }}
                      className="w-full px-3 py-1.5 border rounded text-sm"
                    />
                  </div>
                  <div>
                    <label className="text-xs text-slate-500">颜色 (Hex)</label>
                    <div className="flex gap-2">
                        <input 
                        type="color"
                        value={track.font_color}
                        onChange={e => {
                            const newTexts = [...editingTemplate.tracks.texts]
                            newTexts[idx] = { ...track, font_color: e.target.value }
                            setEditingTemplate({ ...editingTemplate, tracks: { ...editingTemplate.tracks, texts: newTexts } })
                        }}
                        className="h-8 w-8 rounded cursor-pointer border-0"
                        />
                        <input 
                        value={track.font_color}
                        onChange={e => {
                            const newTexts = [...editingTemplate.tracks.texts]
                            newTexts[idx] = { ...track, font_color: e.target.value }
                            setEditingTemplate({ ...editingTemplate, tracks: { ...editingTemplate.tracks, texts: newTexts } })
                        }}
                        className="flex-1 px-3 py-1.5 border rounded text-sm"
                        />
                    </div>
                  </div>
                  <div>
                    <label className="text-xs text-slate-500">位置 X (-1 ~ 1)</label>
                    <input 
                      type="number"
                      step="0.1"
                      value={track.transform_x || 0}
                      onChange={e => {
                        const newTexts = [...editingTemplate.tracks.texts]
                        newTexts[idx] = { ...track, transform_x: parseFloat(e.target.value) }
                        setEditingTemplate({ ...editingTemplate, tracks: { ...editingTemplate.tracks, texts: newTexts } })
                      }}
                      className="w-full px-3 py-1.5 border rounded text-sm"
                    />
                  </div>
                  <div>
                    <label className="text-xs text-slate-500">位置 Y (-1 ~ 1)</label>
                    <input 
                      type="number"
                      step="0.1"
                      value={track.transform_y || 0}
                      onChange={e => {
                        const newTexts = [...editingTemplate.tracks.texts]
                        newTexts[idx] = { ...track, transform_y: parseFloat(e.target.value) }
                        setEditingTemplate({ ...editingTemplate, tracks: { ...editingTemplate.tracks, texts: newTexts } })
                      }}
                      className="w-full px-3 py-1.5 border rounded text-sm"
                    />
                  </div>
                  <div className="flex items-center gap-4">
                    <label className="flex items-center gap-2 text-sm cursor-pointer">
                      <input 
                        type="checkbox"
                        checked={track.is_full_duration}
                        onChange={e => {
                          const newTexts = [...editingTemplate.tracks.texts]
                          newTexts[idx] = { ...track, is_full_duration: e.target.checked }
                          setEditingTemplate({ ...editingTemplate, tracks: { ...editingTemplate.tracks, texts: newTexts } })
                        }}
                        className="rounded text-blue-600"
                      />
                      全程显示
                    </label>
                    <label className="flex items-center gap-2 text-sm cursor-pointer">
                      <input 
                        type="checkbox"
                        checked={track.bold}
                        onChange={e => {
                          const newTexts = [...editingTemplate.tracks.texts]
                          newTexts[idx] = { ...track, bold: e.target.checked }
                          setEditingTemplate({ ...editingTemplate, tracks: { ...editingTemplate.tracks, texts: newTexts } })
                        }}
                        className="rounded text-blue-600"
                      />
                      粗体
                    </label>
                    <label className="flex items-center gap-2 text-sm cursor-pointer">
                      <input 
                        type="checkbox"
                        checked={track.vertical}
                        onChange={e => {
                          const newTexts = [...editingTemplate.tracks.texts]
                          newTexts[idx] = { ...track, vertical: e.target.checked }
                          setEditingTemplate({ ...editingTemplate, tracks: { ...editingTemplate.tracks, texts: newTexts } })
                        }}
                        className="rounded text-blue-600"
                      />
                      竖排
                    </label>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Effects Section */}
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-semibold flex items-center gap-2"><Sparkles className="w-5 h-5"/> 特效轨道</h3>
              <button 
                onClick={() => setEditingTemplate({
                  ...editingTemplate,
                  tracks: {
                    ...editingTemplate.tracks,
                    effects: [...(editingTemplate.tracks.effects || []), { ...DEFAULT_EFFECT_TRACK }]
                  }
                })}
                className="text-sm text-blue-600 hover:underline flex items-center gap-1"
              >
                <Plus className="w-4 h-4"/> 添加特效
              </button>
            </div>
            {editingTemplate.tracks.effects?.map((track, idx) => (
              <div key={idx} className="bg-white p-4 rounded-xl shadow-sm border border-slate-100 relative group flex gap-4 items-center">
                <div className="flex-1">
                  <label className="text-xs text-slate-500">特效名称</label>
                  <input 
                    value={track.effect_type}
                    onChange={e => {
                      const newEffects = [...editingTemplate.tracks.effects]
                      newEffects[idx] = { ...track, effect_type: e.target.value }
                      setEditingTemplate({ ...editingTemplate, tracks: { ...editingTemplate.tracks, effects: newEffects } })
                    }}
                    className="w-full px-3 py-1.5 border rounded text-sm"
                    placeholder="例如: 圣诞星光"
                  />
                </div>
                <div className="flex items-center gap-2 pt-4">
                  <label className="flex items-center gap-2 text-sm cursor-pointer whitespace-nowrap">
                    <input 
                      type="checkbox"
                      checked={track.is_full_duration}
                      onChange={e => {
                        const newEffects = [...editingTemplate.tracks.effects]
                        newEffects[idx] = { ...track, is_full_duration: e.target.checked }
                        setEditingTemplate({ ...editingTemplate, tracks: { ...editingTemplate.tracks, effects: newEffects } })
                      }}
                      className="rounded text-blue-600"
                    />
                    全程显示
                  </label>
                </div>
                <button 
                  onClick={() => {
                    const newEffects = [...editingTemplate.tracks.effects]
                    newEffects.splice(idx, 1)
                    setEditingTemplate({
                      ...editingTemplate,
                      tracks: { ...editingTemplate.tracks, effects: newEffects }
                    })
                  }}
                  className="p-2 text-slate-400 hover:text-red-500 mt-4"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            ))}
          </div>

          {/* Filters Section */}
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-semibold flex items-center gap-2"><Filter className="w-5 h-5"/> 滤镜轨道</h3>
              <button 
                onClick={() => setEditingTemplate({
                  ...editingTemplate,
                  tracks: {
                    ...editingTemplate.tracks,
                    filters: [...(editingTemplate.tracks.filters || []), { ...DEFAULT_FILTER_TRACK }]
                  }
                })}
                className="text-sm text-blue-600 hover:underline flex items-center gap-1"
              >
                <Plus className="w-4 h-4"/> 添加滤镜
              </button>
            </div>
            {editingTemplate.tracks.filters?.map((track, idx) => (
              <div key={idx} className="bg-white p-4 rounded-xl shadow-sm border border-slate-100 relative group flex gap-4 items-center">
                <div className="flex-1">
                  <label className="text-xs text-slate-500">滤镜名称</label>
                  <input 
                    value={track.effect_type}
                    onChange={e => {
                      const newFilters = [...editingTemplate.tracks.filters]
                      newFilters[idx] = { ...track, effect_type: e.target.value }
                      setEditingTemplate({ ...editingTemplate, tracks: { ...editingTemplate.tracks, filters: newFilters } })
                    }}
                    className="w-full px-3 py-1.5 border rounded text-sm"
                    placeholder="例如: 高清"
                  />
                </div>
                <div className="flex items-center gap-2 pt-4">
                  <label className="flex items-center gap-2 text-sm cursor-pointer whitespace-nowrap">
                    <input 
                      type="checkbox"
                      checked={track.is_full_duration}
                      onChange={e => {
                        const newFilters = [...editingTemplate.tracks.filters]
                        newFilters[idx] = { ...track, is_full_duration: e.target.checked }
                        setEditingTemplate({ ...editingTemplate, tracks: { ...editingTemplate.tracks, filters: newFilters } })
                      }}
                      className="rounded text-blue-600"
                    />
                    全程显示
                  </label>
                </div>
                <button 
                  onClick={() => {
                    const newFilters = [...editingTemplate.tracks.filters]
                    newFilters.splice(idx, 1)
                    setEditingTemplate({
                      ...editingTemplate,
                      tracks: { ...editingTemplate.tracks, filters: newFilters }
                    })
                  }}
                  className="p-2 text-slate-400 hover:text-red-500 mt-4"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            ))}
          </div>

        </div>
      </div>
    )
  }

  return (
    <div className="p-10 h-full flex flex-col bg-slate-50 text-slate-900">
      <header className="flex items-center justify-between mb-10">
        <div>
          <h1 className="text-3xl font-bold text-slate-800 mb-2">模板管理</h1>
          <p className="text-slate-500">创建和管理您的剪辑模板</p>
        </div>
        <button 
          onClick={startCreate}
          className="px-6 py-3 bg-blue-600 text-white rounded-xl hover:bg-blue-700 font-semibold shadow-md flex items-center gap-2"
        >
          <Plus className="w-5 h-5" /> 新建模板
        </button>
      </header>

      {loading ? (
        <div className="text-center py-20 text-slate-400">加载中...</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {templates.map(template => (
            <div key={template.id} className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 hover:shadow-md transition-shadow group relative">
              <div className="absolute top-4 right-4 flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                <button 
                  onClick={() => setEditingTemplate(template)}
                  className="p-2 bg-slate-100 hover:bg-slate-200 rounded-lg text-slate-600"
                >
                  <Edit2 className="w-4 h-4" />
                </button>
                <button 
                  onClick={() => handleDelete(template.id)}
                  className="p-2 bg-red-50 hover:bg-red-100 rounded-lg text-red-600"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
              
              <h3 className="text-xl font-bold text-slate-800 mb-2 truncate pr-16">{template.name}</h3>
              <div className="space-y-2 text-sm text-slate-500">
                <div className="flex items-center gap-2">
                  <Type className="w-4 h-4" />
                  <span>{template.tracks.texts?.length || 0} 个文字轨道</span>
                </div>
                <div className="flex items-center gap-2">
                  <Sparkles className="w-4 h-4" />
                  <span>{template.tracks.effects?.length || 0} 个特效轨道</span>
                </div>
                <div className="flex items-center gap-2">
                  <Filter className="w-4 h-4" />
                  <span>{template.tracks.filters?.length || 0} 个滤镜轨道</span>
                </div>
              </div>
              <div className="mt-4 text-xs text-slate-400">
                更新于: {new Date((template.updated_at || 0)).toLocaleString()}
              </div>
            </div>
          ))}
          {templates.length === 0 && (
            <div className="col-span-full text-center py-20 text-slate-400 bg-slate-100/50 rounded-2xl border-dashed border-2 border-slate-200">
              <p>暂无模板，点击右上角创建</p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
