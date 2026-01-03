"""
Resume database model
Defines the structure for storing resume data in MongoDB
"""

from datetime import datetime
from bson import ObjectId
from db.connection import get_db

class Resume:
    """
    Resume model - represents a parsed resume document
    """
    
    COLLECTION_NAME = "resumes"
    
    def __init__(self, data):
        """
        Initialize a Resume object
        
        Args:
            data (dict): Resume data including:
                - filename: Original file name
                - file_path: Path to uploaded file
                - raw_text: Extracted text from resume
                - name: Candidate name (extracted)
                - email: Candidate email (extracted)
                - phone: Candidate phone (extracted)
                - skills: List of skills (extracted)
                - experience: List of work experience
                - education: List of education entries
                - created_at: Timestamp
        """
        self.data = data
        self.data['created_at'] = data.get('created_at', datetime.utcnow())
        self.data['updated_at'] = datetime.utcnow()
    
    def save(self):
        """
        Save resume to MongoDB
        Returns the inserted document ID
        """
        db = get_db()
        if db is None:
            raise Exception("Database not connected")
        
        collection = db[self.COLLECTION_NAME]
        result = collection.insert_one(self.data)
        return result.inserted_id
    
    @staticmethod
    def find_by_id(resume_id):
        """
        Find a resume by its ID
        """
        db = get_db()
        if db is None:
            return None
        
        # Convert string ID to ObjectId if needed
        if isinstance(resume_id, str):
            try:
                resume_id = ObjectId(resume_id)
            except:
                return None
        
        collection = db[Resume.COLLECTION_NAME]
        return collection.find_one({'_id': resume_id})
    
    @staticmethod
    def find_all():
        """
        Get all resumes
        """
        db = get_db()
        if db is None:
            return []
        
        collection = db[Resume.COLLECTION_NAME]
        return list(collection.find().sort('created_at', -1))  # Newest first
    
    @staticmethod
    def delete_by_id(resume_id):
        """
        Delete a resume by its ID
        """
        db = get_db()
        if db is None:
            return False
        
        # Convert string ID to ObjectId if needed
        if isinstance(resume_id, str):
            try:
                resume_id = ObjectId(resume_id)
            except:
                return False
        
        collection = db[Resume.COLLECTION_NAME]
        result = collection.delete_one({'_id': resume_id})
        return result.deleted_count > 0
    
    def to_dict(self):
        """
        Convert resume to dictionary (for JSON serialization)
        """
        result = self.data.copy()
        if '_id' in result:
            result['_id'] = str(result['_id'])  # Convert ObjectId to string
        return result

