# Buzz API test

This project is a FastAPI based API to solve the buzz api tech test. The project is structured with modular components for easy maintenance and scaling.

## Project Structure

```
.
├── Dockerfile
├── app
│   ├── api
│   │   ├── endpoints
│   │   │   ├── __init__.py
│   │   │   └── machine.py
│   │   └── shared
│   │       ├── __init__.py
│   │       └── responses.py
│   ├── database
│   │   ├── base.py
│   │   ├── engine.py
│   │   ├── models.py
│   │   └── schemas.py
│   └── services
│       ├── __init__.py
│       ├── machine_service.py
│       ├── shared
│       │   ├── __init__.py
│       │   └── errors.py
│       └── site_service.py
├── docker-compose.yml
├── entrypoint.sh
├── main.py
└── requirements.txt
```

- `Dockerfile`: Dockerfile for building the container image.
- `app`: Main application folder containing the API, database, and service modules.
- `app/api`: API endpoints and shared responses.
- `app/api/endpoints`: Individual endpoint modules.
- `app/api/shared`: Shared response schemas.
- `app/database`: Database-related modules, including models, schemas, and engine.
- `app/services`: Service modules that handle the business logic.
- `app/services/shared`: Shared service-related modules, including error handling.
- `docker-compose.yml`: Docker Compose configuration file.
- `entrypoint.sh`: Shell script for running the application in a Docker container.
- `main.py`: Entry point of the FastAPI application.
- `requirements.txt`: Python package dependencies for the project.

## Getting Started

1. Install the required packages:

```bash
pip install -r requirements.txt
```

2. Run the application:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

You can now access the API at `http://localhost:8000`.

## Running with Docker

1. Set the env vars on .env file, if is the first time you are running the project or you just want to rebuild the database just
set RUN_INIT_DB=1 otherwise you can leave 0.


2. Build the Docker image:

```bash
docker build -t my-fastapi-project .
```

3. Run the Docker container:

```bash
docker run -d --name my-fastapi-project -p 8000:8000 my-fastapi-project
```

Alternatively, use Docker Compose to run the container:

```bash
docker-compose up -d
```

If you want you can up only the db image with:
```bash
docker-compose up -d db
```

The API should be accessible at `http://localhost:8000`.

## How to test

Run the following command:
```bash
python3 -m pytest
```
## API Documentation

You can access the API documentation at `http://localhost:8000/docs` and the ReDoc documentation at `http://localhost:8000/redoc`.
