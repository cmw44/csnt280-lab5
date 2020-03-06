# initialize_db.py
import psycopg2
conn_string = "host='localhost' dbname='test_db' "
conn_string += " user='bob' password='somepass'"
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()
infile = open("init.sql","r")
sql = infile.read()
infile.close()
cursor.execute(sql)
sql = open("add_initial_data.sql").read()
cursor.execute(sql)
conn.commit()
conn.close()
