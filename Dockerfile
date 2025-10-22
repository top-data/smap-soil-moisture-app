# Use an official Python slim image
FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# System deps required by geemap / earthengine and for building wheels
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gdal-bin libgdal-dev \
    proj-bin libproj-dev libgeos-dev \
    wget ca-certificates git curl \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd --create-home --shell /bin/bash appuser

# Set working dir and copy project files (chown in one step)
WORKDIR /home/appuser/app
COPY --chown=appuser:appuser . /home/appuser/app

# Install Python dependencies as root (some packages need build tools)
RUN python -m pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

# Switch to non-root for running the app
USER appuser

# Streamlit config for container
ENV STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_ENABLECORS=false \
    STREAMLIT_SERVER_PORT=8501

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
