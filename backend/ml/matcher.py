"""
Job-Resume matching using TF-IDF
Calculates similarity scores between resumes and jobs
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def calculate_match_score(resume_text: str, job_description: str) -> float:
    """
    Calculate matching score between resume and job using TF-IDF
    
    Args:
        resume_text (str): Resume text
        job_description (str): Job description text
        
    Returns:
        float: Match score between 0 and 1
    """
    if not resume_text or not job_description:
        return 0.0
    
    # Combine texts
    texts = [resume_text.lower(), job_description.lower()]
    
    # Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer(
        max_features=1000,
        stop_words='english',
        ngram_range=(1, 2)  # Unigrams and bigrams
    )
    
    try:
        # Transform texts to TF-IDF vectors
        tfidf_matrix = vectorizer.fit_transform(texts)
        
        # Calculate cosine similarity
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        
        return float(similarity)
    except Exception as e:
        print(f"Error calculating match score: {e}")
        return 0.0

def calculate_skill_match(resume_skills: list, job_required_skills: list, job_preferred_skills: list = None) -> dict:
    """
    Calculate skill matching between resume and job
    
    Args:
        resume_skills (list): Skills from resume
        job_required_skills (list): Required skills for job
        job_preferred_skills (list): Preferred skills for job
        
    Returns:
        dict: Matching statistics
    """
    if not resume_skills:
        resume_skills = []
    if not job_required_skills:
        job_required_skills = []
    if not job_preferred_skills:
        job_preferred_skills = []
    
    # Normalize skills to lowercase for comparison
    resume_skills_lower = [s.lower().strip() for s in resume_skills]
    required_skills_lower = [s.lower().strip() for s in job_required_skills]
    preferred_skills_lower = [s.lower().strip() for s in job_preferred_skills]
    
    # Find matching skills
    matching_required = [s for s in required_skills_lower if s in resume_skills_lower]
    matching_preferred = [s for s in preferred_skills_lower if s in resume_skills_lower]
    missing_required = [s for s in required_skills_lower if s not in resume_skills_lower]
    
    # Calculate scores
    required_match_score = len(matching_required) / len(required_skills_lower) if required_skills_lower else 1.0
    preferred_match_score = len(matching_preferred) / len(preferred_skills_lower) if preferred_skills_lower else 0.0
    
    # Overall skill score (70% required, 30% preferred)
    overall_skill_score = (required_match_score * 0.7) + (preferred_match_score * 0.3)
    
    return {
        'matching_required_skills': [s.title() for s in matching_required],
        'matching_preferred_skills': [s.title() for s in matching_preferred],
        'missing_required_skills': [s.title() for s in missing_required],
        'required_match_percentage': round(required_match_score * 100, 2),
        'preferred_match_percentage': round(preferred_match_score * 100, 2),
        'overall_skill_score': round(overall_skill_score, 2)
    }

def match_resume_to_job(resume_data: dict, job_data: dict) -> dict:
    """
    Match a resume to a job and return comprehensive matching results
    
    Args:
        resume_data (dict): Resume data from database
        job_data (dict): Job data from database
        
    Returns:
        dict: Complete matching results
    """
    # Get texts for TF-IDF matching
    resume_text = resume_data.get('raw_text', '')
    if not resume_text:
        # Build text from structured data
        resume_text = ' '.join([
            resume_data.get('name', ''),
            ' '.join(resume_data.get('skills', [])),
            ' '.join([exp.get('title', '') + ' ' + exp.get('company', '') for exp in resume_data.get('experience', [])])
        ])
    
    job_description = job_data.get('description', '')
    
    # Calculate TF-IDF similarity
    tfidf_score = calculate_match_score(resume_text, job_description)
    
    # Calculate skill matching
    resume_skills = resume_data.get('skills', [])
    job_required = job_data.get('required_skills', [])
    job_preferred = job_data.get('preferred_skills', [])
    
    skill_match = calculate_skill_match(resume_skills, job_required, job_preferred)
    
    # Calculate overall match score (60% TF-IDF, 40% skills)
    overall_score = (tfidf_score * 0.6) + (skill_match['overall_skill_score'] / 100 * 0.4)
    
    return {
        'resume_id': str(resume_data.get('_id', '')),
        'job_id': str(job_data.get('_id', '')),
        'resume_name': resume_data.get('name', 'Unknown'),
        'job_title': job_data.get('title', 'Unknown'),
        'tfidf_score': round(tfidf_score * 100, 2),
        'skill_match': skill_match,
        'overall_match_score': round(overall_score * 100, 2),
        'match_percentage': round(overall_score * 100, 2)
    }

