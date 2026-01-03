"""
Configuration file for Flask application
Stores all settings in one place for easy management
"""

import os
from datetime import timedelta

class Config:
    """Base configuration class"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # MongoDB settings
    MONGODB_URI = os.environ.get('MONGODB_URI') or 'mongodb://localhost:27017/'
    DATABASE_NAME = os.environ.get('DATABASE_NAME') or 'resume_matcher_db'
    
    # File upload settings
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
    MAX_UPLOAD_SIZE = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc'}
    
    # CORS settings (for React frontend)
    CORS_ORIGINS = ['http://localhost:3000', 'http://localhost:5173', 'http://127.0.0.1:3000']  # React dev servers
    
    # API settings
    JSON_SORT_KEYS = False

class DevelopmentConfig(Config):
    """Configuration for development"""
    DEBUG = True

class ProductionConfig(Config):
    """Configuration for production"""
    DEBUG = False
    # In production, these should come from environment variables
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MONGODB_URI = os.environ.get('MONGODB_URI')

# Default to development config
config = DevelopmentConfig

