# Smart Security Camera System

[![Go version](https://img.shields.io/badge/Go-1.21+-00ADD8.svg?style=flat&logo=go)](https://golang.org)
[![Python version](https://img.shields.io/badge/Python-3.10+-3776AB.svg?style=flat&logo=python)](https://www.python.org)
[![Docker](https://img.shields.io/badge/Docker-25+-2496ED.svg?style=flat&logo=docker)](https://www.docker.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A real-time, event-driven security system built on a microservices architecture. This project is designed as a complete end-to-end solution for capturing video, performing AI-based analysis, and presenting the results through a web interface.

## Target Architecture

The system is designed as a distributed network of specialized microservices that handle distinct responsibilities, from video ingestion to user interface updates.

```
                                     +-----------------+
                                     |   Frontend UI   |
                                     |     (React)     |
                                     +-------+---------+
                                             | (HTTP/WebSockets)
+----------------+       +-----------+       |       +-----------------+
|  Video Source  |------>|  Ingestion|------>| Redis |------>| Processing    |
| (Webcam/Files) |       |  Service  |       | Pub/Sub|      | Service (AI)  |
+----------------+       |  (Go)     |       +--------+      | (Python)      |
                         +-----------+                      +-------+---------+
                                                                    | (Writes)
                               +-----------------+    +-------------+-----------+
                               |  API Gateway    |<-->| PostgreSQL  |  MongoDB  |
                               | (Python/FastAPI)|    | (Users, etc)|  (Events) |
                               +-----------------+    +-------------+-----------+
```

### Component Breakdown

1.  **Ingestion Service (Go):** A high-performance service responsible for connecting to video sources (webcams, files), reading frames at a set rate, and publishing them to a Redis message broker. Go was chosen for its excellent concurrency model, ideal for handling multiple video streams simultaneously.

2.  **Processing Service (Python):** The AI core of the system. It subscribes to frame data from Redis and executes a multi-stage analysis pipeline:
    -   **Person Detection:** Uses a YOLOv8 model to identify human presence.
    -   **Face Recognition (Planned):** A planned feature to identify registered users by comparing face embeddings against a known database.
    -   **Event Generation:** Creates detailed JSON event documents upon positive detection.
    -   **Data Persistence:** Writes event logs to MongoDB.

3.  **API Gateway (FastAPI - Planned):** The central entry point for all client-facing interactions. It will expose a REST API for managing the system and a WebSocket for streaming real-time events to the frontend.

4.  **Databases:**
    -   **MongoDB:** Stores a log of all detection events. Its flexible, document-based structure is perfect for capturing rich, varied event data.
    -   **PostgreSQL (Planned):** Will be used to store relational data such as user profiles, camera configurations, and face encodings for recognized individuals.

5.  **Frontend UI (React - Planned):** A simple, functional dashboard to display a real-time feed of security events. It will also provide an interface for managing users and cameras.

## Current Project Status

The foundational backend pipeline of the system is complete and functional.

**Implemented Features:**
-  **Go Ingestion Service:** Successfully captures from a webcam and publishes frames.
-  **Event-Driven Backbone:** Redis Pub/Sub correctly mediates communication.
-  **Python Processing Service:** Consumes frames and performs **Person Detection** using YOLOv8.
-  **MongoDB Persistence:** Detection events, including Base64 snapshots, are successfully saved.
-  **Containerized Infrastructure:** All backend services (Redis, MongoDB) are fully containerized with Docker.
-  **Clean Internal Architecture:** The Python service is built with a professional, layered structure (`transport`, `core`, `data`).

## Project Roadmap

The following components are planned to complete the full vision of the project:

-  **API Gateway Service:** Build the FastAPI service to expose data to clients.
-  **PostgreSQL Integration:** Add support for managing users and cameras in a relational database.
-  **Frontend Dashboard:** Develop the React application for data visualization and system management.
-  **Face Recognition:** Implement the second stage of the AI pipeline to recognize known faces.
-  **Real-Time WebSocket:** Implement the WebSocket endpoint in the API service and connect it to the React frontend.

## Tech Stack

| Category         | Technology / Tool                                |
| ---------------- | ------------------------------------------------ |
| **Backend**      | Go 1.21, Python 3.10, FastAPI (Planned)          |
| **Frontend**     | React (Planned)                                  |
| **AI / ML**      | PyTorch, Ultralytics (YOLOv8), OpenCV            |
| **Databases**    | MongoDB, Redis, PostgreSQL (Planned)             |
| **Infrastructure**| Docker, Docker Compose                         |

## Setup and Running (Current Implementation)

### Prerequisites

-   [Docker & Docker Compose](https://www.docker.com/products/docker-desktop/)
-   [Go](https://go.dev/doc/install) (version 1.21 or newer)
-   [Python](https://www.python.org/downloads/) (version 3.10 or newer)
-   Git

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2. Set Up Environment and Dependencies
```bash
# Create and activate a Python virtual environment
python -m venv venv
# On Windows: .\venv\Scripts\Activate.ps1 | On Linux/macOS: source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Install Go dependencies
cd ingestion-service && go mod tidy && cd ..
```

### 3. Run the System
Each component must be run in a separate terminal from the project's root directory.

**Terminal 1: Start Infrastructure (Docker)**
```bash
docker-compose up
```

**Terminal 2: Start the Ingestion Service (Go)**
```bash
cd ingestion-service
go run main.go
```

**Terminal 3: Start the Processing Service (Python)**
(Ensure the Python virtual environment is active)
```bash
python -m processing-service.main
```
The system is now running. The webcam will activate, and detection events will be logged and saved to MongoDB.