const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const path = require('path');
const { spawn, exec } = require('child_process');
const fs = require('fs');

class ElectronApp {
    constructor() {
        this.mainWindow = null;
        this.pythonProcess = null;
        this.serverProcess = null;
        this.isDev = process.argv.includes('--dev');
    }

    createWindow() {
        this.mainWindow = new BrowserWindow({
            width: 1200,
            height: 900,
            minWidth: 800,
            minHeight: 600,
            webPreferences: {
                nodeIntegration: false,
                contextIsolation: true,
                preload: path.join(__dirname, 'preload.js')
            },
            icon: path.join(__dirname, '../assets/icon.png'),
            titleBarStyle: 'default',
            frame: true
        });

        this.mainWindow.loadFile(path.join(__dirname, 'renderer/index.html'));

        if (this.isDev) {
            this.mainWindow.webContents.openDevTools();
        }

        this.mainWindow.on('closed', () => {
            this.mainWindow = null;
            this.cleanup();
        });

        // Start Python backend server
        this.startPythonServer();
    }

    startPythonServer() {
        const pythonScript = path.join(__dirname, '../python/server.py');
        
        // Check if Python script exists
        if (!fs.existsSync(pythonScript)) {
            console.error('Python server script not found:', pythonScript);
            return;
        }

        try {
            this.pythonProcess = spawn('python', [pythonScript], {
                cwd: path.dirname(pythonScript)
            });

            this.pythonProcess.stdout.on('data', (data) => {
                console.log('Python:', data.toString());
                if (this.mainWindow) {
                    this.mainWindow.webContents.send('python-log', data.toString());
                }
            });

            this.pythonProcess.stderr.on('data', (data) => {
                console.error('Python Error:', data.toString());
                if (this.mainWindow) {
                    this.mainWindow.webContents.send('python-error', data.toString());
                }
            });

            this.pythonProcess.on('close', (code) => {
                console.log(`Python process exited with code ${code}`);
            });

        } catch (error) {
            console.error('Failed to start Python server:', error);
        }
    }

    cleanup() {
        if (this.pythonProcess) {
            this.pythonProcess.kill();
            this.pythonProcess = null;
        }
        if (this.serverProcess) {
            this.serverProcess.kill();
            this.serverProcess = null;
        }
    }

    setupIPC() {
        // Handle window controls
        ipcMain.handle('minimize-window', () => {
            if (this.mainWindow) this.mainWindow.minimize();
        });

        ipcMain.handle('maximize-window', () => {
            if (this.mainWindow) {
                if (this.mainWindow.isMaximized()) {
                    this.mainWindow.unmaximize();
                } else {
                    this.mainWindow.maximize();
                }
            }
        });

        ipcMain.handle('close-window', () => {
            if (this.mainWindow) this.mainWindow.close();
        });

        // Handle gamepad operations
        ipcMain.handle('gamepad-connect', async () => {
            return this.sendToPython('connect');
        });

        ipcMain.handle('gamepad-disconnect', async () => {
            return this.sendToPython('disconnect');
        });

        ipcMain.handle('gamepad-toggle-movement', async () => {
            return this.sendToPython('toggle_movement');
        });

        ipcMain.handle('gamepad-toggle-anti-afk', async () => {
            return this.sendToPython('toggle_anti_afk');
        });

        ipcMain.handle('gamepad-select-class', async () => {
            return this.sendToPython('select_class');
        });

        ipcMain.handle('gamepad-update-setting', async (event, section, key, value) => {
            return this.sendToPython('update_setting', { section, key, value });
        });

        ipcMain.handle('gamepad-save-settings', async () => {
            return this.sendToPython('save_settings');
        });

        // Handle browser operations
        ipcMain.handle('open-xbox-sessions', async (event, numAccounts) => {
            return this.openXboxSessions(numAccounts);
        });

        ipcMain.handle('launch-black-ops', async (event, numAccounts) => {
            return this.launchBlackOps(numAccounts);
        });

        // Get available profiles
        ipcMain.handle('get-profiles', async () => {
            return this.getAvailableProfiles();
        });

        // Show file dialog
        ipcMain.handle('show-open-dialog', async (event, options) => {
            const result = await dialog.showOpenDialog(this.mainWindow, options);
            return result;
        });
    }

    async sendToPython(command, data = {}) {
        // This would communicate with the Python backend via HTTP or IPC
        // For now, return a mock response
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve({ success: true, message: `${command} executed` });
            }, 100);
        });
    }

    getAvailableProfiles() {
        const shortcutsPath = path.join(__dirname, '../Shortcuts');
        const profiles = [];
        
        try {
            if (fs.existsSync(shortcutsPath)) {
                for (let i = 1; i <= 20; i++) {
                    const profilePath = path.join(shortcutsPath, `b${i}.lnk`);
                    if (fs.existsSync(profilePath)) {
                        profiles.push(`b${i}`);
                    }
                }
            }
        } catch (error) {
            console.error('Error scanning profiles:', error);
        }
        
        return profiles;
    }

    openXboxSessions(numAccounts) {
        return new Promise((resolve) => {
            try {
                const profiles = this.getAvailableProfiles();
                const accountsToOpen = Math.min(numAccounts, profiles.length);
                
                for (let i = 0; i < accountsToOpen; i++) {
                    const profile = profiles[i];
                    const shortcutPath = path.join(__dirname, '../Shortcuts', `${profile}.lnk`);
                    
                    exec(`start "" "${shortcutPath}" "https://xbox.com/play"`, (error) => {
                        if (error) {
                            console.error(`Error opening session ${i + 1}:`, error);
                        }
                    });
                }
                
                resolve({ success: true, message: `Opened ${accountsToOpen} Xbox sessions` });
            } catch (error) {
                resolve({ success: false, message: error.message });
            }
        });
    }

    launchBlackOps(numAccounts) {
        return new Promise((resolve) => {
            try {
                const profiles = this.getAvailableProfiles();
                const accountsToLaunch = Math.min(numAccounts, profiles.length);
                const bo6Url = "https://www.xbox.com/en-US/play/launch/call-of-duty-black-ops-6---cross-gen-bundle/9PF528M6CRHQ";
                
                for (let i = 0; i < accountsToLaunch; i++) {
                    const profile = profiles[i];
                    const shortcutPath = path.join(__dirname, '../Shortcuts', `${profile}.lnk`);
                    
                    exec(`start "" "${shortcutPath}" "${bo6Url}"`, (error) => {
                        if (error) {
                            console.error(`Error launching BO6 for ${profile}:`, error);
                        }
                    });
                }
                
                resolve({ success: true, message: `Launched Black Ops 6 for ${accountsToLaunch} profiles` });
            } catch (error) {
                resolve({ success: false, message: error.message });
            }
        });
    }

    init() {
        app.whenReady().then(() => {
            this.createWindow();
            this.setupIPC();

            app.on('activate', () => {
                if (BrowserWindow.getAllWindows().length === 0) {
                    this.createWindow();
                }
            });
        });

        app.on('window-all-closed', () => {
            this.cleanup();
            if (process.platform !== 'darwin') {
                app.quit();
            }
        });

        app.on('before-quit', () => {
            this.cleanup();
        });
    }
}

const electronApp = new ElectronApp();
electronApp.init();