#!/bin/bash

# Run database migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Start the application
gunicorn conf2025.wsgi:application --bind 0.0.0.0:$PORT
