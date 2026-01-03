"""
ATS Score calculation routes
"""

from flask import Blueprint, request, jsonify
from models.resume_model import Resume
from services.ats_scorer import ATSScorer

ats_bp = Blueprint("ats", __name__, url_prefix="/api")

@ats_bp.route("/ats-score/<resume_id>", methods=["GET"])
def get_ats_score(resume_id):
    """
    Get ATS score for a specific resume
    """
    try:
        resume_doc = Resume.find_by_id(resume_id)
        if not resume_doc:
            return jsonify({"error": "Resume not found"}), 404
        
        resume_obj = Resume(resume_doc)
        resume_data = resume_obj.to_dict()
        
        # Calculate ATS score
        ats_result = ATSScorer.calculate_ats_score(resume_data)
        
        return jsonify({
            "success": True,
            "resume_id": resume_id,
            "resume_name": resume_data.get('name', 'Unknown'),
            "ats_score": ats_result
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

