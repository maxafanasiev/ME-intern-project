before run, you need to rename .env.example file and insert you credentials into it

start uvicorn command       -> "python app/main.py"

run tests                   -> "pytest"

create docker image         -> "docker build -t me-intern-fastapi ."
run docker container        -> "docker run -d -p ${SERVER_PORT:-8000}:8000 --name fastapiapp me-intern-fastapi"

