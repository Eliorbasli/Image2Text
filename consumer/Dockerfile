FROM python:3.12-slim

WORKDIR /app
ENV PYTHONPATH=/app

COPY consumer/requirements.txt /app/consumer/requirements.txt
RUN pip install --no-cache-dir -r /app/consumer/requirements.txt

COPY common/ /app/common/
COPY consumer/ /app/consumer/

RUN mkdir -p /app/data/uploads

CMD ["python", "-u", "-m", "consumer.worker"]
