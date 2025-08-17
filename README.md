# Asynchronous Image Processing Service

## Overview
This project provides an asynchronous service to process image files (JPG/PNG) and extract text from them.  
It is built with **[FastAPI](https://fastapi.tiangolo.com/)**, **[RabbitMQ](https://www.rabbitmq.com/)**, and **SQLite**, wrapped in **Docker** for easy setup.

- **Producer**: FastAPI app for submitting images and querying job status/results  
- **Consumer**: Worker service that consumes jobs from RabbitMQ, extracts text, and stores results in the database  
- **Common**: Shared utilities (DB models, config, RabbitMQ, and Enums)  

<img width="871" height="541" alt="Image2Text Diagram" src="https://github.com/user-attachments/assets/5e0cf3b6-30ed-4478-a9e3-59e9e2c70dde" />


---

## How to Run

1. **Clone & navigate into the project**
   ```bash
   git clone https://github.com/Eliorbasli/Image2Text.git
   cd image2text
   ```

2. **Create a `.env` file** in the root folder with your configuration:
   ```env
   AMQP_URL=amqp://guest:guest@rabbitmq:5672/
   SQLITE_PATH=/data/app.db
   UPLOAD_DIR=/data/uploads
   API_NINJAS_KEY = *****************
   ```

3. **Build and start the services**
   ```bash
   docker compose up --build
   ```

   âœ… This will start:
   - **RabbitMQ** â†’ [http://localhost:15672](http://localhost:15672) (`guest/guest`)  
   - **Producer API (FastAPI)** â†’ [http://localhost:8000](http://localhost:8000)  
   - **Consumer worker**

   To view logs:
   ```bash
   docker compose logs -f consumer
   docker compose logs -f producer
   ```

---

## API Endpoints

### 1. Submit a new image job
`POST /submit`  
Upload a JPG/PNG image for text extraction.  

**Input:** multipart/form-data with field `file`  

**Response:** JSON containing `job_id`  

Example with [cURL](https://curl.se/):  
```bash
curl -X POST "http://localhost:8000/submit" \
  -F "file=@tests/sample_images/test.png"
```

---

### 2. Get job status
`GET /status/{job_id}`  

Check if the job is `queued`, `processing`, `done`, or `failed`.  

Response:
```json
{
  "job_id": "1234-uuid",
  "status": "processing"
}
```

---

### 3. Get job result
`GET /result/{job_id}`  

If the job is done, return the extracted text.  

Response:
```json
{
  "job_id": "1234-uuid",
  "result": "Detected text from image..."
}
```

---

## Testing the API

A sample Python client is included:  

```bash
cd tests
python python_client.py
```

Sample images are available in:  
<img width="1876" height="457" alt="image" src="https://github.com/user-attachments/assets/b6800077-8dea-4b4a-9831-242505ff5574" />
  

---

## UI Previews

- RabbitMQ Management

- FastAPI Docs:  
