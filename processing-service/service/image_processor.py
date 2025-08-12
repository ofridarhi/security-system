import logging
import cv2
import numpy as np
from ultralytics import YOLO


class ImageProcessor:

    def __init__(self,model_path='yolov8n.pt'):
        """
        Initializes the YOLO model.
        """
        logging.info("Initializing ImageProcessor...")
        self.yolo_model = YOLO(model_path) 
        self.person_class_id = 0 # 0 is the class for 'person' in COCO dataset
        logging.info("YOLO model loaded successfully.")


    def decode_frame(self, frame_data: bytes) -> np.ndarray | None:
        """
        Decodes a byte buffer into an OpenCV image (NumPy array).
        """

        try:
            np_arr = np.frombuffer(frame_data, np.uint8)
            return cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        except Exception as e:
            logging.error(f"Failed to decode frame: {e}")
            return None
    
    def detect_people(self, frame: np.ndarray)-> list:
        """
        Processes a single frame to find people.
        Returns a list of detected people's bounding boxes.
        """
        if frame is None:
            return []

        results = self.yolo_model(frame, verbose=False) # verbose=False to prevent flooding logs     

        detected_people  = []
        for result in results:
            for box in result.boxes:
                if int(box.cls) == self.person_class_id: 
                    bounding_box = box.xyxy[0].cpu().numpy().tolist() # (x1, y1, x2, y2) --> (top left, bottom right)
                    detected_people.append(bounding_box)

        return detected_people
