"""
Task queue manager using Celery
"""
from celery import Celery
from celery.result import AsyncResult
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

celery_app = Celery(
    'autocloud',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)


class TaskQueue:
    """Manage asynchronous tasks"""
    
    def __init__(self):
        self.app = celery_app
    
    def enqueue(self, task_name: str, *args, **kwargs) -> str:
        """Enqueue a task"""
        task = self.app.send_task(task_name, args=args, kwargs=kwargs)
        logger.info(f"Enqueued task: {task_name} with ID: {task.id}")
        return task.id
    
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Get task status"""
        result = AsyncResult(task_id, app=self.app)
        return {
            'task_id': task_id,
            'status': result.state,
            'result': result.result if result.ready() else None
        }
    
    def cancel_task(self, task_id: str) -> bool:
        """Cancel a task"""
        self.app.control.revoke(task_id, terminate=True)
        logger.info(f"Cancelled task: {task_id}")
        return True
