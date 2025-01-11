from pathlib import Path
from collections import namedtuple
from bs4 import BeautifulSoup
import pandas as pd
from amazon_scraper import download_amazon_pages

AmazonProduct = namedtuple('AmazonProduct', ['name','price'])

def extract_prop(product_element):
    name = product_element.find('h2','a-size-medium a-spacing-none a-color-base a-text-normal').span.text
    price = product_element.find('span','a-price').find('span','a-offscreen').text if product_element.find('span','a-price').find('span','a-offscreen').text else None
    return AmazonProduct(name=name, price=price)

if __name__ == '__main__':
    query = 'soundcore'
    source_dir = Path('./export')
    download_amazon_pages(query=query,page_from=1,page_to=3, export_location=source_dir)

    records = []
    ignore_sponsored = False

    for html_file in source_dir.glob(f'{query}*.html'):
        with open(html_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
        print(f'Processing file {html_file}')
        result_list = soup.find('div','s-main-slot s-result-list s-search-results sg-row')
        products = result_list.find_all('div',attrs={
            'role':'listitem',
            'data-component-type':'s-search-result'
        })
        priced_products = []
        for product in products:
            if product.find('span','a-price') == None:
                continue
            #priced_products.append(product.find('span','a-price').find('span','a-offscreen').text)
            priced_products.append(product)
        for product in priced_products:
            records.append(extract_prop(product))    
    df=pd.DataFrame(records)
    df.to_csv(f'{query}_search.csv')
    print('file saved')