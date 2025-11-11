#!/usr/bin/env python3
"""PostgreSQL Database Connection Manager"""

import psycopg2
from psycopg2 import pool
from contextlib import contextmanager
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, host, port, database, user, password, min_conn=1, max_conn=10):
        self.connection_pool = psycopg2.pool.SimpleConnectionPool(
            min_conn, max_conn,
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        logger.info("Database connection pool created")
    
    @contextmanager
    def get_connection(self):
        conn = self.connection_pool.getconn()
        try:
            yield conn
        finally:
            self.connection_pool.putconn(conn)
    
    def execute_query(self, query, params=None):
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                conn.commit()
                return cursor.fetchall()
    
    def close_all(self):
        self.connection_pool.closeall()
        logger.info("All database connections closed")

if __name__ == "__main__":
    db = DatabaseManager("localhost", 5432, "mydb", "user", "password")
    result = db.execute_query("SELECT version();")
    print(f"Database version: {result}")
    db.close_all()
