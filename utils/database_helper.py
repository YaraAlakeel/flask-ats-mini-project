# utils/database_helper.py
import os
import psycopg2#A PostgreSQL database adapter for Python.
from psycopg2 import sql
from dotenv import load_dotenv

class Database:
    '''
        def __init__(self): #initializes the connection to the PostgreSQL database using the connection string stored in the DATABASE_URL environment variable.
        self.conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    '''

    def __init__(self):
        # Retrieve the DATABASE_URL environment variable
        database_url = os.getenv('DATABASE_URL')

        try:
            # Establish a connection to the PostgreSQL database
            self.conn = psycopg2.connect(database_url)
            print("Database connection established successfully")
        except psycopg2.Error as e:
            print(f"Error connecting to database: {e}")
            raise e

    def execute_query(self, query, params=None, fetch_all=False):
        cur = self.conn.cursor()
        cur.execute(query, params)

        if fetch_all:
            result = cur.fetchall()
        else:
            result = cur.fetchone()

        cur.close()
        return result

    def add(self, query, params):#now it takes query not column and tabels
        cur = self.conn.cursor()
        cur.execute(query, params)
        id = cur.fetchone()[0] #to return the id of the inserted query
        self.conn.commit()
        cur.close()
        return id

    def delete(self, query, params=None):
        self.execute_query(query, params)# when we use it we pass to it the delet query function and the delete parameters

    def update(self, query, params=None):
        self.execute_query(query, params)

    def close(self):
        self.conn.close()
