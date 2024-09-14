# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install any needed packages from requirements.txt (if applicable)
# Ensure that server.py dependencies are listed in requirements.txt
RUN pip install -r requirements.txt

# Expose port 5000 for the server to be accessible
EXPOSE 5000

# Command to run the server
CMD ["python", "server.py"]
