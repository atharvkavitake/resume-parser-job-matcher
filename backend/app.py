"""
Main Flask application file
This is the entry point for our backend API
"""

from flask import Flask
from flask_cors import CORS
from config import config

# Import database connection
from db.connection import connect_db, is_connected

# Import blueprints (API routes)
from routes.resume_routes import resume_bp
from routes.job_routes import job_bp
from routes.match_routes import match_bp
from routes.ats_routes import ats_bp
from routes.recommendation_routes import recommendation_bp
from routes.test_routes import test_bp

def create_app():
    """
    Application factory pattern
    Creates and configures the Flask app
    """
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config)
    
    # Enable CORS (allows React frontend to call this API)
    # Allow all origins in development for easier debugging
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)
    
    # Initialize database connection before each request
    @app.before_request
    def ensure_db_connection():
        """Ensure database is connected before each request"""
        if not is_connected():
            connect_db()
    
    # Register blueprints (organize routes)
    app.register_blueprint(test_bp)
    app.register_blueprint(resume_bp)
    app.register_blueprint(job_bp)
    app.register_blueprint(match_bp)
    app.register_blueprint(ats_bp)
    app.register_blueprint(recommendation_bp)
    
    # Health check endpoint
    @app.route("/")
    def home():
        db_status = "connected" if is_connected() else "disconnected"
        return {
            "message": "Backend API is running",
            "status": "ok",
            "database": db_status
        }
    
    return app

# Create the app
app = create_app()

# Initialize database connection when module is imported
connect_db()

if __name__ == "__main__":
    # Run the Flask development server
    app.run(debug=True, host='0.0.0.0', port=5000)
