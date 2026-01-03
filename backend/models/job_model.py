"""
Job database model
Defines the structure for storing job description data in MongoDB
"""

from datetime import datetime
from bson import ObjectId
from db.connection import get_db

class Job:
    """
    Job model - represents a job description document
    """
    
    COLLECTION_NAME = "jobs"
    
    def __init__(self, data):
        """
        Initialize a Job object
        
        Args:
            data (dict): Job data including:
                - title: Job title
                - company: Company name
                - description: Full job description text
                - required_skills: List of required skills
                - preferred_skills: List of preferred skills
                - experience_required: Years of experience required
                - location: Job location
                - created_at: Timestamp
        """
        self.data = data
        self.data['created_at'] = data.get('created_at', datetime.utcnow())
        self.data['updated_at'] = datetime.utcnow()
    
    def save(self):
        """
        Save job to MongoDB
        Returns the inserted document ID
        """
        db = get_db()
        if db is None:
            raise Exception("Database not connected")
        
        collection = db[self.COLLECTION_NAME]
        result = collection.insert_one(self.data)
        return result.inserted_id
    
    @staticmethod
    def find_by_id(job_id):
        """
        Find a job by its ID
        """
        db = get_db()
        if db is None:
            return None
        
        # Convert string ID to ObjectId if needed
        if isinstance(job_id, str):
            try:
                job_id = ObjectId(job_id)
            except:
                return None
        
        collection = db[Job.COLLECTION_NAME]
        return collection.find_one({'_id': job_id})
    
    @staticmethod
    def find_all():
        """
        Get all jobs
        """
        db = get_db()
        if db is None:
            return []
        
        collection = db[Job.COLLECTION_NAME]
        return list(collection.find().sort('created_at', -1))  # Newest first
    
    @staticmethod
    def delete_by_id(job_id):
        """
        Delete a job by its ID
        """
        db = get_db()
        if db is None:
            return False
        
        # Convert string ID to ObjectId if needed
        if isinstance(job_id, str):
            try:
                job_id = ObjectId(job_id)
            except:
                return False
        
        collection = db[Job.COLLECTION_NAME]
        result = collection.delete_one({'_id': job_id})
        return result.deleted_count > 0
    
    def to_dict(self):
        """
        Convert job to dictionary (for JSON serialization)
        """
        result = self.data.copy()
        if '_id' in result:
            result['_id'] = str(result['_id'])  # Convert ObjectId to string
        return result

