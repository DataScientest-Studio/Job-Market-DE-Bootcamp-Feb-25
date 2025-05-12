FROM python:3.11-slim

WORKDIR /app

# Install cron
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

# Copy your script and crontab file
COPY adzuna_ads_yesterday.py .
COPY cron.txt /etc/cron.d/adzuna-cron

# Give execution rights
RUN chmod 0644 /etc/cron.d/adzuna-cron && \
    crontab /etc/cron.d/adzuna-cron

# Run cron in foreground
CMD ["cron", "-f"]
