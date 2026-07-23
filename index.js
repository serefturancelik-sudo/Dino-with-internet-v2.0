const { app, BrowserWindow } = require('electron');
const path = require('path');

function createWindow() {
  const mainWindow = new BrowserWindow({
    width: 800,
    height: 500,
    backgroundColor: '#0b0f1a',
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false
    }
  });

  // Load the exact HTML game file we created earlier
  mainWindow.loadFile(path.join(__dirname, 'index.html'));
  
  // Remove menu bar for full immersive arcade experience
  mainWindow.setMenuBarVisibility(false);
}

app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
