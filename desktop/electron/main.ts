import { app, BrowserWindow, ipcMain, dialog } from 'electron'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

const dist = path.join(__dirname, '../dist')
process.env.DIST = dist
process.env.VITE_PUBLIC = app.isPackaged ? dist : path.join(dist, '../public')

const DIST = process.env.DIST
const VITE_PUBLIC = process.env.VITE_PUBLIC
if (!DIST) throw new Error('DIST is not set')
if (!VITE_PUBLIC) throw new Error('VITE_PUBLIC is not set')

let win: BrowserWindow | null
// 🚧 Use ['ENV_NAME'] avoid vite:define plugin - Vite@2.x
const VITE_DEV_SERVER_URL = process.env['VITE_DEV_SERVER_URL']

function resolvePreloadPath() {
  const candidates = [
    path.join(__dirname, 'preload.cjs'),
    path.join(__dirname, 'preload.js'),
    path.join(__dirname, 'preload.mjs'),
    path.join(__dirname, '../dist-electron/preload.cjs'),
    path.join(__dirname, '../dist-electron/preload.js'),
    path.join(__dirname, '../dist-electron/preload.mjs'),
  ]
  for (const candidate of candidates) {
    if (fs.existsSync(candidate)) return candidate
  }
  return candidates[0]
}

function createWindow() {
  const preloadPath = resolvePreloadPath()
  win = new BrowserWindow({
    icon: path.join(VITE_PUBLIC, 'electron-vite.svg'),
    webPreferences: {
      preload: preloadPath,
      contextIsolation: true,
      nodeIntegration: false,
    },
  })

  // Test active push message to Renderer-process.
  win.webContents.on('did-finish-load', () => {
    win?.webContents.send('main-process-message', (new Date).toLocaleString())
  })

  if (VITE_DEV_SERVER_URL) {
    win.loadURL(VITE_DEV_SERVER_URL)
  } else {
    // win.loadFile('dist/index.html')
    win.loadFile(path.join(DIST, 'index.html'))
  }
}

ipcMain.handle('open-directory-dialog', async (event) => {
  const window = BrowserWindow.fromWebContents(event.sender) || win
  if (!window) return null
  const result = await dialog.showOpenDialog(window, {
    properties: ['openDirectory']
  })
  if (result.canceled) {
    return null
  } else {
    return result.filePaths[0]
  }
})

ipcMain.handle('get-first-image', async (event, dirPath) => {
  try {
    const files = await fs.promises.readdir(dirPath)
    const imageExtensions = ['.jpg', '.jpeg', '.png', '.bmp', '.webp']
    const imageFile = files.find(file => 
      imageExtensions.includes(path.extname(file).toLowerCase())
    )
    
    if (imageFile) {
      const fullPath = path.join(dirPath, imageFile)
      const imageBuffer = await fs.promises.readFile(fullPath)
      const base64Image = imageBuffer.toString('base64')
      const ext = path.extname(fullPath).slice(1)
      return `data:image/${ext};base64,${base64Image}`
    }
    return null
  } catch (error) {
    console.error('Error reading directory:', error)
    return null
  }
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
    win = null
  }
})

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow()
  }
})

app.whenReady().then(createWindow)
