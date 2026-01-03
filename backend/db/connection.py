"""
MongoDB database connection
Handles connecting to MongoDB and provides database access
"""

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from config import config
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables to store connection and database
client = None
db = None

def connect_db():
    """
    Connect to MongoDB database
    Returns True if successful, False otherwise
    """
    global client, db
    
    try:
        # Create MongoDB client
        client = MongoClient(
            config.MONGODB_URI,
            serverSelectionTimeoutMS=5000  # 5 second timeout
        )
        
        # Test the connection
        client.admin.command('ping')
        
        # Get the database
        db = client[config.DATABASE_NAME]
        
        logger.info(f"✅ Successfully connected to MongoDB: {config.DATABASE_NAME}")
        return True
        
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        logger.error(f"❌ Failed to connect to MongoDB: {e}")
        logger.info("💡 Make sure MongoDB is running on your system")
        logger.info("💡 Or update MONGODB_URI in config.py for MongoDB Atlas")
        return False
    except Exception as e:
        logger.error(f"❌ Unexpected error connecting to MongoDB: {e}")
        return False

def get_db():
    """
    Get the database instance
    Returns the database object if connected, None otherwise
    """
    global db
    if db is None:
        logger.warning("⚠️ Database not connected. Call connect_db() first.")
    return db

def close_db():
    """
    Close the MongoDB connection
    """
    global client
    if client:
        client.close()
        logger.info("Database connection closed")

def is_connected():
    """
    Check if database is connected
    Returns True if connected, False otherwise
    """
    global client
    if client is None:
        return False
    try:
        client.admin.command('ping')
        return True
    except:
        return False

