# PoC for FastAPI / Async / SQLAlchemy ORM

Requirements:
- make
- docker
- uv: https://docs.astral.sh/uv/getting-started/installation/

`uv` will take care of the python version, venv and dependencies.

To see it in action, run `make db_reset` and then `make serve`.

API docs: http://localhost:8010/docs
react app: http://localhost:5173/
