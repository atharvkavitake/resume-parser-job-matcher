"""
Resume-related API routes
Handles resume uploads, parsing, and management
"""

from flask import Blueprint, request, jsonify
import os
from config import config
from services.resume_parser import parse_resume_file
from services.ats_scorer import ATSScorer
from models.resume_model import Resume
from bson import ObjectId

resume_bp = Blueprint("resume", __name__, url_prefix="/api")

@resume_bp.route("/upload-resume", methods=["POST"])
def upload_resume():
    """
    Upload and parse a resume file (PDF or DOCX)
    Automatically extracts text and parses information
    """
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    # Check file extension
    if '.' not in file.filename:
        return jsonify({"error": "Invalid file type"}), 400
    
    file_ext = file.filename.rsplit('.', 1)[1].lower()
    if file_ext not in config.ALLOWED_EXTENSIONS:
        return jsonify({
            "error": f"File type not allowed. Allowed types: {', '.join(config.ALLOWED_EXTENSIONS)}"
        }), 400

    try:
        # Create uploads directory if it doesn't exist
        os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)

        # Save the file
        file_path = os.path.join(config.UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # Parse the resume
        parsed_resume = parse_resume_file(file_path, file.filename)
        
        # Calculate ATS score
        ats_result = ATSScorer.calculate_ats_score(parsed_resume)
        parsed_resume['ats_score'] = ats_result

        return jsonify({
            "success": True,
            "message": "Resume uploaded and parsed successfully",
            "resume": parsed_resume
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@resume_bp.route("/resumes", methods=["GET"])
def get_resumes():
    """
    Get all uploaded resumes
    """
    try:
        all_resumes = Resume.find_all()
        resumes_list = []
        for resume_doc in all_resumes:
            resume_obj = Resume(resume_doc)
            resumes_list.append(resume_obj.to_dict())
        
        return jsonify({
            "success": True,
            "resumes": resumes_list,
            "count": len(resumes_list)
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@resume_bp.route("/resumes/<resume_id>", methods=["GET"])
def get_resume(resume_id):
    """
    Get a specific resume by ID
    """
    try:
        resume_doc = Resume.find_by_id(resume_id)
        if not resume_doc:
            return jsonify({"error": "Resume not found"}), 404
        
        resume_obj = Resume(resume_doc)
        return jsonify({
            "success": True,
            "resume": resume_obj.to_dict()
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@resume_bp.route("/resumes/<resume_id>", methods=["DELETE"])
def delete_resume(resume_id):
    """
    Delete a resume by ID
    """
    try:
        success = Resume.delete_by_id(resume_id)
        if success:
            return jsonify({"success": True, "message": "Resume deleted"}), 200
        else:
            return jsonify({"error": "Resume not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

