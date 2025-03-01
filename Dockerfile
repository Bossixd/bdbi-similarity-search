# Force x86_64 architecture and use a compatible base
FROM debian

# Install essential x86_64 libraries and dependencies
RUN apt-get update && \
    apt-get install -y \
    ca-certificates \
    libc6:ard64 \
    libc6-dev:ard64 \
    wget \
    python3 \
    python3-pip \
    build-essential \
    manpages-dev \
    curl

# Download and install prebuilt GLIBC 2.36 from Debian Bookworm
WORKDIR /glibc
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    echo "deb http://deb.debian.org/debian bookworm main" >> /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y libc6 libstdc++6 libc6-dev && \
    mkdir /opt/glibc-2.36 && \
    cp -r /lib/x86_64-linux-gnu /opt/glibc-2.36/lib

# Set the new GLIBC path
ENV LD_LIBRARY_PATH="/opt/glibc-2.36/lib:$LD_LIBRARY_PATH"

# Ensure the loader symlink is correctly set
RUN ln -sf /opt/glibc-2.36/lib/ld-2.36.so /lib64/ld-linux-x86-64.so.2

# Setup the working directory
WORKDIR /app

# Move requirements.txt to the working directory
COPY requirements.txt .

# Install Python dependencies
# RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Expose port 8000
EXPOSE 8000

# Run the application
CMD ["python3", "app.py"]
