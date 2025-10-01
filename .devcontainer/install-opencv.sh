#!/bin/bash
set -e # Exit immediately if a command exits with a non-zero status.

LOCK_FILE="/usr/local/etc/gocv-installed"

# Check if the installation has already been completed successfully.
if [ -f "$LOCK_FILE" ]; then
    echo "GoCV and OpenCV are already installed. Skipping build."
    exit 0
fi

echo "--- Installing GoCV and building OpenCV from source via official Makefile ---"
echo "--- This will take a long time (20-45 minutes)... ---"

# 1. Download the GoCV source code
# The GOPATH in these dev containers is /go
# We need to create the directory structure first
mkdir -p /go/src/gocv.io/x
cd /go/src/gocv.io/x
git clone https://github.com/hybridgroup/gocv.git
cd gocv

# 2. Run the official install command.
# This single command handles dependencies, download, build, and install.
# We use sudo because 'make deps' and 'make sudo_install' need it.
sudo make install

# 3. Create the lock file to prevent this script from running again
echo "--- Finalizing installation ---"
sudo touch "$LOCK_FILE"
sudo chown vscode "$LOCK_FILE"

# 4. Clean up the source code to save space
echo "--- Cleaning up GoCV source files ---"
rm -rf /go/src/gocv.io

echo "--- GoCV and OpenCV installation complete! ---"