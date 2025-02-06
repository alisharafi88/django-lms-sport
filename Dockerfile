FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

RUN useradd -ms /bin/bash appuser

WORKDIR /src

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
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ /src/
RUN chown -R appuser:appuser /src

USER appuser

EXPOSE 8000
