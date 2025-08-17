from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import select
from common.database.models import Job, JobResult
from common.status_enum import JobStatus

def create_job(db: Session, *, job_id: str, file_path: str) -> Job:
    job = Job(id=job_id, status=JobStatus.QUEUED.value, file_path=file_path)
    db.add(job)
    db.commit()
    db.refresh(job)
    return job

def get_job(db: Session, job_id: str) -> Job | None:
    return db.get(Job, job_id)

def update_job_status(db: Session, job_id: str, *, status: str) -> Job | None:
    job = db.get(Job, job_id)
    if not job:
        return None
    job.status = status
    job.updated_at = datetime.now()
    db.commit()
    db.refresh(job)
    return job

def job_exists(db: Session, job_id: str) -> bool:
    return db.scalar(select(Job.id).where(Job.id == job_id)) is not None

def upsert_job_result(db: Session, job_id: str, text: str) -> JobResult:
    existing = db.get(JobResult, job_id)
    if existing:
        existing.text = text
        existing.created_at = datetime.now()
        db.commit()
        db.refresh(existing)
        return existing
    
    jr = JobResult(job_id=job_id, text=text)
    db.add(jr)
    db.commit()
    db.refresh(jr)
    return jr

def get_job_result(db: Session, job_id: str) -> JobResult | None:
    return db.get(JobResult, job_id)
