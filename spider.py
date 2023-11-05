# from scrapy.spiders import CrawlSpider , Rule
# from scrapy.linkextractors import LinkExtractor
# import requests
# from bs4 import BeautifulSoup
# import pandas as pd
# import numpy as np

# # dct = {'Product Title': [], 'Product Price': []}
# class crawling(CrawlSpider):
#     name = 'mycrawler'
#     allow = ['tooneyteez.com']
#     start_urls = ['https://www.tooneyteez.com/']

#     # rules = (
#     #     Rule(LinkExtractor(allow='collections/featured-collection-tees' )),
#     #     Rule(LinkExtractor(allow = 'products'),callback = 'parse_item'),
#     #     # Rule(LinkExtractor(allow= ''))

#     #     )
#     rules = (
#         Rule(LinkExtractor(allow='collections/men' )),
#         Rule(LinkExtractor (allow = 'products'),callback = 'parse_men_item'),
#         # Rule(LinkExtractor(allow= ''))

#         )
 
#     def __init__(self, *args, **kwargs):
#         super(crawling , self).__init__(*args, **kwargs)
#         self.data_list = []

#     def parse_item(self, response):
#         data = {} 
        
#         soup = BeautifulSoup(response.text, 'html.parser')
            
            
#         data['Title']= soup.find('h1', class_ = "productView-title").get_text(strip=True)
             
#         data['Price']= soup.find('span', class_ = 'price-item price-item--sale').get_text(strip=True)
#         data['Description'] = soup.find('div', class_ = 'panel').get_text(strip = True)
#         data['Availability'] = soup.find('span', class_ = 'hotStock-text').get_text(strip = True)
#         # try:
#         #     data['Number of reviews'] = soup.find('span', class_ = 'jdgm-prev-badge__text')

#         # except AttributeError:
#         #     print('could not be found')
#         # try:
#         #     data['Ratings'] = soup.find('span', class_ = 'jdgm-rev-widg__summary-average').get_text(strip = True )
#         # except AttributeError:
#         #     print('could not be found')
#         data['Image link'] = soup.find('div', attrs= {'class': 'media'}).get('href')
#         self.data_list.append(data)

#         yield data
#     def parse_men_item(self , response):
        

#         soup = BeautifulSoup(response.text, 'html.parser')

#         links_list = []

#         prd = soup.find_all('a' )

#         for link in prd:
#             href = prd.get('href')
#             links_list.append(href)
            

#         for link in links_list:
#             data= {}
#             product_links = 'https://www.tooneyteez.com/'+ link
#             newpage = requests.get(product_links)
#             print('scraping is happening ')
            
#             new_soup = BeautifulSoup(newpage, 'html.parser')
#             data['Title']= new_soup.find('h1', class_ = "productView-title").get_text(strip=True)
#             data['Price']= new_soup.find('span', class_ = 'price-item price-item--sale').get_text(strip=True)
#             data['Description'] = new_soup.find('div', class_ = 'panel').get_text(strip = True)
#             data['Availability'] = new_soup.find('span', class_ = 'hotStock-text').get_text(strip = True)
#             data['Image link'] = soup.find('div', attrs= {'class': 'media'}).get('href')

#             self.data_list.append(data)

#             yield data
      
        

#     def closed(self, reason):
#         # Convert the scraped data list to a DataFrame
#         df = pd.DataFrame(self.data_list)

#         # Save the DataFrame to a CSV file
#         df.to_csv('scraped_data.csv', index=False)

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import requests
from bs4 import BeautifulSoup
import pandas as pd
import scrapy

class MyCrawler(CrawlSpider):
    name = 'mycrawler'
    allowed_domains = ['tooneyteez.com']
    start_urls = ['https://www.tooneyteez.com/']

    rules = (
        Rule(LinkExtractor(allow=r'collections/featured-collection-tees'), callback='parse_product_page'),
        Rule(LinkExtractor(allow=r'collections/men'), callback='parse_men_item'),
        Rule(LinkExtractor(allow=r'collections/womens'), callback='parse_women_item'),
        # Rule(LinkExtractor(allow=r''), callback = 'parse_product_page')
    )

    def __init__(self, *args, **kwargs):
        super(MyCrawler, self).__init__(*args, **kwargs)
        self.data_list = []

    def parse_men_item(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        prd = soup.find_all('a')

        for link in prd:
            href = link.get('href')
            if href:
                product_links = 'https://www.tooneyteez.com/' + href
                yield scrapy.Request(product_links, callback=self.parse_product_page)

    def parse_women_item(self , response):
        soup = BeautifulSoup(response.text , 'html.parser')
        prds = soup.find_all('a')

        for lin in prds:
            hrefs = lin.get('href')
            if hrefs:
                product_link = 'https://www.tooneyteez.com/' + hrefs
                yield scrapy.Request(product_link,callback = self.parse_product_page )


    def parse_product_page(self, response):
        data = {}
        soup = BeautifulSoup(response.text, 'html.parser')

       
        data['Title']= soup.find('h1', class_ = "productView-title").get_text(strip=True)
        data['Price']= soup.find('span', class_ = 'price-item price-item--sale').get_text(strip=True)
        panel_div = soup.find('div', class_='panel')
    
        if panel_div:
            data['Description'] = panel_div.get_text(strip=True)
        else:
            data['Description'] = 'Description not found'  # or set to a default value
        data['Availability'] = soup.find('span', class_ = 'hotStock-text').get_text(strip = True)
        data['Image link'] = soup.find('div', attrs= {'class': 'media'}).get('href')
        self.data_list.append(data)
        yield data

    def closed(self, reason):
        df = pd.DataFrame(self.data_list)
        df.to_csv('scraped_data.csv', index=False)
