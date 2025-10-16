from sqlalchemy import create_engine, table, column
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.pool import QueuePool
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

postgres_config = {
    'host': os.getenv('POSTGRES_HOST'),
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'database': os.getenv('POSTGRES_DATABASE')
}

# Create a connection pool
def get_engine():
    conn_string = f"postgresql://{postgres_config['user']}:{postgres_config['password']}@{postgres_config['host']}/{postgres_config['database']}"
    return create_engine(
        conn_string,
        poolclass=QueuePool,
        pool_size=5,  # Number of permanent connections
        max_overflow=10,  # Number of additional connections when pool is full
        pool_timeout=30,  # Timeout for getting connection from pool
        pool_pre_ping=True  # Enable connection health checks
    )

# Global engine instance
engine = get_engine()

table_log = table('log',
    column('message')
)

def connect_psql(config=postgres_config):
    """ Get a connection from the pool """
    try:
        conn = engine.connect()
        print('Connected to the PostgreSQL server.')
        return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
    
def execute_query_psql(query, config, database):
    """ Execute query using the connection pool """
    try:
        with engine.begin() as conn:
            res = conn.execute(query)
            return res.rowcount
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
