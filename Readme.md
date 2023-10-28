# Python-FastAPI Web-Server Boilerplate
This is a boilerplate for the FastAPI frame work with best practices and pre-setup user domain. one can add the new domains as per the requirements after cloning it.

## This repo contains or will contain following things

- [x] Basic setup and configurations
- [x] Add User domain with Basic info
- [x] Support for JWT Auth
- [x] Alembic DataBase Migration support
- [x] Basic test cases setup
- [x] Test cases for user domain (SSO/3rd party login not implemented yet)
- [X] Docker support
- [X] pre-commit for code formatting and best practices checks
- [X] `requirements.txt` file and `dev-requirements.txt` files for row and exact requirements

<br>

# Run the Project Using UVcorn

### Create virtual env and activate it

    python3 -m venv venv
    source venv/bin/activate

### Install the requirement

    pip install -r requirement.txt

### If this show any error in installation of any dependency install run bellow command
    pip install -r dev-requirement.txt

### Run Server
    uvicorn src.main:create_app --host 0.0.0.0 --port 8000 --reload --factory


# Docker Setup
    docker compose up --build
    docker compose  exec -it web /bin/bash

# Database Migration
Note: If any new entity added to the Project we need to add it to `alembic/env.py`.

Alembic Commands
### Create a new version fo migration
`alembic revision --autogenerate -m "v0.0 initial commit"`
### Upgrade the to newest version
`alembic upgrade head`

Note: Delete Tables and Data types from Database before migrating
Note: Delete Sqlalchemy versions scripts from versions folder
Note: One to one relationships return None when there's no data associated with particular relation. One to Many and others return empty list so, keep checking if None in one to one before accessing db object's attributes

# Docker Debug Endpoint using breakpoint

1. Start the Container in detached mode

- `docker compose up -d --build`

2. List docker running containers and get the id of the container you want to debug

- `docker container ps`

3. Attach a debugger to the container

- `docker attach <container ID>`

4. Add 'breakpoint()' in endpoint and hit the endpoint to stop at the breakpoint

# Run pytest

```
python -m pytest tests/ --cov=src/ --cov-fail-under=100 -v
```
