# Use an official Python runtime as a parent image
FROM python:3.6-slim

# Set the working directory to /app (creates a new folder)
WORKDIR /app
COPY requirements.txt /app
RUN pip install --trusted-host pypi.python.org -r requirements.txt

COPY get_tweets.py /app
COPY config.py /app

# Run app.py when the container launches
CMD ["python", "get_tweets.py"]
