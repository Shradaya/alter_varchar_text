import psycopg2
from config import config
from simple_colors import *


def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    params = config()
    errors = []
    try:
        conn = psycopg2.connect(host='localhost',
                                database='postgres',
                                user='postgres',
                                password='newpassword') 
        # conn = psycopg2.connect(host=params['host'],
        #                         database=params['database'],
        #                         user=params['user'],
        #                         password=params['password'],
        #                         port= int(params['port']))
        print("Connection has been established .... \n")
    except (Exception, psycopg2.DatabaseError) as err:
        print("Error connecting to the database ....")
        errors.append(err)
    return errors, conn

def disconnect(cur):
    cur.close()
    print("Disconnected from the database server .... \n")

def execute_query(cur, query):
    errors = []
    try:
        cur.execute(query)
    except Exception as err:
        print(f"Error While Executing Query at Query :: {query}")
        errors.append(err)
    return errors

def fetch_db_result(cur, query):
    errors = []
    try:
        cur.execute(query)
        result = cur.fetchall()
    except Exception as err:
        errors.append(err)
    return errors, result


    