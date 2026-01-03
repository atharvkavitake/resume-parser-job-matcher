"""
Matching-related API routes
Handles resume-job matching and skill gap analysis
"""

from flask import Blueprint, request, jsonify
from models.resume_model import Resume
from models.job_model import Job
from ml.matcher import match_resume_to_job
from services.skill_gap import analyze_skill_gap

match_bp = Blueprint("match", __name__, url_prefix="/api")

@match_bp.route("/match", methods=["POST"])
def match_resume_job():
    """
    Match a resume to a job
    Expects JSON: {
        "resume_id": "...",
        "job_id": "..."
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        resume_id = data.get('resume_id')
        job_id = data.get('job_id')
        
        if not resume_id or not job_id:
            return jsonify({"error": "resume_id and job_id are required"}), 400
        
        # Get resume and job from database
        resume_doc = Resume.find_by_id(resume_id)
        job_doc = Job.find_by_id(job_id)
        
        if not resume_doc:
            return jsonify({"error": "Resume not found"}), 404
        
        if not job_doc:
            return jsonify({"error": "Job not found"}), 404
        
        # Match resume to job
        match_result = match_resume_to_job(resume_doc, job_doc)
        
        # Add skill gap analysis
        resume_skills = resume_doc.get('skills', [])
        job_required = job_doc.get('required_skills', [])
        job_preferred = job_doc.get('preferred_skills', [])
        
        skill_gap = analyze_skill_gap(resume_skills, job_required, job_preferred)
        match_result['skill_gap'] = skill_gap
        
        return jsonify({
            "success": True,
            "match": match_result
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@match_bp.route("/match-all/<job_id>", methods=["GET"])
def match_all_resumes_to_job(job_id):
    """
    Match all resumes to a specific job
    Returns ranked list of matches
    """
    try:
        # Get job
        job_doc = Job.find_by_id(job_id)
        if not job_doc:
            return jsonify({"error": "Job not found"}), 404
        
        # Get all resumes
        all_resumes = Resume.find_all()
        
        # Match each resume to job
        matches = []
        for resume_doc in all_resumes:
            try:
                match_result = match_resume_to_job(resume_doc, job_doc)
                
                # Add skill gap
                resume_skills = resume_doc.get('skills', [])
                job_required = job_doc.get('required_skills', [])
                job_preferred = job_doc.get('preferred_skills', [])
                
                skill_gap = analyze_skill_gap(resume_skills, job_required, job_preferred)
                match_result['skill_gap'] = skill_gap
                
                matches.append(match_result)
            except Exception as e:
                print(f"Error matching resume {resume_doc.get('_id')}: {e}")
                continue
        
        # Sort by match score (highest first)
        matches.sort(key=lambda x: x['overall_match_score'], reverse=True)
        
        return jsonify({
            "success": True,
            "job_id": job_id,
            "job_title": job_doc.get('title', ''),
            "matches": matches,
            "count": len(matches)
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@match_bp.route("/match-resume/<resume_id>", methods=["GET"])
def match_resume_to_all_jobs(resume_id):
    """
    Match a specific resume to all jobs
    Returns ranked list of matches
    """
    try:
        # Get resume
        resume_doc = Resume.find_by_id(resume_id)
        if not resume_doc:
            return jsonify({"error": "Resume not found"}), 404
        
        # Get all jobs
        all_jobs = Job.find_all()
        
        # Match resume to each job
        matches = []
        for job_doc in all_jobs:
            try:
                match_result = match_resume_to_job(resume_doc, job_doc)
                
                # Add skill gap
                resume_skills = resume_doc.get('skills', [])
                job_required = job_doc.get('required_skills', [])
                job_preferred = job_doc.get('preferred_skills', [])
                
                skill_gap = analyze_skill_gap(resume_skills, job_required, job_preferred)
                match_result['skill_gap'] = skill_gap
                
                matches.append(match_result)
            except Exception as e:
                print(f"Error matching job {job_doc.get('_id')}: {e}")
                continue
        
        # Sort by match score (highest first)
        matches.sort(key=lambda x: x['overall_match_score'], reverse=True)
        
        return jsonify({
            "success": True,
            "resume_id": resume_id,
            "resume_name": resume_doc.get('name', ''),
            "matches": matches,
            "count": len(matches)
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
