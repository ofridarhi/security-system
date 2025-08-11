# processing-service/main.py
import redis
import time
import logging
    
    
# Configure basic logging to see output clearly.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    # Connect to the Redis instance running inside Docker.
    # We also use "localhost" here as the port is exposed to the host.
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=False)
    
    try:
        # Check if the connection to Redis is successful.
        r.ping()
        logging.info("Connected to Redis successfully!")
    except redis.exceptions.ConnectionError as e:
        logging.error(f"Could not connect to Redis: {e}")
        return

    # Create a PubSub object to subscribe to channels.
    pubsub = r.pubsub()
    # Subscribe to the "frames_channel" to receive messages.
    pubsub.subscribe("frames_channel")
    
    logging.info("Subscribed to 'frames_channel'. Waiting for messages...")

    # Listen for messages in a loop.
    for message in pubsub.listen():
        # The first message received is a confirmation message, which we can ignore.
        if message['type'] == 'message':
            logging.info(f"Received: '{message['data']}'")

if __name__ == "__main__":
    main()