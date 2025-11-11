"""
Generic repository pattern for database operations
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
import logging

logger = logging.getLogger(__name__)


class BaseRepository:
    """Base repository with common CRUD operations"""
    
    def __init__(self, model, session: Session):
        self.model = model
        self.session = session
    
    def create(self, **kwargs) -> Any:
        """Create a new record"""
        try:
            instance = self.model(**kwargs)
            self.session.add(instance)
            self.session.commit()
            self.session.refresh(instance)
            logger.info(f"Created {self.model.__name__}: {instance.id}")
            return instance
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error creating {self.model.__name__}: {str(e)}")
            raise
    
    def get_by_id(self, id: Any) -> Optional[Any]:
        """Get record by ID"""
        try:
            return self.session.query(self.model).filter(self.model.id == id).first()
        except Exception as e:
            logger.error(f"Error getting {self.model.__name__} by ID: {str(e)}")
            raise
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Any]:
        """Get all records with pagination"""
        try:
            return self.session.query(self.model).offset(skip).limit(limit).all()
        except Exception as e:
            logger.error(f"Error getting all {self.model.__name__}: {str(e)}")
            raise
    
    def get_by_field(self, field: str, value: Any) -> Optional[Any]:
        """Get record by specific field"""
        try:
            return self.session.query(self.model).filter(
                getattr(self.model, field) == value
            ).first()
        except Exception as e:
            logger.error(f"Error getting {self.model.__name__} by {field}: {str(e)}")
            raise
    
    def filter(self, filters: Dict[str, Any], skip: int = 0, limit: int = 100) -> List[Any]:
        """Filter records by multiple criteria"""
        try:
            query = self.session.query(self.model)
            
            for field, value in filters.items():
                if hasattr(self.model, field):
                    query = query.filter(getattr(self.model, field) == value)
            
            return query.offset(skip).limit(limit).all()
        except Exception as e:
            logger.error(f"Error filtering {self.model.__name__}: {str(e)}")
            raise
    
    def update(self, id: Any, **kwargs) -> Optional[Any]:
        """Update record by ID"""
        try:
            instance = self.get_by_id(id)
            if not instance:
                return None
            
            for key, value in kwargs.items():
                if hasattr(instance, key):
                    setattr(instance, key, value)
            
            self.session.commit()
            self.session.refresh(instance)
            logger.info(f"Updated {self.model.__name__}: {id}")
            return instance
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error updating {self.model.__name__}: {str(e)}")
            raise
    
    def delete(self, id: Any) -> bool:
        """Delete record by ID"""
        try:
            instance = self.get_by_id(id)
            if not instance:
                return False
            
            self.session.delete(instance)
            self.session.commit()
            logger.info(f"Deleted {self.model.__name__}: {id}")
            return True
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error deleting {self.model.__name__}: {str(e)}")
            raise
    
    def count(self, filters: Dict[str, Any] = None) -> int:
        """Count records with optional filters"""
        try:
            query = self.session.query(self.model)
            
            if filters:
                for field, value in filters.items():
                    if hasattr(self.model, field):
                        query = query.filter(getattr(self.model, field) == value)
            
            return query.count()
        except Exception as e:
            logger.error(f"Error counting {self.model.__name__}: {str(e)}")
            raise
    
    def exists(self, id: Any) -> bool:
        """Check if record exists"""
        return self.get_by_id(id) is not None
    
    def bulk_create(self, items: List[Dict]) -> List[Any]:
        """Create multiple records"""
        try:
            instances = [self.model(**item) for item in items]
            self.session.bulk_save_objects(instances)
            self.session.commit()
            logger.info(f"Bulk created {len(instances)} {self.model.__name__} records")
            return instances
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error bulk creating {self.model.__name__}: {str(e)}")
            raise
    
    def bulk_update(self, updates: List[Dict]) -> bool:
        """Update multiple records"""
        try:
            for update in updates:
                id = update.pop('id')
                self.update(id, **update)
            
            logger.info(f"Bulk updated {len(updates)} {self.model.__name__} records")
            return True
        except Exception as e:
            logger.error(f"Error bulk updating {self.model.__name__}: {str(e)}")
            raise
    
    def bulk_delete(self, ids: List[Any]) -> bool:
        """Delete multiple records"""
        try:
            self.session.query(self.model).filter(self.model.id.in_(ids)).delete(
                synchronize_session=False
            )
            self.session.commit()
            logger.info(f"Bulk deleted {len(ids)} {self.model.__name__} records")
            return True
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error bulk deleting {self.model.__name__}: {str(e)}")
            raise
    
    def search(self, search_term: str, fields: List[str], skip: int = 0, limit: int = 100) -> List[Any]:
        """Search records by term across multiple fields"""
        try:
            query = self.session.query(self.model)
            
            conditions = []
            for field in fields:
                if hasattr(self.model, field):
                    conditions.append(
                        getattr(self.model, field).ilike(f'%{search_term}%')
                    )
            
            if conditions:
                query = query.filter(or_(*conditions))
            
            return query.offset(skip).limit(limit).all()
        except Exception as e:
            logger.error(f"Error searching {self.model.__name__}: {str(e)}")
            raise
