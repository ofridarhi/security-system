import logging
from datetime import datetime

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from shared_packages.data_access.mongo_repository import MongoRepository

logger = logging.getLogger(__name__)



class EventRepository(MongoRepository): 
    """
    A specific repository for handling 'event' documents.
    It inherits generic MongoDB functionalities from MongoRepository.
    """
    def __init__(self):
        """
        Initializes the repository.
        It calls the parent constructor with the specific collection name for events.
        """
        logger.info("Initializing EventRepository...")
        super().__init__(collection_name="events")

    def save_event(self, event_data: dict) -> str | None:
        """
        Saves an event document, adding a timestamp before insertion.
        """
        logger.debug(f"Saving event with data: {event_data}")
        event_data['createdAt'] = datetime.utcnow()
        
        return self.insert_one(event_data)