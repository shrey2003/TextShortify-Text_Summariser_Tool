# Use an official Python runtime as a parent image
FROM python:3.10-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


# Define environment variable for the mode
ENV MODE=web

# Copy the main.py script into the container
COPY main.py /app/main.py

# Run main.py when the container launches
CMD ["python", "/app/main.py"]