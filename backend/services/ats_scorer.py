"""
ATS (Applicant Tracking System) Score Calculator
Evaluates resumes based on ATS-friendly criteria
"""

import re
from typing import Dict, List

class ATSScorer:
    """
    Calculate ATS score based on resume quality factors
    """
    
    # ATS-friendly keywords that improve score
    ATS_KEYWORDS = [
        'experience', 'education', 'skills', 'certification', 'achievement',
        'project', 'leadership', 'team', 'communication', 'problem solving',
        'analytical', 'detail-oriented', 'results-driven', 'proactive'
    ]
    
    # Red flags that decrease score
    RED_FLAGS = [
        'objective',  # Old-style objective statements
        'references available upon request',  # Unnecessary
        'hobbies',  # Not relevant for ATS
        'personal information'  # Privacy concerns
    ]
    
    @staticmethod
    def calculate_ats_score(resume_data: Dict) -> Dict:
        """
        Calculate comprehensive ATS score for a resume
        
        Args:
            resume_data: Resume data dictionary
            
        Returns:
            Dictionary with ATS score and breakdown
        """
        score = 0
        max_score = 100
        factors = {}
        
        # 1. Contact Information (10 points)
        contact_score = ATSScorer._score_contact_info(resume_data)
        score += contact_score
        factors['contact_info'] = {
            'score': contact_score,
            'max': 10,
            'details': ATSScorer._get_contact_details(resume_data)
        }
        
        # 2. Skills Section (20 points)
        skills_score = ATSScorer._score_skills(resume_data)
        score += skills_score
        factors['skills'] = {
            'score': skills_score,
            'max': 20,
            'details': ATSScorer._get_skills_details(resume_data)
        }
        
        # 3. Work Experience (25 points)
        experience_score = ATSScorer._score_experience(resume_data)
        score += experience_score
        factors['experience'] = {
            'score': experience_score,
            'max': 25,
            'details': ATSScorer._get_experience_details(resume_data)
        }
        
        # 4. Education (15 points)
        education_score = ATSScorer._score_education(resume_data)
        score += education_score
        factors['education'] = {
            'score': education_score,
            'max': 15,
            'details': ATSScorer._get_education_details(resume_data)
        }
        
        # 5. Keywords & Formatting (15 points)
        keywords_score = ATSScorer._score_keywords(resume_data)
        score += keywords_score
        factors['keywords'] = {
            'score': keywords_score,
            'max': 15,
            'details': ATSScorer._get_keywords_details(resume_data)
        }
        
        # 6. Resume Length & Structure (10 points)
        structure_score = ATSScorer._score_structure(resume_data)
        score += structure_score
        factors['structure'] = {
            'score': structure_score,
            'max': 10,
            'details': ATSScorer._get_structure_details(resume_data)
        }
        
        # 7. Red Flags (penalties up to -5 points)
        red_flag_penalty = ATSScorer._check_red_flags(resume_data)
        score += red_flag_penalty
        factors['red_flags'] = {
            'score': red_flag_penalty,
            'max': 0,
            'details': ATSScorer._get_red_flag_details(resume_data)
        }
        
        # Ensure score is between 0 and 100
        score = max(0, min(100, score))
        
        # Determine grade
        if score >= 90:
            grade = 'A+'
            rating = 'Excellent'
        elif score >= 80:
            grade = 'A'
            rating = 'Very Good'
        elif score >= 70:
            grade = 'B'
            rating = 'Good'
        elif score >= 60:
            grade = 'C'
            rating = 'Fair'
        elif score >= 50:
            grade = 'D'
            rating = 'Needs Improvement'
        else:
            grade = 'F'
            rating = 'Poor'
        
        return {
            'ats_score': round(score, 1),
            'max_score': max_score,
            'grade': grade,
            'rating': rating,
            'percentage': round((score / max_score) * 100, 1),
            'factors': factors,
            'recommendations': ATSScorer._get_recommendations(factors, score)
        }
    
    @staticmethod
    def _score_contact_info(resume_data: Dict) -> float:
        """Score contact information completeness"""
        score = 0
        if resume_data.get('name'):
            score += 3
        if resume_data.get('email'):
            score += 4
        if resume_data.get('phone'):
            score += 3
        return min(10, score)
    
    @staticmethod
    def _get_contact_details(resume_data: Dict) -> Dict:
        return {
            'has_name': bool(resume_data.get('name')),
            'has_email': bool(resume_data.get('email')),
            'has_phone': bool(resume_data.get('phone'))
        }
    
    @staticmethod
    def _score_skills(resume_data: Dict) -> float:
        """Score skills section"""
        skills = resume_data.get('skills', [])
        if not skills:
            return 0
        
        num_skills = len(skills)
        # 5-10 skills is optimal
        if 5 <= num_skills <= 15:
            return 20
        elif 3 <= num_skills < 5 or 15 < num_skills <= 20:
            return 15
        elif num_skills > 20:
            return 10  # Too many skills
        else:
            return 5  # Too few skills
    
    @staticmethod
    def _get_skills_details(resume_data: Dict) -> Dict:
        skills = resume_data.get('skills', [])
        return {
            'count': len(skills),
            'optimal_range': '5-15 skills',
            'skills_list': skills[:10]  # Show first 10
        }
    
    @staticmethod
    def _score_experience(resume_data: Dict) -> float:
        """Score work experience"""
        experience = resume_data.get('experience', [])
        if not experience:
            return 0
        
        num_experiences = len(experience)
        # 2-5 experiences is good
        if 2 <= num_experiences <= 5:
            return 25
        elif num_experiences == 1:
            return 15
        elif num_experiences > 5:
            return 20  # Too many, might be cluttered
        else:
            return 0
    
    @staticmethod
    def _get_experience_details(resume_data: Dict) -> Dict:
        experience = resume_data.get('experience', [])
        return {
            'count': len(experience),
            'optimal_range': '2-5 experiences',
            'experiences': experience[:5]
        }
    
    @staticmethod
    def _score_education(resume_data: Dict) -> float:
        """Score education section"""
        education = resume_data.get('education', [])
        if not education:
            return 0
        
        # Having education is good
        if len(education) >= 1:
            return 15
        return 0
    
    @staticmethod
    def _get_education_details(resume_data: Dict) -> Dict:
        education = resume_data.get('education', [])
        return {
            'count': len(education),
            'education_list': education
        }
    
    @staticmethod
    def _score_keywords(resume_data: Dict) -> float:
        """Score keyword usage"""
        raw_text = resume_data.get('raw_text', '').lower()
        if not raw_text:
            return 0
        
        # Count ATS keywords found
        keywords_found = sum(1 for keyword in ATSScorer.ATS_KEYWORDS if keyword in raw_text)
        
        # 5-10 keywords is optimal
        if 5 <= keywords_found <= 10:
            return 15
        elif 3 <= keywords_found < 5:
            return 10
        elif keywords_found > 10:
            return 12  # Too many might be keyword stuffing
        else:
            return 5
    
    @staticmethod
    def _get_keywords_details(resume_data: Dict) -> Dict:
        raw_text = resume_data.get('raw_text', '').lower()
        keywords_found = [kw for kw in ATSScorer.ATS_KEYWORDS if kw in raw_text]
        return {
            'keywords_found': len(keywords_found),
            'keywords_list': keywords_found[:10],
            'optimal_range': '5-10 keywords'
        }
    
    @staticmethod
    def _score_structure(resume_data: Dict) -> float:
        """Score resume structure and length"""
        raw_text = resume_data.get('raw_text', '')
        if not raw_text:
            return 0
        
        word_count = len(raw_text.split())
        
        # Optimal resume length: 400-800 words
        if 400 <= word_count <= 800:
            return 10
        elif 200 <= word_count < 400:
            return 7
        elif 800 < word_count <= 1200:
            return 8
        elif word_count > 1200:
            return 5  # Too long
        else:
            return 3  # Too short
    
    @staticmethod
    def _get_structure_details(resume_data: Dict) -> Dict:
        raw_text = resume_data.get('raw_text', '')
        word_count = len(raw_text.split()) if raw_text else 0
        return {
            'word_count': word_count,
            'optimal_range': '400-800 words',
            'status': 'optimal' if 400 <= word_count <= 800 else ('too_short' if word_count < 400 else 'too_long')
        }
    
    @staticmethod
    def _check_red_flags(resume_data: Dict) -> float:
        """Check for red flags (penalties)"""
        raw_text = resume_data.get('raw_text', '').lower()
        if not raw_text:
            return 0
        
        penalty = 0
        red_flags_found = []
        
        for flag in ATSScorer.RED_FLAGS:
            if flag in raw_text:
                penalty -= 1
                red_flags_found.append(flag)
        
        return max(-5, penalty)  # Max penalty of -5
    
    @staticmethod
    def _get_red_flag_details(resume_data: Dict) -> Dict:
        raw_text = resume_data.get('raw_text', '').lower()
        red_flags_found = [flag for flag in ATSScorer.RED_FLAGS if flag in raw_text]
        return {
            'count': len(red_flags_found),
            'flags': red_flags_found
        }
    
    @staticmethod
    def _get_recommendations(factors: Dict, score: float) -> List[Dict]:
        """Generate recommendations based on score factors"""
        recommendations = []
        
        # Contact info recommendations
        contact = factors.get('contact_info', {})
        if contact.get('score', 0) < 10:
            recommendations.append({
                'priority': 'high',
                'category': 'Contact Information',
                'message': 'Ensure your resume includes name, email, and phone number'
            })
        
        # Skills recommendations
        skills = factors.get('skills', {})
        skills_details = skills.get('details', {})
        skill_count = skills_details.get('count', 0)
        if skill_count < 5:
            recommendations.append({
                'priority': 'high',
                'category': 'Skills',
                'message': f'Add more skills. You have {skill_count}, aim for 5-15 relevant skills'
            })
        elif skill_count > 20:
            recommendations.append({
                'priority': 'medium',
                'category': 'Skills',
                'message': f'Too many skills listed ({skill_count}). Focus on 5-15 most relevant skills'
            })
        
        # Experience recommendations
        experience = factors.get('experience', {})
        exp_details = experience.get('details', {})
        exp_count = exp_details.get('count', 0)
        if exp_count == 0:
            recommendations.append({
                'priority': 'high',
                'category': 'Experience',
                'message': 'Add work experience to your resume'
            })
        elif exp_count == 1:
            recommendations.append({
                'priority': 'medium',
                'category': 'Experience',
                'message': 'Consider adding more work experience or projects'
            })
        
        # Keywords recommendations
        keywords = factors.get('keywords', {})
        keywords_details = keywords.get('details', {})
        keywords_found = keywords_details.get('keywords_found', 0)
        if keywords_found < 5:
            recommendations.append({
                'priority': 'medium',
                'category': 'Keywords',
                'message': f'Include more industry-relevant keywords. Found {keywords_found}, aim for 5-10'
            })
        
        # Structure recommendations
        structure = factors.get('structure', {})
        structure_details = structure.get('details', {})
        word_count = structure_details.get('word_count', 0)
        if word_count < 400:
            recommendations.append({
                'priority': 'medium',
                'category': 'Length',
                'message': f'Resume is too short ({word_count} words). Aim for 400-800 words'
            })
        elif word_count > 1200:
            recommendations.append({
                'priority': 'low',
                'category': 'Length',
                'message': f'Resume is too long ({word_count} words). Consider condensing to 400-800 words'
            })
        
        # Red flags recommendations
        red_flags = factors.get('red_flags', {})
        red_flag_details = red_flags.get('details', {})
        if red_flag_details.get('count', 0) > 0:
            recommendations.append({
                'priority': 'high',
                'category': 'Content',
                'message': 'Remove outdated sections like "Objective" or "References available upon request"'
            })
        
        return recommendations

