# Automated Resume Parser & Job Matcher

An end-to-end application that parses resumes, extracts skills and experience, and matches them with job descriptions using NLP and machine learning.

## Features

- 📄 Upload and parse resumes (PDF/DOCX)
- 🔍 Extract skills, experience, and education using NLP
- 💼 Upload job descriptions
- 🎯 Match resumes with jobs using TF-IDF
- 📊 Calculate matching scores
- 🔎 Show missing skills (skill gap analysis)
- 📈 Rank candidates
- 🌐 REST API backend
- ⚛️ React frontend UI

## Tech Stack

### Backend
- Python 3.12
- Flask (with Blueprints)
- MongoDB
- spaCy (NLP)
- scikit-learn (TF-IDF)

### Frontend
- React
- Axios

## Project Structure

```
resume-parser-job-matcher/
├── backend/          # Flask backend
├── frontend/         # React frontend
└── venv/            # Virtual environment
```

## Setup Instructions

### Prerequisites
- Python 3.12+
- Node.js 18+
- MongoDB (local or cloud)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd resume-parser-job-matcher
   ```

2. **Set up Python backend**
   ```bash
   # Activate virtual environment
   .\venv\Scripts\Activate.ps1  # Windows PowerShell
   
   # Install dependencies
   cd backend
   pip install -r requirements.txt
   ```

3. **Set up React frontend**
   ```bash
   cd frontend
   npm install
   ```

4. **Run the application**
   ```bash
   # Terminal 1: Backend
   cd backend
   python app.py
   
   # Terminal 2: Frontend
   cd frontend
   npm start
   ```

## API Endpoints

- `GET /` - Health check
- `POST /api/upload-resume` - Upload resume
- `POST /api/upload-job` - Upload job description
- `POST /api/match` - Match resume with job
- `GET /api/resumes` - Get all resumes
- `GET /api/jobs` - Get all jobs

## Development Status

🚧 **In Development** - Following step-by-step tutorial

## License

MIT


