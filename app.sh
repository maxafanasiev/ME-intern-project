#!/bin/bash

alembic upgrade heads

python3 app/main.py