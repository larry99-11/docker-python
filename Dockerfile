FROM python:3.11-slim

#  includes g++, gcc, make, and other tools needed to compile C/C++ packages. The --no-cache flag ensures that the package manager's cache is cleaned up after installation
RUN apt-get update && apt-get install -y build-essential

WORKDIR /python-docker

COPY requirements.txt .

# Upgrade pip and install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose port 5000 for the Flask application
EXPOSE 5000

# Define the command to run the Flask application
CMD ["python3", "app.py"]