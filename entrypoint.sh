#!/usr/bin/env bash
set -e

# Wait for Postgres if configured
if [ -n "${POSTGRES_HOST}" ]; then
  echo "Waiting for PostgreSQL at ${POSTGRES_HOST}:${POSTGRES_PORT:-5432}..."
  until python - <<END
import sys, socket, os
s=socket.socket()
h=os.environ.get('POSTGRES_HOST','localhost')
p=int(os.environ.get('POSTGRES_PORT','5432') or 5432)
try:
    s.connect((h,p))
    sys.exit(0)
except Exception as e:
    sys.exit(1)
END
  do
    sleep 1
  done
fi

python manage.py makemigrations --noinput || true
python manage.py migrate --noinput
python manage.py collectstatic --noinput || true

# Optional: seed data when SEED=true
if [ "$SEED" = "true" ]; then
  echo "Seeding initial data..."
  python manage.py seed || true
fi

# Start server
if [ "$DJANGO_ENV" = "development" ]; then
  exec python manage.py runserver 0.0.0.0:8000
else
  exec gunicorn catalog_project.wsgi:application --bind 0.0.0.0:8000 --workers ${GUNICORN_WORKERS:-3}
fi
