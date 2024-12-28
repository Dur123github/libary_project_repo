# Use the official Python base image
# Use a lightweight Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /myapp
COPY requirements.txt /myapp/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt


# Expose the port your Flask app runs on (default: 5000)
EXPOSE 5000

# Command to run the Flask app
CMD ["python", "app.py"]
