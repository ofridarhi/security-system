
import logging
from .redis_consumer import RedisConsumer
from .image_processor import ImageProcessor

class ProcessingService:

    def __init__(self):
        """
        Initializes and wires up all components of the service.
        """
        self.consumer = RedisConsumer()
        self.processor = ImageProcessor()
        logging.info("ProcessingService initialized.")

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
        # (Else, do nothing if no one is found)

    def run(self):
        """
        Starts the main loop of the service.
        """
        logging.info("ProcessingService is running...")
        # Tell the consumer to start listening and use our handler method as the callback
        self.consumer.listen(channel_name="frames_channel", callback_function=self._handle_frame_data)

