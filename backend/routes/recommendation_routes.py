"""
Job recommendation routes
"""

from flask import Blueprint, request, jsonify
from services.job_recommender import JobRecommender

recommendation_bp = Blueprint("recommendation", __name__, url_prefix="/api")

@recommendation_bp.route("/recommend-jobs/<resume_id>", methods=["GET"])
def recommend_jobs(resume_id):
    """
    Get job recommendations for a resume
    """
    try:
        limit = request.args.get('limit', 10, type=int)
        
        recommendations = JobRecommender.recommend_jobs_for_resume(resume_id, limit)
        
        return jsonify({
            "success": True,
            "resume_id": resume_id,
            "recommendations": recommendations,
            "count": len(recommendations)
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

