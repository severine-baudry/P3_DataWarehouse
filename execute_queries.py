import configparser
import psycopg2
import sql_queries
import importlib
importlib.reload(sql_queries)
from sql_queries import create_table_queries, drop_table_queries, l_drop_star_tables, l_create_star_tables, insert_table_queries

def split_line(line):
    return [ a for a in line.split("\n") if len(a.strip()) != 0]

def execute_tables(cur, conn, l_queries):
    for query in l_queries:
        print("QUERY : ",  split_line(query)[0] )
        cur.execute(query)
        conn.commit()

def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
        
    execute_tables(cur, conn, l_drop_star_tables)
    execute_tables(cur, conn, l_create_star_tables)
    execute_tables(cur, conn, insert_table_queries)

    conn.close()


if __name__ == "__main__":
    main()