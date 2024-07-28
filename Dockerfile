# Use an official lightweight Python image.
# 3.12-slim variant is chosen for a balance between size and utility.
FROM python:3.12-slim-bullseye as base

# Set environment variables to configure Python and pip.
# Prevents Python from buffering stdout and stderr, enables the fault handler, disables pip cache,
# sets default pip timeout, and suppresses pip version check messages.
ENV PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PIP_NO_CACHE_DIR=true \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    QR_CODE_DIR=/myapp/qr_codes

# Set the working directory inside the container
WORKDIR /myapp

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy only the requirements, to cache them in Docker layer
COPY ./requirements.txt /myapp/requirements.txt

# Upgrade pip and install Python dependencies from requirements file
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Add a non-root user and switch to it
RUN useradd -m myuser
USER myuser

# Copy the rest of your application's code with appropriate ownership
COPY --chown=myuser:myuser . /myapp

# Inform Docker that the container listens on the specified port at runtime.
EXPOSE 8000

# Use ENTRYPOINT to specify the executable when the container starts.
ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
