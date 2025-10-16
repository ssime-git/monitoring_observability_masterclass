from sqlalchemy import create_engine, table, column
from sqlalchemy.dialects.postgresql import insert
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

postgres_config = {
    'host': os.getenv('POSTGRES_HOST'),
    #'user': os.getenv('POSTGRES_USER'),
    #'password': os.getenv('POSTGRES_PASSWORD'),
    #'database': os.getenv('POSTGRES_DATABASE')
    'user': 'suppliers',
    'password': 'suppliers',
    'database': 'suppliers'
}

table_log = table('log',
    column('message')
)

def connect_psql(config=postgres_config):
    """ Connect to the PostgreSQL database server """
    try:
        # connecting to the PostgreSQL server
        with psycopg2.connect(**config) as conn:
            print('Connected to the PostgreSQL server.')
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def execute_query_psql(query, config, database):
    """ Insert data into a table """
    conn_string = 'postgresql://' + config['user'] + ':' + config['password'] + '@' + config['host'] + '/' + database
    try:
        db = create_engine(conn_string)
        with db.begin() as conn:
            res = conn.execute(query)
            return res.rowcount
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
