# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim as base

# RUN apt-get update && apt-get install -y curl unzip && \
#     curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
#     unzip awscliv2.zip && \
#     sudo ./aws/install

# Set environment variables to prevent .pyc files and to prevent buffering
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

ARG UID=10001
RUN adduser --disabled-password --gecos "" --home "/app" --shell "/sbin/nologin" --uid "10001" appuser && \
    chown -R appuser:appuser /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

USER appuser

COPY . /app/

EXPOSE 8000

WORKDIR /app/src

CMD ["gunicorn", "controller:app", "--bind", "0.0.0.0:8000"]
