from sqlalchemy import create_engine, table, column
from sqlalchemy.dialects.postgresql import insert
import psycopg2
from psycopg2 import pool
import os
from dotenv import load_dotenv
import elasticapm
from elasticapm.traces import capture_span

load_dotenv()

postgres_config = {
    'host': os.getenv('POSTGRES_HOST'),
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'database': os.getenv('POSTGRES_DATABASE')
}

table_log = table('log',
    column('message')
)

# Instrument psycopg2
elasticapm.instrument()

threaded_conn_pool = psycopg2.pool.ThreadedConnectionPool(
    minconn=10,
    maxconn=20,
    **postgres_config
)

def get_db_connection(key=None):
    """Get a connection from the pool with an optional key"""
    with capture_span("postgresql-get-connection", "db.postgresql.connect"):
        return threaded_conn_pool.getconn(key=key)

def put_db_connection(conn, key=None):
    """Return a connection to the pool with an optional key"""
    with capture_span("postgresql-put-connection", "db.postgresql.connect"):
        threaded_conn_pool.putconn(conn, key=key)

def connect_psql(config=postgres_config):
    """ Connect to the PostgreSQL database server """
    with capture_span("postgresql-connect", "db.postgresql.connect"):
        try:
            # connecting to the PostgreSQL server
            with psycopg2.connect(**config) as conn:
                print('Connected to the PostgreSQL server.')
                return conn
        except (psycopg2.DatabaseError, Exception) as error:
            print(error)

def execute_query_psql(query, config, database):
    """ Insert data into a table """
    with capture_span("postgresql-query", "db.postgresql.query", {'query': str(query)}):
        conn_string = 'postgresql://' + config['user'] + ':' + config['password'] + '@' + config['host'] + '/' + database
        try:
            db = create_engine(conn_string)
            with db.begin() as conn:
                res = conn.execute(query)
                return res.rowcount
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
