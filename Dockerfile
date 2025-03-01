# Force x86_64 architecture and use a compatible base
FROM python:3.9-slim

# Install essential x86_64 libraries and dependencies
RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip

# Setup the working directory
WORKDIR /app

# Move requirements.txt to the working directory
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Expose port 8080
EXPOSE 8080

# Run the application
CMD ["python3", "app.py"]
