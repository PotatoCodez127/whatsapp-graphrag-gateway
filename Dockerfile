# Use a secure, lightweight, official Python runtime as our base layer
FROM python:3.11-slim

# Enforce clean logging outputs and block bytecode writing
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Initialize the runtime application directory inside the image container
WORKDIR /app

# Copy dependency specifications first to leverage Docker's layer cache engine
COPY requirements.txt .

# Install dependencies directly to the global image layer without caching wheel downloads
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Mirror remaining source code components into the deployment workspace
COPY . .

# Expose the default communication port assigned to the gateway webhook router
EXPOSE 5001

# Execute Gunicorn binding multi-worker threads to production port 5001
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--workers", "2", "webhook:app"]