import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries

def split_line(line):
    '''
    split multiline string along lines; remove empty lines
    '''
    return [ a for a in line.split("\n") if len(a.strip()) != 0]

def load_staging_tables(cur, conn):
    '''
    copy all staging tables from S3 buckets
    '''
    for query in copy_table_queries:
        print("LOAD TABLE", split_line(query)[0] )
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    '''
    insert data from staging tables to the fact and dimension tables
    '''
    for query in insert_table_queries:
        print("INSERT TABLE", split_line(query)[0])
        cur.execute(query)
        conn.commit()


def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()