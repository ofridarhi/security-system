import logging

from application import Application

def main():
    # Configure basic logging to see output clearly.
    logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s')
    logger = logging.getLogger(__name__)


    try:
        logger.info("Starting application...")
        app = Application()
        app.run()
    except Exception as e:
        logger.critical(f"A critical error occurred in the application: {e}", exc_info=True)

if __name__ == "__main__":
    main()