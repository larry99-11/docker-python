FROM python:3.8-slim

WORKDIR /python-docker

COPY requirements.txt .

# Upgrade pip and install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose port 5000 for the Flask application
EXPOSE 5000

# Define the command to run the Flask application using Gunicorn
CMD ["python3", "app.py"]