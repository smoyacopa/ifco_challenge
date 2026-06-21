FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY tests/ ./tests/
COPY data/ ./data/

ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1

CMD ["python", "-m", "pytest", "tests/", "-v", "-o", "cache_dir=/tmp/.pytest_cache"]
