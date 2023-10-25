# syntax=docker/dockerfile:1

# Use a specific Python version as the base image
ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim as base

# Set environment variables to prevent .pyc files and to prevent buffering
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory for the app
WORKDIR /app

# Create a non-privileged user to run the app
ARG UID=10001
RUN adduser --disabled-password --gecos "" --home "/app" --shell "/sbin/nologin" --uid "10001" appuser && \
    chown -R appuser:appuser /app

# Copy only the requirements.txt to leverage Docker cache
COPY requirements.txt ./

# Install project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Switch to the non-privileged user
USER appuser

# Copy the rest of the app into the image
COPY . /app/

# Expose the port that the application listens on
EXPOSE 8000

WORKDIR /app/src

# Command to run the application using Gunicorn
CMD ["gunicorn", "controller:app", "--bind", "0.0.0.0:8000"]
