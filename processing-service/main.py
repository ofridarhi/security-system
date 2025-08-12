# processing-service/main.py
from service.processing_service import ProcessingService
import logging
    
    

def main():
    # Configure basic logging to see output clearly.
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s')

    try:
        service = ProcessingService()
        service.run()
    except Exception as e:
        logging.critical(f"A critical error occurred: {e}")

if __name__ == "__main__":
    main()