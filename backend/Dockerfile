FROM python:3.11-slim

WORKDIR /app

# System dependencies for psycopg2 and gunicorn
RUN apt-get update && \
    apt-get install -y gcc curl libpq-dev postgresql-client && \
    apt-get clean

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

RUN chmod +x scripts/entrypoint.prod.sh

# Entry point handles migration & boot
ENTRYPOINT ["./scripts/entrypoint.prod.sh"]
