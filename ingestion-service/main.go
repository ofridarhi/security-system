package main

import (
	"context"
	"log"
	"time"
	"gocv.io/x/gocv"
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

	// open camera.
	webcam, err := gocv.VideoCaptureDevice(0)
	if err != nil {
		log.Fatalf("Error opening video capture device: %v\n", err)
	}
	defer webcam.Close()

	img := gocv.NewMat()
	defer img.Close() 

	log.Println("Starting to read frames from webcam...")

	for {
		//troubleshooting 
		 if ok := webcam.Read(&img); !ok {
            log.Printf("Device closed")
            return
        }
        if img.Empty() {
            log.Println("Empty frame received, skipping")
            continue
        }

		//reading frame
		nativeByteBuffer, err := gocv.IMEncode(gocv.JPEGFileExt, img)
    	if err != nil {
			log.Printf("Failed to encode frame: %v", err)
			continue
    }

    bytesToSend := nativeByteBuffer.GetBytes()

    // sendig to  Redis
    err = rdb.Publish(ctx, "frames_channel", bytesToSend).Err()

    nativeByteBuffer.Close() 
    
    if err != nil {
        log.Printf("Failed to publish frame to Redis: %v", err)
    } else {
        log.Printf("Published frame to Redis (%d bytes)", len(bytesToSend))
    }

    time.Sleep(200 * time.Millisecond)
	}
}