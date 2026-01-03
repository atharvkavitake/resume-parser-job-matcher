# Troubleshooting Guide

## "Failed to fetch" Error

If you see "Failed to fetch" errors when uploading resumes or jobs, it means the **backend server is not running**.

### Solution 1: Start Backend Manually (Recommended)

1. **Open a new PowerShell or Command Prompt window**

2. **Navigate to the project directory:**
   ```powershell
   cd C:\Users\admin\Documents\resume-parser-job-matcher
   ```

3. **Activate the virtual environment:**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

4. **Navigate to backend folder:**
   ```powershell
   cd backend
   ```

5. **Start the Flask server:**
   ```powershell
   python app.py
   ```

6. **You should see:**
   ```
   * Running on http://0.0.0.0:5000
   * Debug mode: on
   ```

7. **Keep this window open** - the backend must stay running!

### Solution 2: Use the Start Scripts

**Option A - PowerShell:**
```powershell
.\start_backend.ps1
```

**Option B - Batch file:**
```cmd
start_backend.bat
```

### Solution 3: Check if Backend is Running

Open a browser and go to: **http://localhost:5000**

You should see:
```json
{
  "message": "Backend API is running",
  "status": "ok",
  "database": "connected"
}
```

If you see this, the backend is running correctly!

## Common Issues

### Issue 1: MongoDB Not Connected

**Error:** Database shows as "disconnected"

**Solution:**
- Make sure MongoDB is installed and running
- Or use MongoDB Atlas (cloud) and update `MONGODB_URI` in `backend/config.py`

### Issue 2: Port Already in Use

**Error:** `Address already in use`

**Solution:**
- Find and close the process using port 5000
- Or change the port in `backend/app.py` (line 71)

### Issue 3: Import Errors

**Error:** `ModuleNotFoundError` or `ImportError`

**Solution:**
1. Make sure virtual environment is activated
2. Install dependencies:
   ```powershell
   cd backend
   pip install -r requirements.txt
   ```

### Issue 4: CORS Errors

**Error:** CORS policy blocking requests

**Solution:**
- The CORS configuration has been updated to allow all origins in development
- Make sure both servers are running:
  - Backend: http://localhost:5000
  - Frontend: http://localhost:3000

## Quick Checklist

- [ ] Backend server is running (check http://localhost:5000)
- [ ] Frontend server is running (check http://localhost:3000)
- [ ] MongoDB is running (or using MongoDB Atlas)
- [ ] Virtual environment is activated
- [ ] All dependencies are installed
- [ ] No error messages in the backend console

## Still Having Issues?

1. **Check the backend console** for error messages
2. **Check the browser console** (F12) for detailed error messages
3. **Verify both servers are running:**
   - Backend: http://localhost:5000
   - Frontend: http://localhost:3000

## Need Help?

Check the following files:
- `QUICK_START.md` - Quick reference
- `PROJECT_COMPLETE.md` - Complete project documentation
- `README.md` - Project overview

