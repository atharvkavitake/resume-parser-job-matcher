# STEP 2: Installing Python Dependencies & Backend Setup

## What We're Doing

In this step, we will:
1. Install all Python packages needed for the backend
2. Download spaCy language model (for NLP)
3. Test that Flask backend runs correctly
4. Verify all packages are installed

## Why We Need These Packages

### Flask & flask-cors
- **Flask**: Our web framework (creates REST API)
- **flask-cors**: Allows React frontend to call our backend (CORS = Cross-Origin Resource Sharing)

### pymongo
- **MongoDB driver**: Connects Python to MongoDB database
- **Why**: We'll store resumes and jobs in MongoDB

### PyPDF2 & python-docx
- **PyPDF2**: Extracts text from PDF files
- **python-docx**: Extracts text from Word documents (.docx)
- **Why**: Resumes come in PDF or DOCX format

### spaCy
- **NLP library**: Natural Language Processing
- **Why**: Extract skills, experience, education from resume text

### scikit-learn
- **ML library**: Machine learning algorithms
- **Why**: TF-IDF algorithm for matching resumes with jobs

### numpy
- **Math library**: Numerical computing
- **Why**: Required by scikit-learn and spaCy

### python-dotenv
- **Environment variables**: Loads .env files
- **Why**: Store sensitive data (database passwords, API keys) securely

## Installation Steps

1. ✅ Activate virtual environment
2. ✅ Install packages from requirements.txt
3. ✅ Download spaCy English model
4. ✅ Test Flask backend
5. ✅ Verify all packages work

---

## What Was Installed

### Core Packages
- ✅ **Flask 3.1.2** - Web framework
- ✅ **flask-cors 6.0.2** - CORS support
- ✅ **pymongo 4.10.1** - MongoDB driver
- ✅ **PyPDF2 3.0.1** - PDF text extraction
- ✅ **python-docx 1.1.2** - Word document processing
- ✅ **spacy 3.8.2** - NLP library
- ✅ **scikit-learn 1.5.2** - Machine learning
- ✅ **numpy 2.1.1** - Numerical computing
- ✅ **python-dotenv 1.0.1** - Environment variables

### spaCy Model
- ✅ **en_core_web_sm 3.8.0** - English language model (12.8 MB)

### Verification
- ✅ All packages import successfully
- ✅ spaCy model loads correctly
- ✅ Flask app imports without errors

---

**Status:** ✅ STEP 2 COMPLETE - All dependencies installed!

