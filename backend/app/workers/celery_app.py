"""Celery worker configuration - placeholder"""

from celery import Celery
from app.core.config import settings

# Create Celery app
celery_app = Celery(
    "autoreels_ai",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)


# TODO: Implement actual tasks
# @celery_app.task
# def process_video_task(video_job_id: int):
#     """Process video and generate reels"""
#     pass

# @celery_app.task
# def upload_reel_task(reel_id: int):
#     """Upload reel to Instagram"""
#     pass
