
from common.rabbitmq.helpers import read_one_json
from common.database.db_connection import get_db
from common.database import crud

from common.status_enum import JobStatus
from consumer.image_to_text_service import extract_text_from_image
from typing import Any, Optional, Tuple
API_URL = "https://api.api-ninjas.com/v1/imagetotext"

EMPTY_SLEEP   = 0.5   # when queue is empty
READ_ERR_SLEEP = 1.0  # when we fail to read from queue
BAD_PAYLOAD_SLEEP = 0.2  # when payload is missing fields

async def fetch_payload() -> Optional[dict[str, Any]]:
    try:
        return await read_one_json()
    except Exception:
        return None
    
def validate_payload(payload: dict[str, Any]) -> Tuple[str, str]:
    job_id = payload.get("job_id") or payload.get("id")
    file_path = payload.get("file_path")
    
    if not job_id or not file_path:
        raise ValueError(f"Invalid payload (job_id/file_path missing): {payload}")
    return job_id, file_path

async def process_job(job_id: str, file_path: str) -> None:
    try:
        db_gen = get_db()
        db_conn = next(db_gen)
        
        crud.update_job_status(db_conn, job_id, status=JobStatus.PROCESSING.value)
        print(f"Processing job {job_id} | path={file_path}")

        text = await extract_text_from_image(file_path=file_path)

        crud.upsert_job_result(db=db_conn, job_id=job_id, text=text)
        crud.update_job_status(db=db_conn, job_id=job_id, status=JobStatus.DONE.value)
        

    except Exception:
        try:
            crud.update_job_status(db_conn, job_id, status=JobStatus.FAILED.value)
        except Exception:
            print(f"Failed to mark job {job_id} as FAILED")
        raise