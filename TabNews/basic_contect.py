# %%
import requests
import pandas as pd
import datetime
import json
import time


# %%

class Collector:
    def __init__(self, url):
        self.url = url
    


    def get_response(self,**kwargs):
        resp = requests.get(self.url, params=kwargs)
        return resp


    def save_data(self,data, option='json'):
        now = self.now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

        if option == 'json':
            with open(f'data/content/json/{now}.json','w' ) as open_file:
                json.dump(data, open_file,indent=4)
        
        elif option == 'dataframe':
            df = pd.DataFrame(data)
            df.to_parquet(f'data/content/parquet/{now}.parquet',index=False)


#def get_response(**kwargs):
#        url = 'https://www.tabnews.com.br/api/v1/contents'
#        resp = requests.get(url, params=kwargs)
#        return resp
#
#
#def save_data(data, option='json'):
#    now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
#
#    if option == 'json':
#        with open(f'data/content/json/{now}.json','w' ) as open_file:
#            json.dump(data, open_file,indent=4)
#        
#    elif option == 'dataframe':
#        df = pd.DataFrame(data)
#        df.to_parquet(f'data/content/parquet/{now}.parquet',index=False)

# %%

url = 'https://www.tabnews.com.br/api/v1/contents'
collecct = Collector(url)
page =1 
date_stop = pd.to_datetime('2024-03-01').date()
while True:
    print(page)
    
    resp = collecct.get_response(page=page,per_page=100,strategy='new')
    if resp.status_code == 200:
        data = resp.json()
        collecct.save_data(data)

        date = pd.to_datetime(data[-1]['updated_at']).date()
        if len(data) < 100 or date < date_stop:
            break
        
        page += 1
        time.sleep(2) 
    
    else:
        print(resp.status_code)
        print(resp.json())
        time.sleep(30)
 # %%
