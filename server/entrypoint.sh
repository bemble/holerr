#!/bin/sh

if [ -d ".venv" ]
then
    source ".venv/bin/activate"
fi
alembic upgrade head
python -m holerr