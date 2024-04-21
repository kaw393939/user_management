# Comprehensive Docker Compose Guide for Students

## Overview
This guide will walk you through the process of using Docker Compose to manage a multi-container application consisting of a PostgreSQL database, PgAdmin for database management, a FastAPI application, and Nginx as a reverse proxy.

## Prerequisites
- Ensure Docker and Docker Compose are installed on your computer.
- Basic understanding of Docker, PostgreSQL, FastAPI, and how web applications work.

## Docker Compose Setup

### Starting the Services
- To start all services defined in the Docker Compose file, navigate to the directory containing your `docker-compose.yml` file and run:
  - **`docker-compose up -d`**
  - This command starts the containers in the background.

### Accessing PgAdmin
- Open your web browser and visit `http://localhost:5050` to access PgAdmin.
- Login with the following credentials:
  - **Email**: `admin@example.com`
  - **Password**: `adminpassword`
- Configure the PostgreSQL server in PgAdmin:
  - **Right-click** on 'Servers' in the left pane and select **'Create' > 'Server'**.
  - In the 'General' tab, give your server a name (e.g., `MyAppDB`).
  - Switch to the 'Connection' tab and enter:
    - **Hostname/address**: `postgres`
    - **Port**: `5432`
    - **Username**: `user`
    - **Password**: `password`
    - These credentials correspond to the environment variables set in the `docker-compose.yml` for the PostgreSQL service.

## Managing Application Data with Docker

### Running Database Migrations
- Execute database migrations within the FastAPI container:
  - **`docker-compose exec fastapi alembic upgrade head`**
  - This command runs the Alembic upgrade command to apply migrations to your PostgreSQL database.

### Running Tests with Pytest
- To run tests inside the FastAPI container, ensuring they interact with the PostgreSQL service:
  - **`docker-compose exec fastapi pytest`**
  - This command runs all tests defined in your FastAPI application.

### Specific Test Execution
- To run a specific test file:
  - **`docker-compose exec fastapi pytest /myapp/tests/test_specific_file.py`**

### Running Tests with Coverage
- For executing tests with coverage reports:
  - **`docker-compose exec fastapi pytest --cov=myapp`**
  - To generate an HTML coverage report:
    - **`docker-compose exec fastapi pytest --cov=myapp --cov-report=html`**

## Resetting the Testing Environment
- If you need to reset your environment, e.g., to clear test data:
  - **Stop all services and remove volumes**:
    - **`docker-compose down -v`**
  - **Restart the services**:
    - **`docker-compose up -d`**

## Docker Basics

### Building Docker Images
- To build a Docker image for your FastAPI application, ensure you have a Dockerfile in the same directory as your `docker-compose.yml`. Then run:
  - **`docker-compose build`**

## Pushing Images to Docker Hub

### Creating a Docker Hub Account
- Visit [Docker Hub](https://hub.docker.com/) and sign up for an account.
- Once registered, you can create repositories to store your Docker images.

### Logging into Docker Hub from the Command Line
- **`docker login`**
- Enter your Docker Hub username and password.

### Tagging Your Docker Image
- **`docker tag local-image:tagname username/repository:tag`**
  - For example:
    - **`docker tag myfastapi:latest john/myfastapi:latest`**

### Pushing the Image
- **`docker push username/repository:tag`**
  - For example:
    - **`docker push john/myfastapi:latest`**

## Additional Tips

### Viewing Logs
- To view logs for troubleshooting or monitoring application behavior:
  - **`docker-compose logs -f`**
  - The `-f` flag tails the log output.

### Shutting Down
- To stop and remove all running containers:
  - **`docker-compose down`**

This guide is structured to provide clear, step-by-step instructions on how to interact with the Dockerized environment defined by your Docker Compose setup, ideal for educational purposes and ensuring students are well-equipped to manage their development environment effectively.
