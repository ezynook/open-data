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
TABLE_ID = main_config["TABLE_ID"]

class SDC_API:
    def __init__(self) -> None:
        self.editDataExplorer()
        
    def Connect(self):
        engine = create_engine(f"postgresql://{USERNAME}:%s@{IPADDR}/{DB}" % quote(f'{PASSWORD}'))
        return engine
        
    def editDataExplorer(self):
        #Call API
        url = "http://demo-cinspire.myddns.me:9400/json/MEA/usage_distict"
        response = requests.get(url, auth=("admin", "Dci@2560"), verify=False)
        data = response.json()
        data1 = data['MEA.usage_distictResponse']['MEA.usage_distictOutput']['MEA.row']
        #Append to DataFrame
        df = pd.DataFrame(data1)
        df.insert(0, '_id', df.index)
        df.insert(1, '_full_text', np.nan)
        df.to_sql(f"{TABLE_ID}", self.Connect(), if_exists='replace', index=False)
        print(f"Insert Table: {TABLE_ID} Successfully")
        
if __name__ == '__main__':
    obj = SDC_API()
