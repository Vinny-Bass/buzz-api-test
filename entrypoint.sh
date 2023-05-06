#!/bin/bash

# If fails don't execute anything else
set -e

# Set the DATABASE_URL environment variable
export DATABASE_URL="postgresql+asyncpg://buzz:buzz@db:5432/buzz_db"

# Run the application with uvicorn
if [ "$RUN_INIT_DB" = "1" ]; then
  python init_db.py
  python main.py
else
  exec uvicorn main:app --host 0.0.0.0 --port 8000
fi