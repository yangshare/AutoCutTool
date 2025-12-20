import { useState } from 'react'
import Sidebar from './components/Sidebar'
import GeneratorView from './components/GeneratorView'
import TemplateManager from './components/TemplateManager'
import SettingsModal from './components/SettingsModal'

function App() {
  const [currentView, setCurrentView] = useState('generator')
  const [isSettingsOpen, setIsSettingsOpen] = useState(false)

  return (
    <div className="flex h-screen bg-slate-50 text-slate-900 font-sans">
      <Sidebar 
        currentView={currentView} 
        onNavigate={setCurrentView} 
        onOpenSettings={() => setIsSettingsOpen(true)}
      />
      <main className="flex-1 overflow-auto">
        {currentView === 'generator' && <GeneratorView />}
        {currentView === 'templates' && <TemplateManager />}
        {/* Add other views here if needed */}
      </main>
      
      {isSettingsOpen && (
        <SettingsModal onClose={() => setIsSettingsOpen(false)} />
      )}
    </div>
  )
}

export default App
