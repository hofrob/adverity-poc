#!/bin/bash

set -e

(
  trap 'kill 0; wait' SIGINT
  uv run uvicorn --port 8010 "app_poc_api.main:start" --reload --use-colors --factory &
  cd ts && npm run dev
)
