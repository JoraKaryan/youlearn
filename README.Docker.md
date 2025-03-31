# Docker Setup for YouLearn

## Prerequisites
- Docker installed on your system

## Building the Docker Image
1. Navigate to the project directory
2. Build the image:
   ```bash
   docker build -t youlearn .
   ```

## Running the Container
1. Run the container with port mapping:
   ```bash
   docker run -p 8000:8000 youlearn
   ```

## Accessing the Application
- The application will be available at: http://localhost:8000

## Additional Commands
- To run migrations:
  ```bash
  docker exec -it <container_id> python manage.py migrate
  ```
- To create a superuser:
  ```bash
  docker exec -it <container_id> python manage.py createsuperuser
  ```

## Environment Variables
- `PYTHONDONTWRITEBYTECODE=1`: Prevents Python from writing .pyc files
- `PYTHONUNBUFFERED=1`: Ensures Python output is sent straight to terminal

## Notes
- The container exposes port 8000 by default
- The Dockerfile uses Python 3.11 as the base image