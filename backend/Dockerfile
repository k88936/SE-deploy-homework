FROM python:3.8-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1 \
	PIP_DISABLE_PIP_VERSION_CHECK=on \
	PIP_NO_CACHE_DIR=on

WORKDIR /app

# Switch Debian apt sources to Tsinghua mirrors for faster downloads in CN
# Debian (slim) uses deb.debian.org and security.debian.org by default
# Replace them before running apt-get update. Handle both sources.list and new-style debian.sources when present.
RUN set -eux; \
		if [ -f /etc/apt/sources.list ]; then \
			sed -i -e 's|http://deb.debian.org|https://mirrors.tuna.tsinghua.edu.cn|g' \
						 -e 's|https://deb.debian.org|https://mirrors.tuna.tsinghua.edu.cn|g' \
						 -e 's|http://security.debian.org|https://mirrors.tuna.tsinghua.edu.cn/debian-security|g' \
						 -e 's|https://security.debian.org|https://mirrors.tuna.tsinghua.edu.cn/debian-security|g' /etc/apt/sources.list; \
		fi; \
		if [ -d /etc/apt/sources.list.d ]; then \
			find /etc/apt/sources.list.d -type f -name '*.list' -print0 | xargs -0 -r sed -i \
				-e 's|http://deb.debian.org|https://mirrors.tuna.tsinghua.edu.cn|g' \
				-e 's|https://deb.debian.org|https://mirrors.tuna.tsinghua.edu.cn|g' \
				-e 's|http://security.debian.org|https://mirrors.tuna.tsinghua.edu.cn/debian-security|g' \
				-e 's|https://security.debian.org|https://mirrors.tuna.tsinghua.edu.cn/debian-security|g' || true; \
		fi; \
		if [ -f /etc/apt/sources.list.d/debian.sources ]; then \
			sed -i -e 's|http://deb.debian.org|https://mirrors.tuna.tsinghua.edu.cn|g' \
						 -e 's|https://deb.debian.org|https://mirrors.tuna.tsinghua.edu.cn|g' \
						 -e 's|http://security.debian.org|https://mirrors.tuna.tsinghua.edu.cn/debian-security|g' \
						 -e 's|https://security.debian.org|https://mirrors.tuna.tsinghua.edu.cn/debian-security|g' /etc/apt/sources.list.d/debian.sources || true; \
		fi; \
		apt-get update \
	&& apt-get install -y --no-install-recommends \
	   build-essential \
	   default-libmysqlclient-dev \
	   pkg-config \
	   curl \
	&& rm -rf /var/lib/apt/lists/*

# Install python deps
COPY requirements.txt ./
# Configure pip to use TUNA PyPI mirror for faster installs
RUN printf "[global]\nindex-url = https://pypi.tuna.tsinghua.edu.cn/simple\ntrusted-host = pypi.tuna.tsinghua.edu.cn\n" > /etc/pip.conf \
	&& pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static files if used by Django apps (safe no-op if none)
# RUN DJANGO_SETTINGS_MODULE=app.settings_prod python manage.py collectstatic --noinput || true

# Gunicorn default port (backend listens internal 8000)
EXPOSE 8000

# Entrypoint will create migrations, migrate, optional seed, then start gunicorn
CMD ["bash", "-lc", "python manage.py makemigrations app post user && python manage.py migrate --settings=app.settings_prod && if [ \"${INIT_DB:-false}\" = \"true\" ]; then python manage.py init_db; fi; DJANGO_SETTINGS_MODULE=app.settings_prod gunicorn -w 4 -b 0.0.0.0:8000 app.wsgi:application --log-level=info"]
