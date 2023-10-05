# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Install dependencies
RUN pip install --no-cache-dir rembg flask requests

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Copy the current directory contents into the container at /usr/src/app
COPY ./app /usr/src/app

# Run app.py when the container launches
CMD ["python", "./main.py"]