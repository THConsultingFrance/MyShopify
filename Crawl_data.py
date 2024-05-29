'''A pyfile to def a pipeline to crawl data from SHopify into local file csv  '''

import json
import pandas as pd
import shopify
import datetime
import requests
import pytz
import os
import binascii
import time


# Read secrets
with open(r'D:\\Study\\THConsultant\\secret.json', 'r') as jfile:
    secrets = json.load(jfile)
shop_name = secrets['shop_name']
token = secrets['token']
api_key = secrets['api_key']
api_password = secrets['api_password']
shopify_store_domain = secrets['shopify_store_domain']
api_version = secrets['api_version']   

# Shopify settings
orders_endpoint = f'https://{shopify_store_domain}/admin/api/{api_version}/orders.json?status=any'
shop_url = "https://%s:%s@%s.myshopify.com/admin" % (api_key, token, shop_name)
shopify.ShopifyResource.set_site(shop_url)
shopify.Session.setup(api_key=api_key, secret=token)
# shop = shopify.Shop.current     
# Shopify settings
orders_endpoint = f'https://{shopify_store_domain}/admin/api/{api_version}/orders.json?status=any'
shop_url = "https://%s:%s@%s.myshopify.com/admin" % (api_key, token, shop_name)
shopify.ShopifyResource.set_site(shop_url)
shopify.Session.setup(api_key=api_key, secret=token)

# Function to fetch all orders with pagination using since_id
def fetch_all_orders():
    orders = []
    last_id = None

    while True:
        if last_id:
            new_orders = shopify.Order.find(status='any', limit=250, since_id=last_id)
        else:
            new_orders = shopify.Order.find(status='any', limit=250)

        if not new_orders:
            break

        orders.extend(new_orders)
        last_id = new_orders[-1].id
        time.sleep(0.5)  

    return orders

# Fetch all orders
orders = fetch_all_orders()


# Crawling data
info_dict = {}
for inv in orders:
    if inv.customer:
    # Name
        ord_time = datetime.datetime.strptime(inv.created_at, '%Y-%m-%dT%H:%M:%S%z')
        client_name = f'{inv.customer.last_name} {inv.customer.first_name}'
        name = f"S{ord_time.strftime('%d%m%y')}_{inv.order_number}_{client_name}"
    if name not in info_dict:
        info_dict[name] = {}
        info_dict[name]['Order Number'] = inv.order_number
        # Order - Product, Price, Name, Quantity, Order_Date, 
        info_dict[name]['Order Date'] = ord_time.strftime('%m/%d/%Y')
        info_dict[name]['Product'] = []

        for prod in inv.line_items:
            info_dict[name]['Product'].append([prod.name, prod.quantity])

        # Client: Name, Email, Phone, Address
        info_dict[name]['Client name'] = client_name
        if hasattr(inv.customer, 'phone') and inv.customer:
            info_dict[name]['Phone Number'] = inv.customer.phone
        elif hasattr(inv.customer, 'default_address') and inv.customer.default_address:
            info_dict[name]['Phone Number'] = inv.customer.default_address.phone

        info_dict[name]['Email'] = inv.customer.email

        if hasattr(inv.customer, 'default_address') and inv.customer.default_address:
            temp = inv.customer.default_address
            info_dict[name]['Add'] = f'{temp.address1}, {temp.address2}, {temp.city}, {temp.province}'
        # Process - Due_date, Person
    else: 
        continue

data = pd.DataFrame(info_dict)
data.to_csv('Data.csv')

print(data.iloc[:,:4])
print(data.shape)