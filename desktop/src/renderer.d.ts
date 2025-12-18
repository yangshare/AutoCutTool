export interface IpcRenderer {
  on(channel: string, listener: (event: any, ...args: any[]) => void): any
  off(channel: string, listener: (event: any, ...args: any[]) => void): any
  send(channel: string, ...args: any[]): any
  invoke(channel: string, ...args: any[]): Promise<any>
}

declare global {
  interface Window {
    ipcRenderer: IpcRenderer
  }
}
