# STEP 0: Environment Setup - COMPLETE ✅

## What We Did

### 1. ✅ Verified Python Installation
- **Command:** `python --version`
- **Result:** Python 3.12.4 is installed
- **Why:** Python is our backend language for Flask

### 2. ✅ Verified Node.js Installation
- **Command:** `node --version`
- **Result:** Node.js v24.12.0 is installed
- **Why:** Node.js is needed to run React (our frontend framework)

### 3. ✅ Verified npm Installation
- **Command:** `npm --version`
- **Result:** npm 11.6.2 is installed
- **Why:** npm is the package manager for Node.js (like pip for Python)

### 4. ✅ Created Virtual Environment
- **Command:** `python -m venv venv`
- **Location:** `venv/` folder at project root
- **Why:** 
  - Keeps project dependencies isolated
  - Prevents conflicts between different projects
  - Makes the project portable and reproducible

### 5. ✅ Activated Virtual Environment
- **Command (PowerShell):** `.\venv\Scripts\Activate.ps1`
- **Command (Command Prompt):** `venv\Scripts\activate.bat`
- **Command (Git Bash):** `source venv/Scripts/activate`
- **How to know it's active:** You'll see `(venv)` at the start of your terminal prompt
- **Why:** Only when activated, Python will use packages installed in this venv

### 6. ✅ Upgraded pip
- **Command:** `python -m pip install --upgrade pip`
- **Result:** pip upgraded from 24.0 to 25.3
- **Why:** Latest pip ensures we can install all packages without issues

## Important Notes

### Virtual Environment Activation
**Every time you open a new terminal to work on this project, you MUST activate the virtual environment first!**

```powershell
# In PowerShell (Windows)
.\venv\Scripts\Activate.ps1
```

### Deactivating Virtual Environment
When you're done working, you can deactivate:
```powershell
deactivate
```

### VS Code Setup (Optional but Recommended)
1. Open VS Code in this project folder
2. Install the Python extension (if not already installed)
3. VS Code should automatically detect the virtual environment
4. Select the Python interpreter: `Ctrl+Shift+P` → "Python: Select Interpreter" → Choose `.\venv\Scripts\python.exe`

## What's Next?

Once you confirm "done", we'll move to:
- **STEP 1:** Project folder structure
- Setting up proper directories for backend and frontend
- Creating initial configuration files

## Checklist

- [x] Python installed and verified
- [x] Node.js installed and verified
- [x] npm installed and verified
- [x] Virtual environment created
- [x] Virtual environment activated
- [x] pip upgraded
- [x] .gitignore created (to exclude venv from git)

---

**Status:** ✅ STEP 0 COMPLETE - Ready for STEP 1!


