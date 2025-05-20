FROM python:3.11-slim

WORKDIR /app

# Install cron
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

# Copy application files
COPY .env . 
COPY adzuna_ads_yesterday.py .
COPY requirements.txt .
COPY crontab /etc/cron.d/adzuna-cron

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set correct permissions and register the crontab
RUN chmod 0644 /etc/cron.d/adzuna-cron && \
    crontab /etc/cron.d/adzuna-cron

# Create the log file that cron will write to
RUN touch /app/adzuna_cron.log

# Start cron in foreground
CMD ["cron", "-f"]
