import redis
import logging

class RedisConsumer():
        # Connect to the Redis instance running inside Docker.
    def __init__(self,host='localhost',port=6379):
        """
        Initializes the connection to Redis.
        """

        self.host = host
        self.port = port
        self.redis = redis.Redis(host=self.host, port=self.port, db=0, decode_responses=False)

        # Check if the connection to Redis is successful.
        try:
            self.redis.ping()
            logging.info("Connected to Redis successfully!")
        except redis.exceptions.ConnectionError as e:
            logging.error(f"Could not connect to Redis: {e}")
            return
        
        logging.info(" Redis_consumer initialization complete.")

    def listen(self, callback_function, channel_name="frames_channel"):
        """
        Listens to a specific channel and calls the callback function
        for each message.
        """

        # Create a PubSub object to subscribe to channels.
        pubsub = self.redis.pubsub()
        pubsub.subscribe(channel_name)
        logging.info(f"Subscribed to '{channel_name}'. Waiting for messages...")

        for message in pubsub.listen():
            if message['type'] == 'message':
                # We pass the raw data to the callback
                callback_function(message['data'])

