import logging
from rq import Worker
from rq.job import JobStatus
import redis
from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


def start_workers():
    """Start RQ workers for background jobs"""
    try:
        redis_conn = redis.from_url(settings.redis_url)
        worker = Worker([settings.queue_name], connection=redis_conn)
        logger.info("✓ RQ Worker started")
        worker.work()
    except Exception as e:
        logger.error(f"Worker error: {str(e)}")


if __name__ == "__main__":
    start_workers()
