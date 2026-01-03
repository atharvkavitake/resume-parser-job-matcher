"""
Skill gap analysis service
Identifies missing skills and provides recommendations
"""

def analyze_skill_gap(resume_skills: list, job_required_skills: list, job_preferred_skills: list = None) -> dict:
    """
    Analyze skill gap between resume and job requirements
    
    Args:
        resume_skills (list): Skills from resume
        job_required_skills (list): Required skills for job
        job_preferred_skills (list): Preferred skills for job
        
    Returns:
        dict: Skill gap analysis
    """
    if not resume_skills:
        resume_skills = []
    if not job_required_skills:
        job_required_skills = []
    if not job_preferred_skills:
        job_preferred_skills = []
    
    # Normalize to lowercase
    resume_skills_lower = [s.lower().strip() for s in resume_skills]
    required_lower = [s.lower().strip() for s in job_required_skills]
    preferred_lower = [s.lower().strip() for s in job_preferred_skills]
    
    # Find gaps
    missing_required = [s for s in required_lower if s not in resume_skills_lower]
    missing_preferred = [s for s in preferred_lower if s not in resume_skills_lower]
    matching_skills = [s for s in resume_skills_lower if s in required_lower or s in preferred_lower]
    
    # Calculate statistics
    total_required = len(required_lower)
    total_preferred = len(preferred_lower)
    matched_required = total_required - len(missing_required)
    matched_preferred = total_preferred - len(missing_preferred)
    
    # Gap percentage
    required_gap = (len(missing_required) / total_required * 100) if total_required > 0 else 0
    preferred_gap = (len(missing_preferred) / total_preferred * 100) if total_preferred > 0 else 0
    
    # Recommendations
    recommendations = []
    if missing_required:
        recommendations.append({
            'priority': 'high',
            'message': f"Learn {len(missing_required)} required skill(s) to improve match",
            'skills': [s.title() for s in missing_required]
        })
    if missing_preferred:
        recommendations.append({
            'priority': 'medium',
            'message': f"Consider learning {len(missing_preferred)} preferred skill(s)",
            'skills': [s.title() for s in missing_preferred]
        })
    if not missing_required and not missing_preferred:
        recommendations.append({
            'priority': 'low',
            'message': "Great! You have all required and preferred skills",
            'skills': []
        })
    
    return {
        'missing_required_skills': [s.title() for s in missing_required],
        'missing_preferred_skills': [s.title() for s in missing_preferred],
        'matching_skills': [s.title() for s in matching_skills],
        'statistics': {
            'total_required': total_required,
            'matched_required': matched_required,
            'total_preferred': total_preferred,
            'matched_preferred': matched_preferred,
            'required_gap_percentage': round(required_gap, 2),
            'preferred_gap_percentage': round(preferred_gap, 2)
        },
        'recommendations': recommendations
    }

