FROM python:3.8-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1 \
	PIP_DISABLE_PIP_VERSION_CHECK=on \
	PIP_NO_CACHE_DIR=on

WORKDIR /app

# System deps for mysqlclient and pillow etc.
RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
	   build-essential \
	   default-libmysqlclient-dev \
	   pkg-config \
	   curl \
	&& rm -rf /var/lib/apt/lists/*

# Install python deps
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static files if used by Django apps (safe no-op if none)
# RUN DJANGO_SETTINGS_MODULE=app.settings_prod python manage.py collectstatic --noinput || true

# Gunicorn default port (backend listens internal 8000)
EXPOSE 8000

# Entrypoint will create migrations, migrate, optional seed, then start gunicorn
CMD ["bash", "-lc", "python manage.py makemigrations app post user && python manage.py migrate --settings=app.settings_prod && if [ \"${INIT_DB:-false}\" = \"true\" ]; then python manage.py init_db; fi; DJANGO_SETTINGS_MODULE=app.settings_prod gunicorn -w 4 -b 0.0.0.0:8000 app.wsgi:application --log-level=info"]
