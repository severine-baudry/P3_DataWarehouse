import configparser
import psycopg2
import sql_queries
import importlib
importlib.reload(sql_queries)
from sql_queries import create_table_queries, drop_table_queries, l_drop_star_tables, l_create_star_tables, insert_table_queries

def split_line(line):
    '''
    split multiline string along lines; remove empty lines
    '''
    return [ a for a in line.split("\n") if len(a.strip()) != 0]

def execute_queries(cur, conn, l_queries):
    '''
    execute a list of queries given as strings
    '''
    for query in l_queries:
        print("QUERY : ",  split_line(query)[0] )
        cur.execute(query)
        conn.commit()

def main():
    '''
    drop, create and fill only star-schema tables (to avoid time-consumming copies from S3)
    '''
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
        
    execute_queries(cur, conn, l_drop_star_tables)
    execute_queries(cur, conn, l_create_star_tables)
    execute_queries(cur, conn, insert_table_queries)

    conn.close()


if __name__ == "__main__":
    main()