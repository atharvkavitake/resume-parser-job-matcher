"""
Job Recommendation Service
Analyzes resume and recommends suitable jobs based on keywords and skills
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict
from models.job_model import Job
from models.resume_model import Resume

class JobRecommender:
    """
    Recommends jobs based on resume analysis
    """
    
    @staticmethod
    def recommend_jobs_for_resume(resume_id: str, limit: int = 10) -> List[Dict]:
        """
        Recommend jobs for a given resume
        
        Args:
            resume_id: Resume ID
            limit: Maximum number of recommendations
            
        Returns:
            List of recommended jobs with match scores
        """
        # Get resume data
        resume_doc = Resume.find_by_id(resume_id)
        if not resume_doc:
            return []
        
        # Get all jobs
        all_jobs = Job.find_all()
        if not all_jobs:
            return []
        
        # Build resume text for analysis
        resume_text = JobRecommender._build_resume_text(resume_doc)
        
        # Calculate matches for each job
        recommendations = []
        for job_doc in all_jobs:
            match_result = JobRecommender._calculate_job_match(resume_doc, job_doc, resume_text)
            if match_result:
                recommendations.append(match_result)
        
        # Sort by overall match score (highest first)
        recommendations.sort(key=lambda x: x['overall_match_score'], reverse=True)
        
        # Return top recommendations
        return recommendations[:limit]
    
    @staticmethod
    def _build_resume_text(resume_doc: Dict) -> str:
        """Build comprehensive text from resume for analysis"""
        parts = []
        
        # Add name
        if resume_doc.get('name'):
            parts.append(resume_doc['name'])
        
        # Add skills
        skills = resume_doc.get('skills', [])
        if skills:
            parts.extend(skills)
        
        # Add experience
        experience = resume_doc.get('experience', [])
        for exp in experience:
            if exp.get('title'):
                parts.append(exp['title'])
            if exp.get('company'):
                parts.append(exp['company'])
        
        # Add education
        education = resume_doc.get('education', [])
        for edu in education:
            if edu.get('degree'):
                parts.append(edu['degree'])
            if edu.get('university'):
                parts.append(edu['university'])
        
        # Add raw text
        if resume_doc.get('raw_text'):
            parts.append(resume_doc['raw_text'])
        
        return ' '.join(parts).lower()
    
    @staticmethod
    def _calculate_job_match(resume_doc: Dict, job_doc: Dict, resume_text: str) -> Dict:
        """Calculate how well a job matches the resume"""
        try:
            # Build job text
            job_text = JobRecommender._build_job_text(job_doc)
            
            if not resume_text or not job_text:
                return None
            
            # TF-IDF similarity
            tfidf_score = JobRecommender._calculate_tfidf_similarity(resume_text, job_text)
            
            # Skill matching
            resume_skills = [s.lower().strip() for s in resume_doc.get('skills', [])]
            job_required = [s.lower().strip() for s in job_doc.get('required_skills', [])]
            job_preferred = [s.lower().strip() for s in job_doc.get('preferred_skills', [])]
            
            skill_match = JobRecommender._calculate_skill_match(resume_skills, job_required, job_preferred)
            
            # Experience matching
            experience_match = JobRecommender._calculate_experience_match(resume_doc, job_doc)
            
            # Education matching (if job requires specific education)
            education_match = JobRecommender._calculate_education_match(resume_doc, job_doc)
            
            # Calculate overall score
            # Weighted: TF-IDF (40%), Skills (35%), Experience (15%), Education (10%)
            overall_score = (
                tfidf_score * 0.40 +
                skill_match['overall_score'] * 0.35 +
                experience_match * 0.15 +
                education_match * 0.10
            )
            
            return {
                'job_id': str(job_doc.get('_id', '')),
                'job_title': job_doc.get('title', 'Unknown'),
                'company': job_doc.get('company', 'Unknown'),
                'location': job_doc.get('location', ''),
                'overall_match_score': round(overall_score * 100, 1),
                'tfidf_score': round(tfidf_score * 100, 1),
                'skill_match': skill_match,
                'experience_match': round(experience_match * 100, 1),
                'education_match': round(education_match * 100, 1),
                'match_breakdown': {
                    'tfidf': round(tfidf_score * 100, 1),
                    'skills': round(skill_match['overall_score'] * 100, 1),
                    'experience': round(experience_match * 100, 1),
                    'education': round(education_match * 100, 1)
                },
                'matching_skills': skill_match['matching_skills'],
                'missing_skills': skill_match['missing_skills'],
                'job_description': job_doc.get('description', '')[:200] + '...' if len(job_doc.get('description', '')) > 200 else job_doc.get('description', '')
            }
        except Exception as e:
            print(f"Error calculating job match: {e}")
            return None
    
    @staticmethod
    def _build_job_text(job_doc: Dict) -> str:
        """Build text from job description for analysis"""
        parts = []
        
        if job_doc.get('title'):
            parts.append(job_doc['title'])
        
        if job_doc.get('description'):
            parts.append(job_doc['description'])
        
        skills = job_doc.get('required_skills', []) + job_doc.get('preferred_skills', [])
        if skills:
            parts.extend(skills)
        
        return ' '.join(parts).lower()
    
    @staticmethod
    def _calculate_tfidf_similarity(text1: str, text2: str) -> float:
        """Calculate TF-IDF cosine similarity"""
        try:
            vectorizer = TfidfVectorizer(
                max_features=1000,
                stop_words='english',
                ngram_range=(1, 2)
            )
            
            texts = [text1, text2]
            tfidf_matrix = vectorizer.fit_transform(texts)
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            return float(similarity)
        except:
            return 0.0
    
    @staticmethod
    def _calculate_skill_match(resume_skills: List[str], job_required: List[str], job_preferred: List[str]) -> Dict:
        """Calculate skill matching score"""
        if not resume_skills:
            return {
                'overall_score': 0.0,
                'matching_skills': [],
                'missing_skills': job_required + job_preferred
            }
        
        # Find matching skills
        matching_required = [s for s in job_required if s in resume_skills]
        matching_preferred = [s for s in job_preferred if s in resume_skills]
        missing_required = [s for s in job_required if s not in resume_skills]
        missing_preferred = [s for s in job_preferred if s not in resume_skills]
        
        # Calculate scores
        required_score = len(matching_required) / len(job_required) if job_required else 1.0
        preferred_score = len(matching_preferred) / len(job_preferred) if job_preferred else 0.0
        
        # Overall skill score (70% required, 30% preferred)
        overall_score = (required_score * 0.7) + (preferred_score * 0.3)
        
        return {
            'overall_score': overall_score,
            'required_match': round(required_score * 100, 1),
            'preferred_match': round(preferred_score * 100, 1),
            'matching_skills': [s.title() for s in matching_required + matching_preferred],
            'missing_skills': [s.title() for s in missing_required + missing_preferred],
            'matching_required_count': len(matching_required),
            'total_required_count': len(job_required),
            'matching_preferred_count': len(matching_preferred),
            'total_preferred_count': len(job_preferred)
        }
    
    @staticmethod
    def _calculate_experience_match(resume_doc: Dict, job_doc: Dict) -> float:
        """Calculate experience matching score"""
        job_experience_required = job_doc.get('experience_required', 0)
        if job_experience_required == 0:
            return 1.0  # No requirement, perfect match
        
        resume_experience = resume_doc.get('experience', [])
        experience_years = len(resume_experience)  # Simple: count of positions
        
        if experience_years >= job_experience_required:
            return 1.0
        elif experience_years > 0:
            # Partial match based on ratio
            return min(1.0, experience_years / job_experience_required)
        else:
            return 0.0
    
    @staticmethod
    def _calculate_education_match(resume_doc: Dict, job_doc: Dict) -> float:
        """Calculate education matching score"""
        # If job doesn't specify education requirement, return 1.0
        # For now, we'll return 1.0 if resume has education, 0.5 if not
        resume_education = resume_doc.get('education', [])
        if resume_education:
            return 1.0
        else:
            return 0.5  # Partial score if no education listed

