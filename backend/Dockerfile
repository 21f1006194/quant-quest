FROM python:3.11-slim

WORKDIR /app

# System dependencies for psycopg2 and gunicorn
RUN apt-get update && \
    apt-get install -y gcc libpq-dev postgresql-client && \
    apt-get clean

# Install Python packages in one layer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

RUN chmod +x entrypoint.sh

# Entry point handles migration & boot
ENTRYPOINT ["./entrypoint.sh"]
