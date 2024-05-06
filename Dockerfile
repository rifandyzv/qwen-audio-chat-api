# Use the official Python image as the base
FROM nvidia/cuda:12.1.1-runtime-ubuntu20.04

RUN apt-get update && \
    apt-get install -y python3-pip python3-dev python-is-python3 && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Install dependencies
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI app code into the container
COPY . .

# Expose port 8080
EXPOSE 8080

# Run uvicorn with host 0.0.0.0 and port 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
