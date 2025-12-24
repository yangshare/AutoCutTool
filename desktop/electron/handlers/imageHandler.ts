import { ipcMain } from 'electron'
import fs from 'node:fs'
import path from 'node:path'

export function setupImageHandlers() {
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
}
