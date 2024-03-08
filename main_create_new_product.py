import json

import pandas as pd
import shopify

from src.new_product_creator import ShopifyProduct

# Input and output
input_file_name = 'data/test_product_generator_v3.csv'
out_file_name = input_file_name.replace('.csv', '_report.csv')

# Read secrets
with open('config/secret.json', 'r') as jfile:
    secrets = json.load(jfile)
shop_name = secrets['shop_name']
token = secrets['token']
api_key = secrets['api_key']
api_password = secrets['api_password']
shopify_store_domain = secrets['shopify_store_domain']
api_version = secrets['api_version']

# Shopify settings
product_endpoint = f'https://{shopify_store_domain}/admin/api/{api_version}/products.json'
shop_url = "https://%s:%s@%s.myshopify.com/admin" % (api_key, token, shop_name)
shopify.ShopifyResource.set_site(shop_url)
shopify.Session.setup(api_key=api_key, secret=token)
shop = shopify.Shop.current

# Read input data
df_new_products = pd.read_csv(input_file_name, sep=';').head(1)
print(df_new_products)

df_new_products['Created'] = False
inventory = shopify.InventoryItem()

# Create products
for i, row in df_new_products.iterrows():
    try:
        title, sku, product_type, vendor, body_html, size, quantity, price, tags, link_img, _ = row.values
        new_product = ShopifyProduct.create(
            title, sku, product_type, vendor, body_html, size, quantity, price, tags, link_img)
        success = new_product.save()  # returns false if the record is invalid
        df_new_products.at[i, 'Created'] = success
    except Exception as e:
        raise e

# Generate output report
df_new_products.to_csv(out_file_name, index=False)

print('success')
