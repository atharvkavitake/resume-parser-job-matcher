# How to Run the Application

## Prerequisites
- Python 3.12+ installed
- Node.js 18+ installed
- MongoDB running (local or Atlas)

## Step 1: Start MongoDB
Make sure MongoDB is running on your system:
- **Windows**: MongoDB should be running as a service
- **Mac/Linux**: Run `mongod` or start MongoDB service
- **Cloud**: If using MongoDB Atlas, update `MONGODB_URI` in `backend/config.py`

## Step 2: Start Backend (Flask)

Open Terminal 1:
```powershell
# Navigate to project root
cd C:\Users\admin\Documents\resume-parser-job-matcher

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Navigate to backend
cd backend

# Start Flask server
python app.py
```

Backend will run on: `http://localhost:5000`

## Step 3: Start Frontend (React)

Open Terminal 2:
```powershell
# Navigate to frontend directory
cd C:\Users\admin\Documents\resume-parser-job-matcher\frontend

# Install dependencies (first time only)
npm install

# Start React development server
npm start
```

Frontend will run on: `http://localhost:3000`

## Step 4: Use the Application

1. Open browser: `http://localhost:3000`
2. **Upload Tab**: Upload resumes (PDF/DOCX) and job descriptions
3. **Match Tab**: Match resumes with jobs and see results
4. **Resumes Tab**: View all uploaded resumes

## API Endpoints

Backend API is available at: `http://localhost:5000/api`

- `GET /` - Health check
- `POST /api/upload-resume` - Upload resume
- `GET /api/resumes` - Get all resumes
- `POST /api/upload-job` - Upload job
- `GET /api/jobs` - Get all jobs
- `POST /api/match` - Match resume with job
- `POST /api/skill-gap` - Get skill gap analysis

## Troubleshooting

### MongoDB Connection Error
- Make sure MongoDB is running
- Check `backend/config.py` for correct `MONGODB_URI`
- For MongoDB Atlas, update the connection string

### Port Already in Use
- Backend: Change port in `backend/app.py` (line 45)
- Frontend: React will ask to use a different port

### CORS Errors
- Make sure backend is running on port 5000
- Check `backend/config.py` CORS_ORIGINS setting

