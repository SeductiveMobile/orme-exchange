#!/bin/sh
echo "Waiting Postgres to start..."
while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
  sleep 0.1
done

echo "Postgres started, running migrations"

# First run custom migration script
python bin/migrate.py

# Afterwards run usual alembic migrations
alembic upgrade head
