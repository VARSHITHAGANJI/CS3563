import psycopg2
import pandas as pd
import numpy as np
from psycopg2.extensions import register_adapter, AsIs
psycopg2.extensions.register_adapter(np.int64, psycopg2._psycopg.AsIs)

username = input('Enter user name:')
passwd = input('Enter postgres password:')

conn = psycopg2.connect(
   database="postgres", user=username, password=passwd, host='localhost', port= '5432')
import psycopg2.extras
print('succesfully connected to database')
cur = conn.cursor()



schema_sql = '''CREATE SCHEMA mydb;

CREATE TABLE mydb.author (
	author_name VARCHAR PRIMARY KEY
);

CREATE TABLE mydb.conference (
	name VARCHAR PRIMARY KEY
);

CREATE TABLE mydb.research_paper (
	paper_id INTEGER PRIMARY KEY,
	paper_title VARCHAR NOT NULL,
	year_of_publication INTEGER NOT NULL,
	abstract text NOT NULL,
	name VARCHAR NOT NULL,
	
	FOREIGN KEY (name)
      REFERENCES mydb.Conference (name)
);

CREATE TABLE mydb.citation (
	paper_id_1 INTEGER NOT NULL,
	citationpaper_id_2 INTEGER NOT NULL,
	
	FOREIGN KEY (paper_id_1 )
      REFERENCES mydb.Research_Paper (paper_id ),
	
	FOREIGN KEY (citationpaper_id_2)
      REFERENCES mydb.Research_Paper (paper_id)
);

CREATE TABLE mydb.authored_By (
	paper_id INTEGER NOT NULL,
	author_name VARCHAR NOT NULL,
	author_number INTEGER NOT NULL,
	
	FOREIGN KEY (paper_id)
      REFERENCES mydb.Research_Paper (paper_id),
	
	FOREIGN KEY (author_name)
      REFERENCES mydb.Author (author_name)
);'''

s = '''DROP SCHEMA mydb CASCADE'''

cur.execute(s)

cur.execute(schema_sql)
cur.close()
conn.commit()
print('Created schema and tables')
df_authors = pd.read_csv('authors.csv',encoding = 'utf-8')
df_cites = pd.read_csv('citation.csv')
df_conf = pd.read_csv('venues.csv')
df_research = pd.read_csv('research.csv')
df_authored_by = pd.read_csv('authored_by.csv')


#Function to populate dataframe to table
def populate(table,df):
    if len(df) > 0:
      df_columns = list(df)
    
      columns = ",".join(df_columns)

    
      values = "VALUES({})".format(",".join(["%s" for _ in df_columns])) 

    
      insert_stmt = "INSERT INTO {} {}".format(table,values)

      cur = conn.cursor()
      psycopg2.extras.execute_batch(cur, insert_stmt, df.values)
      conn.commit()
      cur.close()




import time
begin = time.time()
populate('mydb.author',df_authors)
populate('mydb.conference',df_conf)
populate('mydb.research_paper',df_research)
populate('mydb.citation',df_cites)
populate('mydb.authored_By',df_authored_by)
time.sleep(1)

end = time.time()
print('Database is succesfully populated in ',(end-begin),'s')

