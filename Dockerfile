FROM python:3.11-slim

RUN useradd -m appuser

WORKDIR /app

COPY requirements.txt requirements-dev.txt ./

RUN pip install --no-cache-dir -r requirements.txt -r requirements-dev.txt

COPY app ./app
COPY data ./data

RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 6767

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${APP_PORT} --reload"]
