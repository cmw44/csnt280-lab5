"""
create_db.py A program that demonstrates how to create a
database using the psycopg2 module.
"""
import psycopg2
conn_string = "host='localhost' dbname='cent280db' "
conn_string += " user='cent280man' password='pgsql_man'"
conn = psycopg2.connect(conn_string)
conn.autocommit = True
cursor = conn.cursor()
sql = "drop database if exists test_db;"
cursor.execute(sql)
sql = "create database test_db owner bob;"
cursor.execute(sql)
conn.close()
