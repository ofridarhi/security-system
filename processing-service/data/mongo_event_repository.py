import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
from datetime import datetime


logger = logging.getLogger(__name__)

class MongoEventRepository():
    DATABASE_NAME = "security_system_db"
    COLLECTION_NAME = "events"

    def __init__(self,uri="mongodb://localhost:27017/"):
        """
        Initializes the connection to the MongoDB database and the specific collection.
        """
        logger.info("Initializing MongoEventRepository...")
        self.uri = uri

        try:
            self.client = MongoClient(self.uri, serverSelectionTimeoutMS=5000)
            self.client.admin.command('ismaster')
            logging.info("MongoDB connection successful.")
        except:
            logging.error(f"Could not connect to MongoDB: {e}")
            return
        
        self.db = self.client[self.DATABASE_NAME]
        self.collection = self.db[self.COLLECTION_NAME]
        logger.info(f"Connected to database '{self.DATABASE_NAME}' and collection '{self.COLLECTION_NAME}'.")



    def save_event(self,event_data:dict)-> str | None:
        """
        Saves a single event document to the 'events' collection.
        Returns the ID of the inserted document, or None if it failed.
        """
        if not isinstance(event_data, dict):
            logger.error("Event data must be a dictionary.")
            return None
        
        try:
            event_data['createdAt'] = datetime.utcnow() # Adding a timestamp from the server's perspective right before insertion
            result = self.collection.insert_one(event_data)

            inserted_id = str(result.inserted_id)
            logger.info(f"Event saved to MongoDB with id: {inserted_id}")
            return inserted_id
        except OperationFailure as e:
            logger.error(f"Failed to save event to MongoDB (operation failure): {e}")
            return None
        except Exception as e:
            # Catch other potential errors
            logger.error(f"An unexpected error occurred while saving event: {e}")
            return None
        

    def close_connection(self):
        """
        Closes the MongoDB connection.
        """
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed.")
