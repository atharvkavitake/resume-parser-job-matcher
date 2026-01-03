# STEP 1: Project Folder Structure

## Why We Need This Structure

A well-organized folder structure makes your project:
- **Maintainable**: Easy to find and update code
- **Scalable**: Easy to add new features
- **Professional**: Industry-standard organization
- **Deployable**: Clear separation of backend and frontend

## Our Project Structure

```
resume-parser-job-matcher/
├── backend/                 # Python Flask backend
│   ├── app.py              # Main Flask application
│   ├── config.py           # Configuration settings
│   ├── routes/             # API routes (Flask Blueprints)
│   │   ├── __init__.py
│   │   ├── resume_routes.py
│   │   └── job_routes.py
│   ├── models/             # Database models
│   │   ├── __init__.py
│   │   └── resume_model.py
│   ├── services/           # Business logic
│   │   ├── __init__.py
│   │   ├── resume_parser.py
│   │   ├── job_matcher.py
│   │   └── skill_gap.py
│   ├── nlp/                # NLP processing
│   │   ├── __init__.py
│   │   └── text_extractor.py
│   ├── ml/                 # Machine learning
│   │   ├── __init__.py
│   │   └── matcher.py
│   ├── utils/              # Helper functions
│   │   ├── __init__.py
│   │   └── file_handler.py
│   ├── uploads/            # Uploaded files (PDFs, DOCX)
│   └── requirements.txt    # Python dependencies
│
├── frontend/               # React frontend
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   ├── App.js
│   │   └── index.js
│   ├── package.json
│   └── package-lock.json
│
├── venv/                   # Virtual environment (at root!)
├── .gitignore
├── README.md
└── STEP_0_GUIDE.md
```

## Folder Explanations

### Backend Structure

**routes/**: Contains Flask Blueprints (organized API endpoints)
- **Why**: Separates different API functionalities
- **Example**: `/api/upload-resume`, `/api/match-job`

**models/**: Database models (MongoDB documents)
- **Why**: Defines data structure
- **Example**: Resume model, Job model

**services/**: Business logic (the "brain" of your app)
- **Why**: Keeps routes clean, reusable code
- **Example**: Parse resume, match skills, calculate scores

**nlp/**: Natural Language Processing
- **Why**: Text extraction and parsing
- **Example**: Extract skills from resume text

**ml/**: Machine Learning
- **Why**: TF-IDF matching algorithm
- **Example**: Calculate similarity scores

**utils/**: Helper functions
- **Why**: Reusable utility functions
- **Example**: File upload handling, text cleaning

### Frontend Structure

**components/**: React components
- **Why**: Reusable UI pieces
- **Example**: UploadForm, MatchResults

**services/**: API calls to backend
- **Why**: Separates API logic from UI
- **Example**: axios calls to Flask backend

## What We're Creating

1. ✅ Proper folder structure
2. ✅ `__init__.py` files (makes folders Python packages)
3. ✅ `requirements.txt` (lists all Python packages)
4. ✅ `package.json` (lists all Node.js packages)
5. ✅ Configuration files
6. ✅ README.md

---

## Files Created in STEP 1

### Backend Files
- ✅ `backend/__init__.py` - Makes backend a Python package
- ✅ `backend/app.py` - Main Flask application (updated)
- ✅ `backend/config.py` - Configuration settings
- ✅ `backend/requirements.txt` - Python dependencies list
- ✅ `backend/routes/__init__.py` - Routes package
- ✅ `backend/routes/resume_routes.py` - Resume API routes (updated)
- ✅ `backend/routes/job_routes.py` - Job API routes (new)
- ✅ `backend/routes/test_routes.py` - Test routes (updated)
- ✅ `backend/models/__init__.py` - Models package
- ✅ `backend/services/__init__.py` - Services package
- ✅ `backend/nlp/__init__.py` - NLP package
- ✅ `backend/ml/__init__.py` - ML package
- ✅ `backend/utils/__init__.py` - Utils package
- ✅ `backend/uploads/.gitkeep` - Uploads folder placeholder

### Frontend Files
- ✅ `frontend/package.json` - Node.js dependencies
- ✅ `frontend/public/index.html` - HTML template
- ✅ `frontend/src/index.js` - React entry point
- ✅ `frontend/src/index.css` - Global styles
- ✅ `frontend/src/App.js` - Main React component
- ✅ `frontend/src/App.css` - App styles
- ✅ `frontend/src/components/` - Components folder (empty, ready for use)
- ✅ `frontend/src/services/` - Services folder (empty, ready for use)

### Documentation
- ✅ `README.md` - Project documentation
- ✅ `STEP_1_GUIDE.md` - This guide

## Key Concepts Explained

### 1. `__init__.py` Files
**What:** Empty Python files in folders
**Why:** Makes folders "Python packages" - allows imports like `from routes import resume_routes`
**Example:** `backend/routes/__init__.py` makes the routes folder importable

### 2. Flask Blueprints
**What:** Way to organize routes into separate files
**Why:** Keeps code organized, scalable, and maintainable
**Example:** 
- `resume_bp` handles all `/api/upload-resume`, `/api/resumes` routes
- `job_bp` handles all `/api/upload-job`, `/api/jobs` routes

### 3. Configuration File (`config.py`)
**What:** Central place for all settings
**Why:** Easy to change settings, different configs for dev/production
**Example:** Database URL, file upload limits, allowed file types

### 4. Application Factory Pattern
**What:** `create_app()` function that creates Flask app
**Why:** Better for testing, multiple app instances, cleaner code
**Example:** See `backend/app.py` - the `create_app()` function

### 5. CORS (Cross-Origin Resource Sharing)
**What:** Allows React frontend (port 3000) to call Flask backend (port 5000)
**Why:** Browsers block requests between different origins (ports) for security
**Example:** `CORS(app, origins=['http://localhost:3000'])`

## What's Next?

In the next steps, we will:
1. Install Python dependencies (`pip install -r requirements.txt`)
2. Set up MongoDB connection
3. Build the resume parser
4. Build the job matcher
5. Create the React frontend

---

**Status:** ✅ STEP 1 COMPLETE - Folder structure ready!

## Important Note

⚠️ **I noticed there's a `venv` folder inside `backend/` - this shouldn't be there!**
- Virtual environments should be at the project root (which we have: `venv/`)
- The one in `backend/venv/` can be deleted - it's not needed
- We're using the root-level `venv/` for the entire project

