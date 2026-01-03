"""
NLP text extraction and parsing
Uses spaCy to extract skills, experience, education from resume text
"""

import spacy
import re
from typing import List, Dict

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Warning: spaCy model not found. Please run: python -m spacy download en_core_web_sm")
    nlp = None

# Common skills keywords
SKILL_KEYWORDS = [
    'python', 'javascript', 'java', 'c++', 'c#', 'react', 'angular', 'vue',
    'node.js', 'flask', 'django', 'express', 'mongodb', 'mysql', 'postgresql',
    'aws', 'docker', 'kubernetes', 'git', 'linux', 'html', 'css', 'sql',
    'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'numpy',
    'pandas', 'scikit-learn', 'agile', 'scrum', 'rest api', 'graphql',
    'microservices', 'ci/cd', 'jenkins', 'terraform', 'ansible'
]

def extract_email(text: str) -> str:
    """Extract email address from text"""
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    matches = re.findall(email_pattern, text)
    return matches[0] if matches else ""

def extract_phone(text: str) -> str:
    """Extract phone number from text"""
    phone_patterns = [
        r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
        r'\(\d{3}\)\s?\d{3}[-.]?\d{4}',
        r'\+\d{1,3}[-.]?\d{3,4}[-.]?\d{3,4}[-.]?\d{3,4}'
    ]
    for pattern in phone_patterns:
        matches = re.findall(pattern, text)
        if matches:
            return matches[0]
    return ""

def extract_name(text: str) -> str:
    """Extract name (usually first line or first proper noun)"""
    if not nlp:
        lines = text.split('\n')
        if lines:
            return lines[0].strip()
        return ""
    
    doc = nlp(text[:500])  # Process first 500 chars for speed
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    # Fallback: first line
    lines = text.split('\n')
    return lines[0].strip() if lines else ""

def extract_skills(text: str) -> List[str]:
    """Extract skills from resume text"""
    if not nlp:
        # Simple keyword matching
        found_skills = []
        text_lower = text.lower()
        for skill in SKILL_KEYWORDS:
            if skill.lower() in text_lower:
                found_skills.append(skill.title())
        return list(set(found_skills))
    
    # Use NLP for better extraction
    doc = nlp(text.lower())
    found_skills = []
    
    # Check for skill keywords
    for skill in SKILL_KEYWORDS:
        if skill in text.lower():
            found_skills.append(skill.title())
    
    # Look for skill sections
    skill_section_patterns = [
        r'skills?\s*:?\s*([^\n]+)',
        r'technical\s+skills?\s*:?\s*([^\n]+)',
        r'technologies?\s*:?\s*([^\n]+)'
    ]
    
    for pattern in skill_section_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            # Split by common delimiters
            skills = re.split(r'[,;|•\-]', match)
            for skill in skills:
                skill = skill.strip()
                if len(skill) > 2 and len(skill) < 30:
                    found_skills.append(skill.title())
    
    return list(set(found_skills))[:20]  # Limit to 20 skills

def extract_experience(text: str) -> List[Dict]:
    """Extract work experience from resume"""
    experience = []
    
    # Look for experience section
    exp_patterns = [
        r'experience\s*:?\s*(.+?)(?=education|skills|projects|$)',
        r'work\s+history\s*:?\s*(.+?)(?=education|skills|projects|$)',
        r'employment\s*:?\s*(.+?)(?=education|skills|projects|$)'
    ]
    
    exp_text = ""
    for pattern in exp_patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            exp_text = match.group(1)
            break
    
    if not exp_text:
        # Try to find job titles
        if nlp:
            doc = nlp(text)
            for ent in doc.ents:
                if ent.label_ == "ORG":
                    # Look for job title near organization
                    start = max(0, ent.start_char - 50)
                    end = min(len(text), ent.end_char + 50)
                    context = text[start:end]
                    # Simple extraction
                    lines = context.split('\n')
                    for line in lines:
                        if any(title in line.lower() for title in ['engineer', 'developer', 'manager', 'analyst', 'specialist']):
                            experience.append({
                                'title': line.strip(),
                                'company': ent.text,
                                'duration': ''
                            })
                            break
    
    # Parse experience entries
    if exp_text:
        entries = re.split(r'\n\s*\n', exp_text)
        for entry in entries[:5]:  # Limit to 5 entries
            lines = [l.strip() for l in entry.split('\n') if l.strip()]
            if len(lines) >= 2:
                exp_entry = {
                    'title': lines[0],
                    'company': lines[1] if len(lines) > 1 else '',
                    'duration': lines[-1] if len(lines) > 2 else ''
                }
                experience.append(exp_entry)
    
    return experience[:5]  # Return max 5 experiences

def extract_education(text: str) -> List[Dict]:
    """Extract education from resume"""
    education = []
    
    # Look for education section
    edu_patterns = [
        r'education\s*:?\s*(.+?)(?=experience|skills|projects|$)',
        r'academic\s*:?\s*(.+?)(?=experience|skills|projects|$)'
    ]
    
    edu_text = ""
    for pattern in edu_patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            edu_text = match.group(1)
            break
    
    if edu_text:
        entries = re.split(r'\n\s*\n', edu_text)
        for entry in entries[:3]:  # Limit to 3 entries
            lines = [l.strip() for l in entry.split('\n') if l.strip()]
            if lines:
                edu_entry = {
                    'degree': lines[0],
                    'university': lines[1] if len(lines) > 1 else '',
                    'year': lines[-1] if len(lines) > 2 else ''
                }
                education.append(edu_entry)
    
    return education[:3]  # Return max 3 education entries

def parse_resume_text(text: str) -> Dict:
    """
    Parse resume text and extract structured information
    
    Args:
        text (str): Raw resume text
        
    Returns:
        dict: Parsed resume data
    """
    return {
        'name': extract_name(text),
        'email': extract_email(text),
        'phone': extract_phone(text),
        'skills': extract_skills(text),
        'experience': extract_experience(text),
        'education': extract_education(text),
        'raw_text': text
    }

