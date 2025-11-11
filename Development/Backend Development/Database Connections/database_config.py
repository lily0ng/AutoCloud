import os
from dotenv import load_dotenv
import boto3
import mysql.connector
import cx_Oracle
import pymongo
from cassandra.cluster import Cluster
from neo4j import GraphDatabase
import redis
from sqlalchemy import create_engine
from contextlib import contextmanager

# Load environment variables
load_dotenv()

class DatabaseConfig:
    def __init__(self):
        self.initialize_connections()

    def initialize_connections(self):
        """Initialize all database connections"""
        try:
            self.init_aws_s3()
            self.init_mysql()
            self.init_oracle()
            self.init_mongodb()
            self.init_cassandra()
            self.init_neo4j()
            self.init_redis()
        except Exception as e:
            print(f"Error initializing connections: {str(e)}")

    def init_aws_s3(self):
        """Initialize AWS S3 connection"""
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION', 'us-east-1')
        )

    def init_mysql(self):
        """Initialize MySQL connection pool"""
        self.mysql_pool = mysql.connector.pooling.MySQLConnectionPool(
            pool_name="mypool",
            pool_size=5,
            host=os.getenv('MYSQL_HOST'),
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASSWORD'),
            database=os.getenv('MYSQL_DATABASE')
        )

    def init_oracle(self):
        """Initialize Oracle connection"""
        self.oracle_dsn = cx_Oracle.makedsn(
            os.getenv('ORACLE_HOST'),
            os.getenv('ORACLE_PORT'),
            service_name=os.getenv('ORACLE_SERVICE')
        )
        self.oracle_pool = cx_Oracle.SessionPool(
            user=os.getenv('ORACLE_USER'),
            password=os.getenv('ORACLE_PASSWORD'),
            dsn=self.oracle_dsn,
            min=2,
            max=5,
            increment=1
        )

    def init_mongodb(self):
        """Initialize MongoDB connection"""
        self.mongo_client = pymongo.MongoClient(
            os.getenv('MONGODB_URI'),
            serverSelectionTimeoutMS=5000
        )

    def init_cassandra(self):
        """Initialize Cassandra connection"""
        self.cassandra_cluster = Cluster([os.getenv('CASSANDRA_HOST', 'localhost')])
        self.cassandra_session = self.cassandra_cluster.connect()

    def init_neo4j(self):
        """Initialize Neo4j connection"""
        self.neo4j_driver = GraphDatabase.driver(
            os.getenv('NEO4J_URI'),
            auth=(os.getenv('NEO4J_USER'), os.getenv('NEO4J_PASSWORD'))
        )

    def init_redis(self):
        """Initialize Redis connection"""
        self.redis_client = redis.Redis(
            host=os.getenv('REDIS_HOST', 'localhost'),
            port=int(os.getenv('REDIS_PORT', 6379)),
            db=0,
            decode_responses=True
        )

    @contextmanager
    def get_mysql_connection(self):
        """Get MySQL connection from pool"""
        connection = self.mysql_pool.get_connection()
        try:
            yield connection
        finally:
            connection.close()

    @contextmanager
    def get_oracle_connection(self):
        """Get Oracle connection from pool"""
        connection = self.oracle_pool.acquire()
        try:
            yield connection
        finally:
            self.oracle_pool.release(connection)

    def upload_to_s3(self, bucket_name, file_path, object_name=None):
        """Upload a file to S3 bucket"""
        if object_name is None:
            object_name = os.path.basename(file_path)
        try:
            self.s3_client.upload_file(file_path, bucket_name, object_name)
            return True
        except Exception as e:
            print(f"Error uploading to S3: {str(e)}")
            return False

    def close_all_connections(self):
        """Close all database connections"""
        try:
            self.mysql_pool.close()
            self.oracle_pool.close()
            self.mongo_client.close()
            self.cassandra_cluster.shutdown()
            self.neo4j_driver.close()
            self.redis_client.close()
        except Exception as e:
            print(f"Error closing connections: {str(e)}")

# Usage example
if __name__ == "__main__":
    db_config = DatabaseConfig()
    
    # Example MySQL query
    with db_config.get_mysql_connection() as mysql_conn:
        cursor = mysql_conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        print(f"MySQL test query result: {result}")
    
    # Close all connections when done
    db_config.close_all_connections()
