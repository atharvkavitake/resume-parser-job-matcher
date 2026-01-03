# Quick Start Guide

## 🚀 Application is Running!

### Backend Server
- **URL**: http://localhost:5000
- **Status**: Running in background
- **API Endpoints**: 
  - `GET /` - Health check
  - `POST /api/upload-resume` - Upload resume
  - `POST /api/upload-job` - Upload job
  - `POST /api/match` - Match resume to job
  - `GET /api/resumes` - Get all resumes
  - `GET /api/jobs` - Get all jobs

### Frontend Server
- **URL**: http://localhost:3000
- **Status**: Running in background
- **Browser**: Should open automatically

## 📋 How to Use

1. **Upload a Resume**
   - Click "Choose File" in the Resume Upload section
   - Select a PDF or DOCX file
   - Click "Upload Resume"
   - The system will automatically parse and extract:
     - Name, email, phone
     - Skills
     - Work experience
     - Education

2. **Upload a Job Description**
   - Fill in the job form:
     - Job Title (required)
     - Company
     - Description (required)
     - Required Skills (comma-separated)
     - Preferred Skills (comma-separated)
     - Experience Required
     - Location
   - Click "Upload Job"

3. **Match Resume to Job**
   - Select a resume from the Resume List
   - Select a job from the Job List
   - Click "Match Resume to Job"
   - View detailed match results including:
     - Overall match score
     - TF-IDF similarity score
     - Skill matching analysis
     - Skill gap analysis with recommendations

## 🛠️ Troubleshooting

### Backend not running?
```powershell
cd backend
python app.py
```

### Frontend not running?
```powershell
cd frontend
npm start
```

### MongoDB not connected?
- Make sure MongoDB is installed and running
- Or use MongoDB Atlas (cloud) and update `MONGODB_URI` in `backend/config.py`

### CORS errors?
- Make sure backend is running on port 5000
- Make sure frontend is running on port 3000
- Check `backend/config.py` CORS_ORIGINS setting

## 📁 Project Structure

```
resume-parser-job-matcher/
├── backend/          # Flask API
│   ├── app.py        # Main application
│   ├── routes/       # API endpoints
│   ├── models/       # Database models
│   ├── services/     # Business logic
│   ├── nlp/          # NLP processing
│   └── ml/           # ML matching
├── frontend/         # React UI
│   ├── src/
│   │   ├── components/
│   │   └── services/
│   └── public/
└── venv/             # Python virtual environment
```

## 🎯 Features

✅ Upload and parse resumes (PDF/DOCX)
✅ Extract skills, experience, education using NLP
✅ Upload job descriptions
✅ Match resumes with jobs using TF-IDF
✅ Calculate matching scores
✅ Show missing skills (skill gap analysis)
✅ Rank candidates
✅ REST API backend
✅ React frontend UI

## 🔧 Technology Stack

- **Backend**: Python, Flask, MongoDB, spaCy, scikit-learn
- **Frontend**: React, Axios
- **ML/NLP**: TF-IDF, spaCy NLP

---

**Enjoy using the Resume Parser & Job Matcher!** 🎉

