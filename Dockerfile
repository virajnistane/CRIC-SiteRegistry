FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock ./
COPY src ./src

RUN pip install --no-cache-dir --upgrade pip uv && \
    uv export --locked --no-dev --no-emit-project --format requirements-txt -o requirements.txt && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir --no-deps -e .

COPY . .

CMD ["gunicorn", "site_registry.wsgi:application", "--bind", "0.0.0.0:8000"]