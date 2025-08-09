package main

import (
	"context"
	"fmt"
	"log"
	"time"

    "github.com/go-redis/redis/v8"
)

var ctx = context.Background()

func main() {
	// Connect to the Redis instance running inside Docker.
	// We use "localhost" because the container's port is mapped to our host machine.
	rdb := redis.NewClient(&redis.Options{
		Addr:     "localhost:6379", // <-- Important! Connect to the exposed port.
		Password: "",               // No password set by default.
		DB:       0,                // Use the default database.
	})

	// Ping the server to check if the connection is successful.
	_, err := rdb.Ping(ctx).Result()
	if err != nil {
		log.Fatalf("Could not connect to Redis: %v", err)
	}
	log.Println("Connected to Redis successfully!")

	// A loop that publishes a message every 2 seconds.
	for {
		message := fmt.Sprintf("Hello from Go Ingestion Service at %s", time.Now().Format(time.RFC3339))
		
		// Publish the message to the "frames_channel".
		err := rdb.Publish(ctx, "frames_channel", message).Err()
		if err != nil {
			log.Printf("Failed to publish message: %v", err)
		} else {
			log.Printf("Published: '%s'", message)
		}
		
		time.Sleep(2 * time.Second)
	}
}