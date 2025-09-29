# Start from a universal base image that has Go, Python, and Node.js
FROM mcr.microsoft.com/devcontainers/universal:2

# Switch to root user to install system packages
USER root

# Install system dependencies needed for your project
# - build-essential & cmake: For compiling dlib (face-recognition)
# - libopencv-dev: The C++ libraries required by GoCV
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
    build-essential \
    cmake \
    libopencv-dev \
    libopencv-contrib-dev

# Switch back to the non-root user
USER vscode