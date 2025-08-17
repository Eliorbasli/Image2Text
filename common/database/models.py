from datetime import datetime
from sqlalchemy import String, DateTime, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from common.database.db_connection import Base


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)  # uuid4 as str
    status: Mapped[str] = mapped_column(String(20), index=True)    # queued|processing|done|failed
    file_path: Mapped[str] = mapped_column(Text)                   
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )

    result: Mapped["JobResult"] = relationship(back_populates="job", uselist=False)


class JobResult(Base):
    __tablename__ = "job_results"

    job_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("jobs.id", ondelete="CASCADE"),
        primary_key=True,
    )
    text: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    job: Mapped[Job] = relationship(back_populates="result")
