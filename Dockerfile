FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

RUN useradd -ms /bin/bash appuser

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        default-libmysqlclient-dev \
        build-essential \
        pkg-config \
        python3-dev \
        default-mysql-client \
        curl \
        gcc \
        libpq-dev \
#        nginx \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

#RUN mkdir -p /var/lib/nginx/body /var/lib/nginx/proxy /var/lib/nginx/fastcgi /var/lib/nginx/uwsgi /var/lib/nginx/scgi \
#    && chown -R appuser:appuser /var/lib/nginx \
#    && chmod -R 755 /var/lib/nginx \
#    && chown -R appuser:appuser /var/log/nginx \
#    && chmod -R 755 /var/log/nginx

WORKDIR /src

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get purge -y build-essential gcc \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY src/ /src/
#COPY nginx.conf /etc/nginx/nginx.conf
#
#RUN mkdir -p /src/run \
#    && touch /src/run/nginx.pid \
#    && chown -R appuser:appuser /src \
#    && chmod -R 755 /src/run \
#    && chmod 644 /etc/nginx/nginx.conf

USER appuser

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn --bind 0.0.0.0:8000 config.wsgi:application"]

#CMD ["sh", "-c", "python manage.py migrate && \
#    python manage.py collectstatic --noinput && \
#    chmod -R 755 /src/staticfiles && \
#    gunicorn --bind 127.0.0.1:8000 --log-level debug config.wsgi:application & \
#    nginx -g 'daemon off;'"]