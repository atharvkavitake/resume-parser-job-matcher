# STEP 3: MongoDB Setup & Database Models

## What We're Doing

In this step, we will:
1. Set up MongoDB connection
2. Create database models (Resume and Job)
3. Create database utility functions
4. Test the connection

## Why MongoDB?

**MongoDB** is a NoSQL database that stores data as documents (like JSON objects).

**Why we use it:**
- **Flexible**: Resume and job data can have different structures
- **Easy**: No need to define rigid tables like SQL
- **Fast**: Great for storing and querying document data
- **Scalable**: Handles large amounts of data easily

## MongoDB Setup Options

### Option 1: Local MongoDB (Recommended for Learning)
- Install MongoDB on your computer
- Runs on `localhost:27017`
- Free and works offline

### Option 2: MongoDB Atlas (Cloud - Free Tier)
- Free cloud database
- No installation needed
- Accessible from anywhere
- Good for deployment

**For this tutorial, we'll use local MongoDB, but the code works with both!**

## What We'll Create

1. **Database Connection** (`backend/db/connection.py`)
   - Connects to MongoDB
   - Handles connection errors

2. **Resume Model** (`backend/models/resume_model.py`)
   - Stores resume data
   - Fields: name, email, skills, experience, education, etc.

3. **Job Model** (`backend/models/job_model.py`)
   - Stores job description data
   - Fields: title, company, required_skills, description, etc.

4. **Update app.py**
   - Initialize database connection when app starts

---

## Files Created

1. ✅ `backend/db/connection.py` - MongoDB connection handler
2. ✅ `backend/models/resume_model.py` - Resume database model
3. ✅ `backend/models/job_model.py` - Job database model
4. ✅ `backend/test_db.py` - Test script to verify everything works
5. ✅ Updated `backend/app.py` - Initialize database on startup

## Test Results

✅ **MongoDB Connection**: Successfully connected to `resume_matcher_db`
✅ **Resume Model**: Create, read, delete operations working
✅ **Job Model**: Create, read, delete operations working

## Key Concepts Explained

### 1. MongoDB Connection (`db/connection.py`)
- **`connect_db()`**: Establishes connection to MongoDB
- **`get_db()`**: Returns the database instance
- **`is_connected()`**: Checks if database is connected
- **Why**: Centralized connection management, easy to test and maintain

### 2. Resume Model (`models/resume_model.py`)
- **`save()`**: Saves resume to database
- **`find_by_id()`**: Finds resume by ID
- **`find_all()`**: Gets all resumes
- **`delete_by_id()`**: Deletes a resume
- **Why**: Encapsulates database operations, makes code reusable

### 3. Job Model (`models/job_model.py`)
- Same methods as Resume model
- **Why**: Consistent structure, easy to extend

### 4. Database Collections
- **Collections** in MongoDB = Tables in SQL
- `resumes` collection stores all resume documents
- `jobs` collection stores all job documents
- **Why**: Organized data storage, easy to query

---

**Status:** ✅ STEP 3 COMPLETE - MongoDB setup working!

