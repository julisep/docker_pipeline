# Use an official Python runtime as a parent image
FROM python:3.6-slim

# Set the working directory to /app (creates a new folder)
WORKDIR /app

# Copy all files in current working directory into the docker container
COPY . /app

# Install any needed packages
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Run app.py when the container launches
CMD ["python", "etl.py"]
