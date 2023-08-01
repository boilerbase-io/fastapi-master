# Run the Project Using UVcorn

- uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

Note:

- The environment variables are set with the .env file, therefore, not loading it in the Docker's Environment Variable
- Not keeping the Models ORM Classes and Pydantic's Schema classes with identical attributes, because some of the Models Attributes contain sensitive information
- Delete and Place gain Login Token Variable in the request to refresh the new login token pasted in the Postman Environment

# First Time Data Seeding in the Database

- The Seeding Data passwords should be normal passwords (and not hashed ones) in the seeding script
- The Seeding UUID Values all must be in the form of a UUID value only
- Need to sign up a user, manually make that user admin true in the database, and then access the seeding endpoint to seed the database

Commands:
docker compose up --build
docker compose  exec -it web /bin/bash

# Database

Alembic Commands
alembic revision --autogenerate -m "v0.0 initial commit"
alembic upgrade head

Note: Delete Tables and Data types from Database before migrating
Note: Delete Sqlalchemy versions scripts from versions folder
Note: One to one relationships return None when there's no data associated with particular relation. One to Many and others return empty list so, keep checking if None in one to one before accessing db object's attributes

Features

1. Account verification suggestions on login
2. 

Learnings:

- Keeping __init__.py file inside the directory has some disadvantages
  for example, when calling the import `<something>` from db.`<something>`.`<something>`, the __init__ file in db, calls all the other modules present in the directory, and we need to install non-needed dependencies even when just seeding

Session Token in the Header has to have - instead of _. Code can have _ and postman - at the same time and still it will match each other

# Docker Debug Endpoint using breakpoint

1. Start the Container in detached mode

- docker compose up -d --build

2. List docker running containers and get the id of the container you want to debug

- docker container ps

3. Attach a debugger to the container

- docker attach `<container ID>`

4. Add 'breakpoint()' in endpoint and hit the endpoint to stop at the breakpoint

## Naming Conventions

Table name: User_History (with underscore)
Schema name: UserHistory (withoutj underscore)

# Business Logic

- Decrease the Credit Usage rate(for services) according to the Frequency of User Credit Usage

# installation issues(ERROR) of psycopg2

- can be solved with this command :: sudo apt install python3-dev libpq-dev

# Run pytest

```
python -m pytest tests/ --cov=src/ --cov-fail-under=100 -v
```
