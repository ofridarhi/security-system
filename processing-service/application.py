import logging
import cv2
import base64

from transport.redis_consumer import RedisConsumer
from core.image_processor import ImageProcessor
from data.mongo_event_repository import EventRepository

class Application:
    def __init__(self):
        """
        Initializes and wires up all components from different layers.
        """
        self.consumer = RedisConsumer()
        self.processor = ImageProcessor()
        self.event_repo = EventRepository() 
        logging.info("Application initialized with all layers.")

    def _handle_frame_data(self, frame_data: bytes):
        """
        This is the callback method that gets executed by the RedisConsumer.
        It orchestrates the processing of a single frame.
        """
        # 1. Decode the frame
        frame = self.processor.decode_frame(frame_data)
        if frame is None:
            return # Skip if decoding failed

        # 2. Process the frame to find people
        people_detected = self.processor.detect_people(frame)
        
        # 3. Act on the results
        if people_detected:
            logging.info(f"Person(s) detected! Count: {len(people_detected)}. BBoxes: {people_detected}")

            #Prepare data for the repository for
            _, buffer = cv2.imencode('.jpg', frame)
            jpg_as_text = base64.b64encode(buffer).decode('utf-8') 

            event = {
                "camera_id": "cam_01",
                "detections": [{"type": "person", "bbox": bbox} for bbox in people_detected],
                "frame_base64": jpg_as_text,
                "people_count": len(people_detected)
            }

            # Use the data layer to save the event
            self.event_repo.save_event(event)

    def run(self):
        """
        Starts the main loop by activating the transport layer.
        """
        logging.info("Application is running...")
        try:
            # Tell the transport layer to start listening and use our handler
            self.consumer.listen(channel_name="frames_channel", callback_function=self._handle_frame_data)
        finally:
            self.event_repo.close_connection()