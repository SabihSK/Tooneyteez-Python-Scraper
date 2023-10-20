from scrapy.spiders import CrawlSpider , Rule
from scrapy.linkextractors import LinkExtractor
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
dct = {'Product Title': [], 'Product Price': []}
class crawling(CrawlSpider):
    name = 'mycrawler'
    allow = ['tooneyteez.com']
    start_urls = ['https://www.tooneyteez.com/']

    rules = (
        Rule(LinkExtractor(allow='collections/featured-collection-tees')),
        Rule(LinkExtractor(allow = 'products'),callback = 'parse_item')

        )
    def parse_item(self, response):
        # try:
        soup = BeautifulSoup(response.text, 'html.parser')
            # dct = { 'Product title': [], 'Product Price': []}
            
        product_title = soup.find('h1', class_ = "productView-title").get_text(strip=True)
                # dct['Product title'].append(title)
        # for product in product_price:
        product_price = soup.find('span', class_ = 'price-item price-item--sale').get_text(strip=True)
                # dct['Product Price'].append(product)
        yield{
            'Product Title' : product_title,
            'product Price': product_price
        }
        # if product_title and product_price:
        #     dct['Product Title'].append(product_title),
        #     dct['Product Price'].append(product_price)
        # print(dct)

    
        # except :
        #     print('info could not be found')



