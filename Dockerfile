# Define a base stage with a Debian Bullseye base image that supports the needed glibc update
FROM python:3.12-bullseye as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PIP_NO_CACHE_DIR=true \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    QR_CODE_DIR=/myapp/qr_codes

WORKDIR /myapp

# Update system and specifically upgrade libc-bin to address the security vulnerability
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && apt-get install -y libc-bin=2.31-13+deb11u9 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies in /.venv
COPY requirements.txt .
RUN python -m venv /.venv \
    && . /.venv/bin/activate \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

# Define a second stage for the runtime, using the same Debian Bullseye slim image
FROM python:3.12-slim-bullseye as final

# Upgrade libc-bin in the final stage to ensure security patch is applied
RUN apt-get update && apt-get install -y libc-bin=2.31-13+deb11u9 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the virtual environment from the base stage
COPY --from=base /.venv /.venv

# Set environment variable to ensure all python commands run inside the virtual environment
ENV PATH="/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    QR_CODE_DIR=/myapp/qr_codes

# Set the working directory
WORKDIR /myapp

# Create and switch to a non-root user
RUN useradd -m myuser
USER myuser

# Copy application code with appropriate ownership
COPY --chown=myuser:myuser . .

# Inform Docker that the container listens on the specified port at runtime.
EXPOSE 8000

# Use ENTRYPOINT to specify the executable when the container starts.
ENTRYPOINT ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
