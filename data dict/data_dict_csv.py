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

df = pd.read_csv("dict.txt")

def getID(dataset):
    r = requests.get(f"http://192.168.10.47:8080/api/3/action/package_show?id={dataset}", 
                 headers={'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2 \
                            ODYyMDI0MTgsImp0aSI6IlVLaGFsSWU1eG1xUjZNR2o3bGQ4amVkTnEzeHB1X2QyZ05hS1VUV \
                            ENVNkJRVTZaM3VsX295MkVicE1FRzBkSnNKNHluZTFFM0lVRUlaTlVPIn0.-2GI8s-h4MZrZ\
                            2MeOtkZvqyWyEw54d5m_p7vLboEekY'})
    data = r.json()
    result = data['result']['resources'][0]['id']
    return result

for v in df.itertuples():
    TABLE_ID = getID("test")
    j = json.dumps({
        "notes": v.description,
        "type_override": v.datatype,
        "label": v.label
    })
    with engine.begin() as conn:
        conn.execute(f'comment on column public."{TABLE_ID}".{v.cols} IS '+"'"+j+"';")
        print("Update Comment:", v.cols)
        