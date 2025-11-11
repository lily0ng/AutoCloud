"""
Task scheduling service using APScheduler
"""
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
import logging

logger = logging.getLogger(__name__)


class SchedulerService:
    """Manage scheduled tasks"""
    
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.jobs = {}
    
    def start(self):
        """Start the scheduler"""
        if not self.scheduler.running:
            self.scheduler.start()
            logger.info("Scheduler started")
    
    def shutdown(self):
        """Shutdown the scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Scheduler shutdown")
    
    def add_cron_job(self, func, job_id: str, cron_expression: str, **kwargs):
        """Add cron-based job"""
        try:
            trigger = CronTrigger.from_crontab(cron_expression)
            job = self.scheduler.add_job(
                func,
                trigger=trigger,
                id=job_id,
                replace_existing=True,
                **kwargs
            )
            self.jobs[job_id] = job
            logger.info(f"Cron job added: {job_id} - {cron_expression}")
            return job
        except Exception as e:
            logger.error(f"Failed to add cron job: {str(e)}")
            raise
    
    def add_interval_job(self, func, job_id: str, seconds: int, **kwargs):
        """Add interval-based job"""
        try:
            job = self.scheduler.add_job(
                func,
                trigger=IntervalTrigger(seconds=seconds),
                id=job_id,
                replace_existing=True,
                **kwargs
            )
            self.jobs[job_id] = job
            logger.info(f"Interval job added: {job_id} - every {seconds}s")
            return job
        except Exception as e:
            logger.error(f"Failed to add interval job: {str(e)}")
            raise
    
    def remove_job(self, job_id: str):
        """Remove scheduled job"""
        try:
            self.scheduler.remove_job(job_id)
            if job_id in self.jobs:
                del self.jobs[job_id]
            logger.info(f"Job removed: {job_id}")
        except Exception as e:
            logger.error(f"Failed to remove job: {str(e)}")
    
    def get_jobs(self):
        """Get all scheduled jobs"""
        return self.scheduler.get_jobs()
    
    def pause_job(self, job_id: str):
        """Pause a job"""
        self.scheduler.pause_job(job_id)
        logger.info(f"Job paused: {job_id}")
    
    def resume_job(self, job_id: str):
        """Resume a paused job"""
        self.scheduler.resume_job(job_id)
        logger.info(f"Job resumed: {job_id}")
