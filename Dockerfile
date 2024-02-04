# Use an official Python runtime as a parent image
FROM python:3.10-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libc6-dev \
    && rm -rf /var/lib/apt/lists/*
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


# # Define environment variable for the mode
# ENV MODE=web

# Copy the main.py script into the container
COPY main.py /app/app.py

# Run main.py when the container launches
CMD ["python", "/app/app.py"]