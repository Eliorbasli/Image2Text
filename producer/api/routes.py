import uuid
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Response
from starlette.background import BackgroundTasks

from common.config import settings
from common.database.db_connection import get_db
from common.database import crud

from common.rabbitmq.connection import get_connection
from common.rabbitmq.helpers import publish_job
from common.status_enum import JobStatus
from producer.api.schemas.job_schema import (
    JobCreateResponse,
    JobStatusResponse,
    JobResultResponse,
)
router = APIRouter()



def _generate_unique_job_id(db, max_attempts: int = 5) -> str:
    for _ in range(max_attempts):
        candidate = str(uuid.uuid4())
        if not crud.job_exists(db, candidate):
            return candidate
    
    raise HTTPException(status_code=500, detail="Failed to allocate unique job_id")



@router.post("/submit" , response_model=JobCreateResponse , description="Accepts an image file and returns a job_id")
async def submit_image(
    background: BackgroundTasks,
    file: UploadFile = File(...),
    db=Depends(get_db),
):
    if file.content_type not in {"image/jpeg", "image/png"}:
        raise HTTPException(status_code=400, detail="Only JPG or PNG are supported")

    job_id = _generate_unique_job_id(db)

    # Save file to file system
    suffix = ".jpg" if file.content_type == "image/jpeg" else ".png"
    target_path = Path(settings.upload_dir) / f"{job_id}{suffix}"
    
    target_path.parent.mkdir(parents=True, exist_ok=True)
    content = await file.read()
    with target_path.open("wb") as out:
        out.write(content)

    job = crud.create_job(db, job_id=job_id, file_path=str(target_path))

    print(f"publish to RabbitMQ: {job.id} -> {target_path}")
    background.add_task(publish_job_message, job_id=job.id, file_path=str(target_path))

    return {"job_id": job.id}


async def publish_job_message(*, job_id: str, file_path: str):
    payload = {
        "job_id": job_id,
        "file_path": file_path,
        "routing_reason": "image_submitted",
    }

    queue_conn = await get_connection()
    try:
        await publish_job(payload=payload)
        print(f"publish_job_message: sucess to publish {job_id}")
    except Exception as e:
        print(f"publish_job_message: failed to publish {job_id}, error : {e}")
    finally:
        await queue_conn.close()


@router.get("/status/{job_id}" , response_model=JobStatusResponse, description="Retrieve the current status of a job (queued, processing, done, failed) and its associated metadata.")
def get_job(job_id: str, db=Depends(get_db)):
    job = crud.get_job(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return {
        "job_id": job.id,
        "status": job.status,
        "file_path": job.file_path,
    }


@router.get("/result/{job_id}" , response_model=JobResultResponse)
def get_result(job_id: str, db=Depends(get_db)):
    job = crud.get_job(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    if job.status != JobStatus.DONE.value:
        raise HTTPException(status_code=202, detail=f"Job status is '{job.status}'")

    jr = crud.get_job_result(db, job_id)
    if not jr:
        raise HTTPException(status_code=500, detail="Result missing")

    return Response(content=jr.text, media_type="text/plain")
