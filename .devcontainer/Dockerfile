# Start from a focused, smaller Python 3.12 image
FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ARG GO_VERSION=1.22.5

# Switch to root to install software
USER root

# 1. Install ALL build dependencies for Go, OpenCV (from GoCV), and Python's dlib
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    make \
    sudo \
    procps \
    wget \
    build-essential \
    cmake \
    libgl1-mesa-glx \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
# 2. Install Go
RUN wget -q https://go.dev/dl/go${GO_VERSION}.linux-amd64.tar.gz -O /tmp/go.tar.gz && \
    tar -C /usr/local -xzf /tmp/go.tar.gz && \
    rm /tmp/go.tar.gz
ENV PATH="/usr/local/go/bin:${PATH}"

# 3. Use GoCV's official Makefile to build and install itself and the correct OpenCV version.
#    This is the long-running step.
RUN mkdir -p /go/src/gocv.io/x && \
    cd /go/src/gocv.io/x && \
    git clone https://github.com/hybridgroup/gocv.git && \
    cd gocv && \
    make deps && \
    make build && \
    make sudo_install

# 4. Set the PKG_CONFIG_PATH for the final environment
ENV PKG_CONFIG_PATH=/usr/local/lib/pkgconfig

# 5. Clean up the gocv source to save space
RUN rm -rf /go/src/gocv.io

# Switch back to the non-root user for the Codespace
USER vscode
WORKDIR /workspaces