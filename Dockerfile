# --- STAGE 1: Builder ---
# This stage is where all dependencies are installed. It is temporary and will be discarded.
FROM python:3.11-slim AS builder

# Install build tools necessary for packages with C extensions (like psycopg2, greenlet).
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory for the builder stage
WORKDIR /app

# Copy the requirements file first to take advantage of Docker's layer caching.
# If requirements.txt doesn't change, this step and the next one are skipped.
COPY requirements.txt .

# Install Python dependencies. Use --no-cache-dir to prevent caching pip packages.
RUN pip install --no-cache-dir -r requirements.txt


# --- STAGE 2: Final Runtime ---
# This is the final, production-ready image. It is based on a clean, minimal image.
FROM python:3.11-slim

# Set the working directory for the final stage
WORKDIR /app

# Copy the installed packages from the 'builder' stage.
# This is the key step. We only copy the necessary files, not the build tools.
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Copy the rest of your application code
COPY . .

# Expose the port your application listens on
EXPOSE 5000

# Define the command to run your application
CMD ["python3", "app.py"]
