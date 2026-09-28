FROM python:3.11-slim-bookworm
RUN apt-get update && apt-get install -y --no-install-recommends openjdk-17-jre-headless procps \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir "pyspark==4.0.*"
WORKDIR /app
COPY server.py .
EXPOSE 9000 4040
CMD ["python", "-u", "server.py"]
