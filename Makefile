docker_directory = docker

db_reset: db_down db_start db_migrate

db_down:
	cd $(docker_directory) && docker compose down --volumes

db_start:
	cd $(docker_directory) && docker compose build && docker compose up --detach --force-recreate

db_migrate:
	@until uv run alembic upgrade heads; do echo "migration failed. Retrying..."; sleep 1; done

serve:
	./serve.sh

