import asyncio

from consumer.helpers import (
    fetch_payload,
    validate_payload,
    process_job,
    EMPTY_SLEEP
)

async def consume() -> None:
    print("Polling queue image_jobs..")
    while True:
        payload = await fetch_payload()
        
        if payload is None:
            await asyncio.sleep(EMPTY_SLEEP)
            continue

        print("### QUEUE ITEM ###")
        print(payload)

        try:
            job_id, file_path = validate_payload(payload)
        except ValueError as e:
            print(f"error: {e}")
            await asyncio.sleep(0.5)
        
        try:
            print("Processing job:", job_id)
            await process_job(job_id, file_path)
            print(f"## Job {job_id} processed successfully")
                
        except Exception as e:
            
            print(f"Job {job_id} failed")
            await asyncio.sleep(EMPTY_SLEEP)


if __name__ == "__main__":
    asyncio.run(consume())