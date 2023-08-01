# Database
    Alembic Commands
    alembic revision --autogenerate -m "v0.0 initial commit"
    alembic upgrade head

Please do not delete any Version from alembic\versions or Table from DB.

# Naming convention to follow while making the new commit for DB.
    alembic revision --autogenerate -m "{VERSION FORMAT}"

### VERSION FORMAT
    v{major version}.{minor version} {relevant sort-comment}
