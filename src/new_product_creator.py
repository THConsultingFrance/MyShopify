import shopify
import re


def split_string_by_delimiters(input_string):
    # Split by ',' first
    split_by_comma = input_string.split(',')
    # Split each element by ', ' if it exists and flatten the result using list comprehension
    split_by_comma_and_space = [item.strip() for elem in split_by_comma for item in elem.split(', ')]
    # Return the result
    return split_by_comma_and_space


def get_id_image(url):
    pattern = r'file/d/([a-zA-Z0-9_-]+)/'
    match = re.search(pattern, url)
    file_id = ""
    if match:
        file_id = match.group(1)
        print("File ID:", file_id)
    return file_id


class ShopifyProduct:
    @staticmethod
    def create(title, sku, product_type, vendor, body_html, size, quantity, price, tags, link_img):
        # Create a new product
        new_product = shopify.Product()

        # Define product details
        new_product.title = f'{title}'
        new_product.product_type = f'{product_type}'
        new_product.vendor = f'{vendor}'
        new_product.body_html = f'{body_html}'
        new_product.tags = f'{tags}'

        # Add variants to set price
        str_price = f'{float(price):.2f}'
        # Create variants for different sizes
        size_variants = split_string_by_delimiters(size)
        # quantity_variants = split_string_by_delimiters(quantity)

        variants = [shopify.Variant({'price': str_price,
                                     'option1': s,
                                     'sku': f'{sku}',
                                     'inventory_management': 'shopify',  # Set inventory management to 'shopify'
                                     'inventory_policy': 'deny',
                                     }) for s in size_variants]

        # Add the variants to the product
        new_product.variants = variants

        # Add images to the product
        links = split_string_by_delimiters(link_img)
        images = []
        for link_i in links:
            image_i = shopify.Image()
            image_i.src = f"https://docs.google.com/uc?export=download&confirm=no_antivirus&id={get_id_image(link_i)}"
            images.append(image_i)
        print('images', len(images), images)
        new_product.images = images

        return new_product
