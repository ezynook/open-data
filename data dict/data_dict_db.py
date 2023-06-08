import pandas as pd
import psycopg2 as pg
import numpy as np
import os
from urllib.parse import quote
from sqlalchemy import create_engine
import json
import requests

USERNAME = "ckan"
PASSWORD = "ckan"
DB = "datastore"
IPADDR = "192.168.10.47"
engine = create_engine(f"postgresql://{USERNAME}:%s@{IPADDR}/{DB}" % quote(f'{PASSWORD}'))

def getID(dataset):
    r = requests.get(f"http://192.168.10.47:8080/api/3/action/package_show?id={dataset}", 
                 headers={'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2 \
                            ODYyMDI0MTgsImp0aSI6IlVLaGFsSWU1eG1xUjZNR2o3bGQ4amVkTnEzeHB1X2QyZ05hS1VUV \
                            ENVNkJRVTZaM3VsX295MkVicE1FRzBkSnNKNHluZTFFM0lVRUlaTlVPIn0.-2GI8s-h4MZrZ\
                            2MeOtkZvqyWyEw54d5m_p7vLboEekY'})
    data = r.json()
    result = data['result']['resources'][0]['id']
    return result

note = pd.read_sql(f"""
            SELECT
                cols.data_type,cols."column_name" cols,
                (SELECT
                    pg_catalog.col_description (C.OID, cols.ordinal_position::INT) 
                FROM
                    pg_catalog.pg_class C 
                WHERE
                    C.OID = (SELECT ('"' || cols.TABLE_NAME || '"')::REGCLASS::OID) 
                    AND C.relname = cols.TABLE_NAME) AS "comment" 
            FROM
                information_schema.COLUMNS cols 
            WHERE
                cols.table_catalog = '{DB}' 
                AND cols.TABLE_NAME = '{getID('test')}' 
                AND cols.table_schema = 'public';
    """, engine)

#Loop insert
for row in note.itertuples():
    TABLE_ID = getID("test")
    j = json.dumps({
        "notes": row.comment,
        "type_override": row.data_type,
        "label": row.cols.upper()
    })
    with engine.begin() as conn:
        conn.execute(f'comment on column public."{TABLE_ID}".{row.cols} IS '+"'"+j+"';")
        print("Update Comment:", row.cols)