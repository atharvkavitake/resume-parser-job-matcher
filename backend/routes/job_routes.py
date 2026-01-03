"""
Job-related API routes
Handles job description uploads and management
"""

from flask import Blueprint, request, jsonify
from models.job_model import Job
from nlp.text_extractor import extract_skills

job_bp = Blueprint("job", __name__, url_prefix="/api")

@job_bp.route("/upload-job", methods=["POST"])
def upload_job():
    """
    Upload a job description
    Expects JSON: {
        "title": "...",
        "company": "...",
        "description": "...",
        "required_skills": [...],
        "preferred_skills": [...],
        "experience_required": 5,
        "location": "..."
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Extract required fields
        title = data.get('title', '')
        company = data.get('company', '')
        description = data.get('description', '')
        
        if not title or not description:
            return jsonify({"error": "title and description are required"}), 400
        
        # Auto-extract skills from description if not provided
        required_skills = data.get('required_skills', [])
        preferred_skills = data.get('preferred_skills', [])
        
        if not required_skills and description:
            # Try to extract skills from description
            extracted_skills = extract_skills(description)
            required_skills = extracted_skills[:10]  # Top 10 as required
        
        # Create job data
        job_data = {
            'title': title,
            'company': company,
            'description': description,
            'required_skills': required_skills,
            'preferred_skills': preferred_skills,
            'experience_required': data.get('experience_required', 0),
            'location': data.get('location', '')
        }
        
        # Save to database
        job = Job(job_data)
        job_id = job.save()
        
        # Get saved job
        job_doc = Job.find_by_id(job_id)
        job_obj = Job(job_doc)
        
        return jsonify({
            "success": True,
            "message": "Job uploaded successfully",
            "job": job_obj.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@job_bp.route("/jobs", methods=["GET"])
def get_jobs():
    """
    Get all job descriptions
    """
    try:
        all_jobs = Job.find_all()
        jobs_list = []
        for job_doc in all_jobs:
            job_obj = Job(job_doc)
            jobs_list.append(job_obj.to_dict())
        
        return jsonify({
            "success": True,
            "jobs": jobs_list,
            "count": len(jobs_list)
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@job_bp.route("/jobs/<job_id>", methods=["GET"])
def get_job(job_id):
    """
    Get a specific job by ID
    """
    try:
        job_doc = Job.find_by_id(job_id)
        if not job_doc:
            return jsonify({"error": "Job not found"}), 404
        
        job_obj = Job(job_doc)
        return jsonify({
            "success": True,
            "job": job_obj.to_dict()
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@job_bp.route("/jobs/<job_id>", methods=["DELETE"])
def delete_job(job_id):
    """
    Delete a job by ID
    """
    try:
        success = Job.delete_by_id(job_id)
        if success:
            return jsonify({"success": True, "message": "Job deleted"}), 200
        else:
            return jsonify({"error": "Job not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

