# adengine engine image: MCP servers (dr :8770, gen :8771) + workers.
# ffmpeg / ffprobe / curl from apt, yt-dlp from pip. Boots with an empty HOME and no vault.
FROM python:3.12-slim

RUN apt-get update \
 && apt-get install -y --no-install-recommends ffmpeg curl ca-certificates \
 && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    ADENGINE_PACKAGES_DIR=/app/packages \
    ADENGINE_DATA_DIR=/data \
    ADENGINE_FFMPEG=/usr/bin/ffmpeg \
    ADENGINE_FFPROBE=/usr/bin/ffprobe \
    ADENGINE_CURL=/usr/bin/curl \
    ADENGINE_YTDLP=/usr/local/bin/yt-dlp \
    HOME=/nonexistent

WORKDIR /app
COPY services/engine/requirements.txt /app/services/engine/requirements.txt
RUN pip install -r /app/services/engine/requirements.txt yt-dlp

COPY services/engine /app/services/engine
COPY packages /app/packages

WORKDIR /app/services/engine
RUN mkdir -p /data && chmod 777 /data
VOLUME ["/data"]
EXPOSE 8770 8771

CMD ["python", "-m", "adengine.dr", "--http", "8770"]
