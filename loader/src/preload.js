const { contextBridge, ipcRenderer } = require('electron');

// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld('electronAPI', {
    // Window controls
    minimizeWindow: () => ipcRenderer.invoke('minimize-window'),
    maximizeWindow: () => ipcRenderer.invoke('maximize-window'),
    closeWindow: () => ipcRenderer.invoke('close-window'),

    // Gamepad operations
    gamepad: {
        connect: () => ipcRenderer.invoke('gamepad-connect'),
        disconnect: () => ipcRenderer.invoke('gamepad-disconnect'),
        toggleMovement: () => ipcRenderer.invoke('gamepad-toggle-movement'),
        toggleAntiAfk: () => ipcRenderer.invoke('gamepad-toggle-anti-afk'),
        selectClass: () => ipcRenderer.invoke('gamepad-select-class'),
        updateSetting: (section, key, value) => ipcRenderer.invoke('gamepad-update-setting', section, key, value),
        saveSettings: () => ipcRenderer.invoke('gamepad-save-settings')
    },

    // Browser operations
    browser: {
        openXboxSessions: (numAccounts) => ipcRenderer.invoke('open-xbox-sessions', numAccounts),
        launchBlackOps: (numAccounts) => ipcRenderer.invoke('launch-black-ops', numAccounts),
        getProfiles: () => ipcRenderer.invoke('get-profiles')
    },

    // File operations
    showOpenDialog: (options) => ipcRenderer.invoke('show-open-dialog', options),

    // Event listeners
    onPythonLog: (callback) => ipcRenderer.on('python-log', callback),
    onPythonError: (callback) => ipcRenderer.on('python-error', callback),
    
    // Remove listeners
    removeAllListeners: (channel) => ipcRenderer.removeAllListeners(channel)
});