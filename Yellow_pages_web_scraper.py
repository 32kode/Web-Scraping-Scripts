import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from time import sleep
import sys

headers = {
    '###'
}

# Yellow pages scraper
web_page_results = []
def yellow_pages_scraper(search_term, location):
    page = 1
    while True:
        url = f'https://www.yellowpages.com/search?search_terms={search_term}&geo_location_terms={location}&page={page}'
        r = requests.get(url, headers = headers)
        soup = bs(r.content, 'html.parser')
        # The number of listings on the page, used for the progress bar
        nr_items = soup.find('div', {'class':'pagination'}).span.text.split(' ')[-1]
        nr_items = int(nr_items)
        business = soup.find_all('div', {'class':'srp-listing'})
        for attribute in business:
            business_dict = {}
            try:
                business_dict['name'] = attribute.find('a', {'class':'business-name'}).text
            except:
                business_dict['name'] = ''
            try:
                business_dict['street_address'] = attribute.find('div', {'class':'street-address'}).text
            except:
                business_dict['street_address'] = ''
            try:
                business_dict['locality'] = attribute.find('div', {'class':'locality'}).text
            except:
                business_dict['locality'] = ''
            try:
                business_dict['phone'] = attribute.find('div', {'class':'phones phone primary'}).text
            except:
                business_dict['phone'] = ''
            try:
                business_dict['website'] = attribute.find('a', {'class':'track-visit-website'})['href']
            except:
                business_dict['website'] = ''
            web_page_results.append(business_dict)
            # Progress bar
            progress = len(web_page_results) / nr_items * 100
            sys.stdout.write("\r[%-20s] %d%%" % ('='*int(progress/5), progress))
            sys.stdout.flush()
        if not soup.find('a', {'class':'next ajax-page'}):
            break
        page += 1
    return web_page_results


# Export these results to Excel:
"""
import pandas as pd
df = pd.DataFrame.from_dict(web_page_results)
df.to_excel('output.xlsx', index=False)
"""
