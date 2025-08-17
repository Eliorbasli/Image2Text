Asynchronous Image Processing Service
Overview

This project provides an asynchronous service to process image files (JPG/PNG) and extract text from them.
It is built with FastAPI, RabbitMQ, and SQLite, wrapped in Docker for easy setup.

Producer: FastAPI app for submitting images and querying job status/results

Consumer: Worker service that consumes jobs from RabbitMQ, extracts text, and stores results in the database

Common: Shared utilities (DB models, config, RabbitMQ, and Enums)

How to Run

Clone & navigate into the project:

git clone https://github.com/Eliorbasli/Image2Text.git
cd image2text


Create a .env file in the root folder with your configuration.

Build and start the services:

docker compose up --build


This will start:

RabbitMQ (UI at http://localhost:15672, user/pass = guest / guest)

Producer API (FastAPI) on http://localhost:8000

Consumer worker

To view logs:

docker compose logs -f consumer
docker compose logs -f producer

API Endpoints
1. Submit a new image job

POST /submit
Upload a JPG/PNG image for text extraction.

Input: multipart/form-data with field file
Response: JSON containing job_id

2. Get job status

GET /status/{job_id}
Check if the job is queued, processing, done, or failed.

3. Get job result

GET /result/{job_id}
If the job is done, returns the extracted text.

Testing the API

A sample Python client is included:

cd tests
python python_client.py


Sample images are available in tests/sample_images/.
