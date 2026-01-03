# How to Run the Project in VS Code

## 📋 Prerequisites

- VS Code installed
- Python 3.12+ installed
- Node.js 18+ installed
- MongoDB running (local or Atlas)

## 🚀 Quick Start Guide

### Step 1: Open Project in VS Code

1. Open VS Code
2. Click **File** → **Open Folder**
3. Navigate to: `C:\Users\admin\Documents\resume-parser-job-matcher`
4. Click **Select Folder**

### Step 2: Open Terminal in VS Code

**Method 1:**
- Press `` Ctrl + ` `` (backtick key) to open terminal

**Method 2:**
- Click **Terminal** → **New Terminal** from menu

**Method 3:**
- Click **View** → **Terminal**

### Step 3: Run Backend Server

1. **Open a new terminal** (click the `+` button or press `` Ctrl + Shift + ` ``)

2. **Navigate to backend folder:**
   ```powershell
   cd backend
   ```

3. **Activate virtual environment:**
   ```powershell
   ..\venv\Scripts\Activate.ps1
   ```

4. **Start Flask server:**
   ```powershell
   python app.py
   ```

5. **You should see:**
   ```
   * Running on http://0.0.0.0:5000
   * Debug mode: on
   ```

6. **Keep this terminal open!** (Don't close it)

### Step 4: Run Frontend Server

1. **Open another new terminal** (click the `+` button again)

2. **Navigate to frontend folder:**
   ```powershell
   cd frontend
   ```

3. **Start React development server:**
   ```powershell
   npm start
   ```

4. **Wait for compilation** (30-60 seconds first time)

5. **Browser should open automatically** at `http://localhost:3000`

6. **Keep this terminal open too!**

## 🎯 Running Both Servers (Recommended Method)

### Using VS Code's Split Terminal

1. Open one terminal (`` Ctrl + ` ``)

2. **Split terminal** (click split icon or `` Ctrl + Shift + 5 ``)

3. **Left terminal - Backend:**
   ```powershell
   cd backend
   ..\venv\Scripts\Activate.ps1
   python app.py
   ```

4. **Right terminal - Frontend:**
   ```powershell
   cd frontend
   npm start
   ```

## 🔧 VS Code Extensions (Recommended)

Install these extensions for better experience:

1. **Python** (by Microsoft)
   - Python language support
   - Debugging
   - Linting

2. **ES7+ React/Redux/React-Native snippets**
   - React code snippets

3. **Prettier - Code formatter**
   - Auto-format code

4. **ESLint**
   - JavaScript linting

5. **MongoDB for VS Code**
   - MongoDB database tools

## 🐛 Debugging in VS Code

### Debug Backend (Flask)

1. **Create `.vscode/launch.json`** (if it doesn't exist):
   ```json
   {
     "version": "0.2.0",
     "configurations": [
       {
         "name": "Python: Flask",
         "type": "python",
         "request": "launch",
         "program": "${workspaceFolder}/backend/app.py",
         "console": "integratedTerminal",
         "env": {
           "FLASK_APP": "app.py",
           "FLASK_ENV": "development"
         },
         "jinja": true
       }
     ]
   }
   ```

2. **Set breakpoints** in your Python code (click left of line number)

3. **Press F5** or click **Run and Debug** → **Python: Flask**

### Debug Frontend (React)

1. **Install Chrome Debugger extension** (if not installed)

2. **Add to `.vscode/launch.json`:**
   ```json
   {
     "version": "0.2.0",
     "configurations": [
       {
         "name": "Chrome: React",
         "type": "chrome",
         "request": "launch",
         "url": "http://localhost:3000",
         "webRoot": "${workspaceFolder}/frontend/src"
       }
     ]
   }
   ```

3. **Start frontend** (`npm start`)

4. **Press F5** to debug

## 📁 Project Structure in VS Code

```
resume-parser-job-matcher/
├── .vscode/              # VS Code settings
├── backend/              # Flask backend
│   ├── app.py           # Main Flask app
│   ├── routes/          # API routes
│   ├── services/        # Business logic
│   └── models/          # Database models
├── frontend/            # React frontend
│   ├── src/
│   │   ├── components/  # React components
│   │   └── services/   # API services
│   └── public/
└── venv/                # Python virtual environment
```

## ⚡ Quick Commands

### Terminal Shortcuts

- `` Ctrl + ` `` - Toggle terminal
- `` Ctrl + Shift + ` `` - New terminal
- `` Ctrl + Shift + 5 `` - Split terminal
- `` Ctrl + K `` then `` Ctrl + 0 `` - Close all terminals

### Useful VS Code Shortcuts

- `Ctrl + P` - Quick file open
- `Ctrl + Shift + P` - Command palette
- `F5` - Start debugging
- `Ctrl + F5` - Run without debugging
- `F9` - Toggle breakpoint
- `F12` - Go to definition

## 🔍 Troubleshooting

### Backend Not Starting

**Problem:** `ModuleNotFoundError` or import errors

**Solution:**
1. Make sure virtual environment is activated
2. Check you're in `backend` folder
3. Verify packages: `pip list`

### Frontend Not Starting

**Problem:** Port 3000 already in use

**Solution:**
```powershell
# Find process using port 3000
netstat -ano | findstr :3000

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

### MongoDB Connection Error

**Problem:** Database connection failed

**Solution:**
1. Check if MongoDB is running
2. Verify connection string in `backend/config.py`
3. For MongoDB Atlas, check your connection string

### CORS Errors

**Problem:** Frontend can't connect to backend

**Solution:**
1. Make sure backend is running on port 5000
2. Check `backend/config.py` CORS settings
3. Verify both servers are running

## 📝 VS Code Settings (Optional)

Create `.vscode/settings.json`:

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/venv/Scripts/python.exe",
  "python.terminal.activateEnvironment": true,
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll": true
  },
  "files.exclude": {
    "**/__pycache__": true,
    "**/*.pyc": true,
    "**/node_modules": true
  }
}
```

## 🎯 Step-by-Step Checklist

- [ ] Open project in VS Code
- [ ] Open terminal (`` Ctrl + ` ``)
- [ ] Split terminal (optional)
- [ ] Terminal 1: Activate venv and run backend
- [ ] Terminal 2: Run frontend (`npm start`)
- [ ] Wait for both to start
- [ ] Open browser to `http://localhost:3000`
- [ ] Test the application!

## 💡 Pro Tips

1. **Use Integrated Terminal**: VS Code's terminal is integrated and convenient

2. **Multiple Terminals**: You can have multiple terminals open for different tasks

3. **Terminal Names**: Right-click terminal tab → Rename (e.g., "Backend", "Frontend")

4. **Auto-save**: Enable auto-save (File → Auto Save) to see changes immediately

5. **Git Integration**: VS Code has built-in Git support - use it!

6. **Extensions**: Install recommended extensions for better development experience

---

**You're all set! Happy coding in VS Code!** 🚀

