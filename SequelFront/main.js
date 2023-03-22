const { app, BrowserWindow } = require('electron')

try {
  require('electron-reloader')(module)
} catch (_) {}

const createWindow = () => {
  const win = new BrowserWindow({
    width: 1280,
    height: 720
  })

  win.loadFile('./src/index.html')
}

app.whenReady().then(() => {
  createWindow()
})
