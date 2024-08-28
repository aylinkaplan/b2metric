
## B2Metric Project Documentation

### Overview
The B2Metric project provides CRUD operations for managing books and patrons in a library. It utilizes FastAPI for building the REST API, Celery for task management, Redis as the message broker, and Celery-Beat for scheduling periodic tasks.

### Working in a Virtual Environment

Project uses Python 3.11.

#### Create/Activate Relevant Python Version
```bash
brew install pyenv
pyenv install 3.11
pyenv shell 3.11
python --version
```

#### Prepare virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Working with Docker Containers
To build and run the Docker containers for the project, use the following command:
```bash
docker-compose up --build
```

### API Documentation:
API documentation is automatically generated by FastAPI and can be accessed at:
```bash
http://0.0.0.0:8000/docs
```

### Verifying Celery-Beat Tasks
#### Check Logs
To check the logs for Celery-Beat and verify task execution, use:
```bash
docker logs <celery_beat_container_id>
```
Replace <celery_beat_container_id> with the actual container ID or name for the Celery-Beat service.

#### Test Task Execution
To test Celery tasks manually, you can run use:


```bash
docker-compose run web python test_celery.py
```