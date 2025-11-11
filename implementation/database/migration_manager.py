"""
Database migration manager using Alembic
"""
from alembic import command
from alembic.config import Config
import logging
import os

logger = logging.getLogger(__name__)


class MigrationManager:
    """Manage database migrations"""
    
    def __init__(self, alembic_ini_path: str = 'alembic.ini'):
        self.alembic_cfg = Config(alembic_ini_path)
    
    def create_migration(self, message: str):
        """Create a new migration"""
        try:
            command.revision(self.alembic_cfg, message=message, autogenerate=True)
            logger.info(f"Migration created: {message}")
        except Exception as e:
            logger.error(f"Failed to create migration: {str(e)}")
            raise
    
    def upgrade(self, revision: str = 'head'):
        """Upgrade database to a revision"""
        try:
            command.upgrade(self.alembic_cfg, revision)
            logger.info(f"Database upgraded to: {revision}")
        except Exception as e:
            logger.error(f"Failed to upgrade database: {str(e)}")
            raise
    
    def downgrade(self, revision: str):
        """Downgrade database to a revision"""
        try:
            command.downgrade(self.alembic_cfg, revision)
            logger.info(f"Database downgraded to: {revision}")
        except Exception as e:
            logger.error(f"Failed to downgrade database: {str(e)}")
            raise
    
    def current(self):
        """Show current revision"""
        try:
            command.current(self.alembic_cfg)
        except Exception as e:
            logger.error(f"Failed to get current revision: {str(e)}")
            raise
    
    def history(self):
        """Show migration history"""
        try:
            command.history(self.alembic_cfg)
        except Exception as e:
            logger.error(f"Failed to get migration history: {str(e)}")
            raise
