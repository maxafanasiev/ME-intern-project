before run, you need to rename .env.example file and insert you credentials into it

start uvicorn command       -> "python app/main.py"

run tests                   -> "pytest"


create app docker image     -> "docker build -t fastapiapp -f Dockerfile ."
create tests docker image   -> "docker build -t me-tests -f Dockerfile.tests ."
create docker network       -> "docker network create api_net"

run app docker container    -> "docker run -d --network api_net -p ${SERVER_PORT}:8000 --name fastapiapp fastapiapp ."

run test docker container   -> "docker run -it --network api_net --name me-tests me-tests ."

run docker-compose          -> "docker-compose up"
rebuild                     -> "docker-compose up -d --build"
stop docker-compose         -> "docker-compose down"

make alembic migration      -> "alembic revision --autogenerate -m 'Init'"
apply alembic migrations    -> "alembic upgrade heads"

