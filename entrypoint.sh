#!/bin/bash

# If fails don't execute anything else
set -e

# Run database migrations
echo "Running database migrations...ss"
python main.py init_db

# Run the application
exec uvicorn app:app --host 0.0.0.0 --port 8000
