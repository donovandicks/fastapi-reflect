dev:
  uv run --env-file .env -- fastapi dev ./src/fastapi_reflect/main.py

run:
  uv run --env-file .env -- fastapi run ./src/fastapi_reflect/main.py

