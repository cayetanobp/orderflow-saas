#!/bin/sh
set -eu

python manage.py migrate --noinput
python manage.py collectstatic --noinput

if [ "${RUN_DEMO_SEED:-false}" = "true" ]; then
	python manage.py seed_demo
fi

exec "$@"