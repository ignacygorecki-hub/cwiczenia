FROM python:3.11-slim

# Install system deps (add more if needed for specific packages)
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirement files and install
COPY requirements.txt requirements-dev.txt ./
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

# Copy project
COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["python", "-m", "src.main"]
