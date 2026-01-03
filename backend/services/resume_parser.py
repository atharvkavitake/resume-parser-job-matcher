"""
Resume parsing service
Combines file extraction and NLP parsing
"""

import os
from utils.file_handler import extract_text
from nlp.text_extractor import parse_resume_text
from models.resume_model import Resume

def parse_resume_file(file_path: str, filename: str) -> dict:
    """
    Parse a resume file (PDF or DOCX)
    
    Args:
        file_path (str): Path to the uploaded file
        filename (str): Original filename
        
    Returns:
        dict: Parsed resume data with database ID
    """
    try:
        # Extract text from file
        raw_text = extract_text(file_path)
        
        if not raw_text or len(raw_text.strip()) < 50:
            raise ValueError("Could not extract sufficient text from file")
        
        # Parse text using NLP
        parsed_data = parse_resume_text(raw_text)
        
        # Add file information
        parsed_data['filename'] = filename
        parsed_data['file_path'] = file_path
        
        # Save to database
        resume = Resume(parsed_data)
        resume_id = resume.save()
        
        # Return complete resume data
        resume_doc = Resume.find_by_id(resume_id)
        if resume_doc:
            resume_obj = Resume(resume_doc)
            return resume_obj.to_dict()
        
        return parsed_data
        
    except Exception as e:
        raise Exception(f"Error parsing resume: {str(e)}")

