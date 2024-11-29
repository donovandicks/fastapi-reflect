import json

from fastapi_reflect.main import app

if __name__ == "__main__":
    schema = app.openapi()
    with open("./openapi.json", "w") as f:
        json.dump(schema, f)