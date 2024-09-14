# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install Flask requests

# Make port 5002 available to the world outside this container
EXPOSE 5002

# Run the Flask app
CMD ["python", "server_flask_gui.py"]
