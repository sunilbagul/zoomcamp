#!/usr/bin/env python
# coding: utf-8
from sqlalchemy import create_engine
import pandas as pd
import argparse 
import os

def main(params):
    user = params.user
    password = params.user
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    # the backup files are gzipped, and it's important to keep the correct extension
    # for pandas to be able to open the file
    if url.endswith('.csv.gz'):
        csv_name = 'output.csv.gz'
    else:
        csv_name = 'output.csv'
    
    os.system(f"wget {url} -O {csv_name}")

    #df = pd.read_csv(csv_name, nrows=100)
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)
    df = next(df_iter)
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

    df.to_sql(name=table_name, con=engine, if_exists='append')


    while True:
        df = next(df_iter)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.to_sql('yellow_taxi_data',con=engine,if_exists='append')
        print('inserted another chunk..')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest csv data to ostgres')
    parser.add_argument("--user",
                        help="user name for postgres")
    parser.add_argument("--password",
                        help="password name for postgres")
    parser.add_argument("--host",
                        help="host for postgres")
    parser.add_argument("--port",
                        help="port for postgres")
    parser.add_argument("--db",
                        help="db for postgres")
    parser.add_argument("--table_name",
                        help="table name for postgres")
    parser.add_argument("--url",
                        help="url of csv file")

    args = parser.parse_args()
    main(args)