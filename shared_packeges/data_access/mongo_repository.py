import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os

logger = logging.getLogger(__name__)

class MongoRepository():
    """
    A generic repository for MongoDB operations.
    """
    def __init__(self, collection_name: str, db_name: str = "security_system_db", uri: str = "mongodb://localhost:27017/"):
        """
        Initializes the connection to a specific collection.
        Note: We use 'mongo' as the host, which is the service name in docker-compose.
        """
        logger.info(f"Initializing MongoRepository for collection '{collection_name}'...")
        self.collection_name = collection_name
        self.db_name = db_name
        
        try:
            # We connect to the Docker service name
            self.client = MongoClient(uri, serverSelectionTimeoutMS=5000)
            self.client.admin.command('ismaster')
            logger.info("MongoDB connection successful.")
        except ConnectionFailure as e:
            logger.error(f"Could not connect to MongoDB: {e}")
            raise

        self.db = self.client[self.db_name]
        self.collection = self.db[self.collection_name]
        logger.info(f"Connected to database '{self.db_name}' and collection '{self.collection_name}'.")
    
    def find(self, query: dict, limit: int = 10):
        """Finds documents based on a query."""
        try:
            # Convert ObjectId to string for JSON serialization
            cursor = self.collection.find(query).sort("createdAt", -1).limit(limit)
            results = []
            for doc in cursor:
                doc['_id'] = str(doc['_id'])
                results.append(doc)
            return results
        except Exception as e:
            logger.error(f"Error finding documents: {e}")
            return []
        
    def insert_one(self, document: dict) -> str | None:
        """Inserts one document."""
        try:
            result = self.collection.insert_one(document)
            inserted_id = str(result.inserted_id)
            logger.info(f"Document inserted with id: {inserted_id}")
            return inserted_id
        except Exception as e:
            logger.error(f"Error inserting document: {e}")
            return None
    
    def close_connection(self):
        """
        Closes the MongoDB connection.
        """
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed.")