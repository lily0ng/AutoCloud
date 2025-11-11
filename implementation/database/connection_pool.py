"""
Database connection pool manager
"""
from sqlalchemy import create_engine, pool
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager
import logging

logger = logging.getLogger(__name__)


class DatabasePool:
    """Manage database connection pool"""
    
    def __init__(self, database_url: str, pool_size: int = 10, max_overflow: int = 20):
        self.engine = create_engine(
            database_url,
            poolclass=pool.QueuePool,
            pool_size=pool_size,
            max_overflow=max_overflow,
            pool_pre_ping=True,
            echo=False
        )
        
        self.SessionFactory = sessionmaker(bind=self.engine)
        self.Session = scoped_session(self.SessionFactory)
        
        logger.info(f"Database pool initialized: pool_size={pool_size}, max_overflow={max_overflow}")
    
    @contextmanager
    def get_session(self):
        """Get database session with automatic cleanup"""
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database session error: {str(e)}")
            raise
        finally:
            session.close()
    
    def execute_query(self, query: str, params: dict = None):
        """Execute raw SQL query"""
        with self.get_session() as session:
            result = session.execute(query, params or {})
            return result.fetchall()
    
    def get_pool_status(self):
        """Get connection pool status"""
        return {
            'pool_size': self.engine.pool.size(),
            'checked_in': self.engine.pool.checkedin(),
            'checked_out': self.engine.pool.checkedout(),
            'overflow': self.engine.pool.overflow()
        }
    
    def dispose(self):
        """Dispose of the connection pool"""
        self.engine.dispose()
        logger.info("Database pool disposed")
