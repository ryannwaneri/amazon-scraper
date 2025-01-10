from pathlib import Path
from collections import namedtuple
from bs4 import BeautifulSoup
import pandas as pd
from amazon_scraper import download_amazon_pages

AmazonProduct = namedtuple('AmazonProduct', ['name','price','url'])

if __name__ == '__main__':
    query = 'soundcore'
    source_dir = Path('./exports')
    download_amazon_pages(query=query,page_from=1,page_to=3, export_location=source_dir)

    records = []
    ignore_sponsored = False

    for html_file in source_dir.glob(f'{query}*.html'):
        with open(html_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
        print(f'Processing file {html_file}')
        result_list = soup.find('div','s-main-slot s-result-list s-search-results sg-row')
        products = result_list.find_all('div',{
            'role':True
        })