"""
Test script for MongoDB connection and models
Run this to verify everything works
"""

from db.connection import connect_db, is_connected, get_db
from models.resume_model import Resume
from models.job_model import Job
from datetime import datetime

def test_connection():
    """Test MongoDB connection"""
    print("=" * 50)
    print("Testing MongoDB Connection")
    print("=" * 50)
    
    if connect_db():
        print("[OK] MongoDB connection successful!")
        print(f"[OK] Database: {get_db().name}")
        return True
    else:
        print("[ERROR] MongoDB connection failed!")
        print("\nTroubleshooting:")
        print("   1. Make sure MongoDB is installed and running")
        print("   2. Check if MongoDB service is started")
        print("   3. Or use MongoDB Atlas (cloud) and update MONGODB_URI in config.py")
        return False

def test_resume_model():
    """Test Resume model"""
    print("\n" + "=" * 50)
    print("Testing Resume Model")
    print("=" * 50)
    
    if not is_connected():
        print("[ERROR] Database not connected. Skipping model test.")
        return False
    
    # Create a test resume
    test_resume_data = {
        'filename': 'test_resume.pdf',
        'file_path': 'uploads/test_resume.pdf',
        'raw_text': 'John Doe\nSoftware Engineer\nPython, JavaScript',
        'name': 'John Doe',
        'email': 'john@example.com',
        'skills': ['Python', 'JavaScript', 'Flask'],
        'experience': [
            {
                'title': 'Software Engineer',
                'company': 'Tech Corp',
                'duration': '2020-2024'
            }
        ],
        'education': [
            {
                'degree': 'BS Computer Science',
                'university': 'State University',
                'year': '2020'
            }
        ]
    }
    
    try:
        resume = Resume(test_resume_data)
        resume_id = resume.save()
        print(f"[OK] Resume saved with ID: {resume_id}")
        
        # Test finding resume
        found_resume = Resume.find_by_id(resume_id)
        if found_resume:
            print(f"[OK] Resume found: {found_resume.get('name', 'N/A')}")
        
        # Test getting all resumes
        all_resumes = Resume.find_all()
        print(f"[OK] Total resumes in database: {len(all_resumes)}")
        
        # Clean up - delete test resume
        Resume.delete_by_id(resume_id)
        print(f"[OK] Test resume deleted")
        
        return True
    except Exception as e:
        print(f"[ERROR] Error testing Resume model: {e}")
        return False

def test_job_model():
    """Test Job model"""
    print("\n" + "=" * 50)
    print("Testing Job Model")
    print("=" * 50)
    
    if not is_connected():
        print("[ERROR] Database not connected. Skipping model test.")
        return False
    
    # Create a test job
    test_job_data = {
        'title': 'Senior Software Engineer',
        'company': 'Tech Company',
        'description': 'We are looking for a senior software engineer...',
        'required_skills': ['Python', 'JavaScript', 'React'],
        'preferred_skills': ['MongoDB', 'Docker'],
        'experience_required': 5,
        'location': 'Remote'
    }
    
    try:
        job = Job(test_job_data)
        job_id = job.save()
        print(f"[OK] Job saved with ID: {job_id}")
        
        # Test finding job
        found_job = Job.find_by_id(job_id)
        if found_job:
            print(f"[OK] Job found: {found_job.get('title', 'N/A')}")
        
        # Test getting all jobs
        all_jobs = Job.find_all()
        print(f"[OK] Total jobs in database: {len(all_jobs)}")
        
        # Clean up - delete test job
        Job.delete_by_id(job_id)
        print(f"[OK] Test job deleted")
        
        return True
    except Exception as e:
        print(f"[ERROR] Error testing Job model: {e}")
        return False

if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("Starting Database Tests")
    print("=" * 50 + "\n")
    
    # Test connection
    if test_connection():
        # Test models
        test_resume_model()
        test_job_model()
        
        print("\n" + "=" * 50)
        print("[OK] All tests completed!")
        print("=" * 50)
    else:
        print("\n[WARNING] Please fix MongoDB connection before testing models")

