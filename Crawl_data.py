'''A pyfile to def a pipeline to crawl data from SHopify into local file csv  '''

import json
import pandas as pd
import shopify



# Read secrets
with open('D:\DSEB 63 - NEU\THConsultant\secret.json', 'r') as jfile:
    secrets = json.load(jfile)
shop_name = secrets['shop_name']
token = secrets['token']
api_key = secrets['api_key']
api_password = secrets['api_password']
shopify_store_domain = secrets['shopify_store_domain']
api_version = secrets['api_version']    