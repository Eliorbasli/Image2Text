FROM python:3.12-slim

WORKDIR /app

# install deps
COPY producer/requirements.txt /app/producer/requirements.txt
RUN pip install --no-cache-dir -r /app/producer/requirements.txt

# copy code
COPY common/ /app/common/
COPY producer/ /app/producer/

# runtime data dir
RUN mkdir -p /app/data/uploads

EXPOSE 8000
CMD ["uvicorn", "producer.app:app", "--host", "0.0.0.0", "--port", "8000"]
