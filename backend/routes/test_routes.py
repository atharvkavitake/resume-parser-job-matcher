"""
Test API routes
Used for testing and health checks
"""

from flask import Blueprint, jsonify

test_bp = Blueprint("test", __name__, url_prefix="/api")

@test_bp.route("/test", methods=["GET"])
def test_route():
    """Test endpoint to verify API is working"""
    return jsonify({"message": "API route working", "status": "ok"}), 200
