import pandas as pd
import psycopg2 as pg
import numpy as np
import os
from sqlalchemy import create_engine
from urllib.parse import quote
import json
import requests
from configparser import ConfigParser

config_object = ConfigParser()
config_object.read("config.ini")
main_config = config_object["MAIN"]

USERNAME = main_config["USERNAME"]
PASSWORD = main_config["PASSWORD"]
IPADDR = main_config["IPADDR"]
DB = main_config["DB"]

class SDC_Dataset:
    def __init__(self) -> None:
        self.getData()
        
    def Connect(self):
        engine = create_engine(f"postgresql://{USERNAME}:%s@{IPADDR}/{DB}" % quote(f'{PASSWORD}'))
        return engine
    
    #ต้องไป Generate API ที่ WebUI
    def getID(dataset):
        r = requests.get(f"http://192.168.10.47/api/3/action/package_show?id={dataset}", 
                     headers={'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2ODYyMDI0MTgsImp0aSI6IlVLaGFsSWU1eG1xUjZNR2o3bGQ4amVkTnEzeHB1X2QyZ05hS1VUVENVNkJRVTZaM3VsX295MkVicE1FRzBkSnNKNHluZTFFM0lVRUlaTlVPIn0.-2GI8s-h4MZrZ2MeOtkZvqyWyEw54d5m_p7vLboEekY'})
        data = r.json()
        result = data['result']['resources'][0]['id']
        return result
    
    def getData(self):
        TABLE_ID = getID("test")
        url = "http://demo-cinspire.myddns.me:9400/json/MEA/usage_distict"
        response = requests.get(url, auth=("admin", "Dci@2560"), verify=False)
        data = response.json()
        data1 = data['MEA.usage_distictResponse']['MEA.usage_distictOutput']['MEA.row']
        #Append to DataFrame
        df = pd.DataFrame(data1)
        os.system(f"rm -f /var/lib/docker/volumes/ckan_storage/_data/resource/{TABLE_ID[:3]}/{TABLE_ID[3:6]}/*")
        df.to_csv(f"/var/lib/docker/volumes/ckan_storage/_data/resource/{TABLE_ID[:3]}/{TABLE_ID[3:6]}/{TABLE_ID[6:]}", index=False)
        print(f"Replace file: {TABLE_ID[6:]} Successfully")
        self.editDataExplorer(df)
        
    def editDataExplorer(self, df):
        TABLE_ID = getID("test")
        df.insert(0, '_id', df.index)
        df.insert(1, '_full_text', np.nan)
        df.to_sql(f"{TABLE_ID}", self.Connect(), if_exists='replace', index=False)
        print(f"Insert Table: {TABLE_ID} Successfully")
        
if __name__ == '__main__':
    obj = SDC_Dataset()
