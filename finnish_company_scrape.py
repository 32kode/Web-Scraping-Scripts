# a scraper for more in-depth info on a company level.

import time
from random import randint
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs

company_ytunnus_ls = []
company_kotipaikka_ls = []
company_paatoimiala_ls = []
company_perustusvuosi_ls = []
company_yhtiomuoto_ls = []
company_kayntiosoite_ls = []
company_postiosoite_ls = []
company_toimari_ls = []
company_puhelin_ls = []
company_sahkoposti_ls = []
company_kotisivut_ls = []
company_liikevaihto_ls = []


i = 0

with open('base_file.txt') as file:
    for raw_comp_num in file:
        time.sleep(randint(0, 1))
        i += 1
        ytunnus = raw_comp_num.strip().zfill(8)
        url = f'https://www.asiakastieto.fi/yritykset/fi/{ytunnus}/rekisteritiedot'
        page = requests.get(url)
        soup = bs(page.content, 'html.parser')
        company_ytunnus_ls.append(ytunnus)
        print(f'{i} companies basic data scraped')
        try:
            toimari = soup.find('div', class_='col-md-6').find('dt', text='Toimitusjohtaja').find_next_sibling(
                'dd').text
            company_toimari_ls.append(toimari)
        except AttributeError:
            company_toimari_ls.append('N/A')
        try:
            paatoimiala = soup.find('div', class_='col-md-6').find('dt', text='Päätoimiala').find_next_sibling(
                'dd').text
            company_paatoimiala_ls.append(paatoimiala)
        except AttributeError:
            company_paatoimiala_ls.append('N/A')
        try:
            yhtiomuoto = soup.find('div', class_='col-md-6').find('dt', text='Yhtiömuoto').find_next_sibling(
                'dd').text
            company_yhtiomuoto_ls.append(yhtiomuoto)
        except AttributeError:
            company_yhtiomuoto_ls.append('N/A')
        try:
            year = soup.find('div', class_='col-md-6').find('dt', text='Toiminta käynnistynyt').find_next_sibling(
                'dd').text[0:4]
            company_perustusvuosi_ls.append(year)
        except AttributeError:
            company_perustusvuosi_ls.append('N/A')
        try:
            kayntiosoite = soup.find('div', class_='col-sm-9 vcard').\
                find('dl', class_='dl-horizontal dl--no-mobile-stack mobile-bottom-margin').\
                find('dt', text='Käyntiosoite').find_next_sibling('dd').text
            company_kayntiosoite_ls.append(kayntiosoite)
        except AttributeError:
            company_kayntiosoite_ls.append('N/A')
        try:
            kotipaikka = soup.find('div', id='box--registry-information--contact-information'). \
                find('dt', text='Kotipaikka').find_next_sibling('dd').text
            company_kotipaikka_ls.append(kotipaikka)
        except AttributeError:
            company_kotipaikka_ls.append('N/A')
        try:
            postiosoite = soup.find('div', id='box--registry-information--contact-information'). \
                find('dt', text='Postiosoite').find_next_sibling('dd').text
            company_postiosoite_ls.append(postiosoite)
        except AttributeError:
            company_postiosoite_ls.append('N/A')
        try:
            puhelin = soup.find('div', id='box--registry-information--contact-information').\
                find('dt', text='Puhelin').find_next_sibling('dd').text
            company_puhelin_ls.append(puhelin)
        except AttributeError:
            company_puhelin_ls.append('N/A')
        try:
            kotisivut = soup.find('div', id='box--registry-information--contact-information').\
                find('dt', text='Kotisivu').find_next_sibling('dd').text
            company_kotisivut_ls.append(kotisivut)
        except AttributeError:
            company_kotisivut_ls.append('N/A')
        try:
            sahkoposti = soup.find('div', id='box--registry-information--contact-information').\
                find('dt', text='Sähköposti').find_next_sibling('dd').text
            company_sahkoposti_ls.append(sahkoposti)
        except AttributeError:
            company_sahkoposti_ls.append('N/A')
        try:  # get company latest revenue
            url = f'https://www.asiakastieto.fi/yritykset/fi/{ytunnus}/taloustiedot'
            page = requests.get(url)
            soup = bs(page.content, 'html.parser')
            raw_revenue = soup.find('div', class_='wrapper chart__headings') \
                .find('span',
                      class_='chart__highlight pull-right').text
            sep = '€'
            revenue = raw_revenue.split(sep, 1)[0].strip()
            company_liikevaihto_ls.append(revenue)
        except AttributeError:
            company_liikevaihto_ls.append('N/A')

header_list = ['Y-tunnus', 'Perustusvuosi', 'Toimitusjohtaja', 'Sähköposti', 'Puhelin', 'Verkkosivut', 'Kotipaikka',
               'Käyntiosoite', 'Postiosoite', 'Päätoimiala', 'Yhtiömuoto', 'Liikevaihto 2022']

df = pd.DataFrame(list(zip(company_ytunnus_ls, company_perustusvuosi_ls, company_toimari_ls, company_sahkoposti_ls,
                           company_puhelin_ls, company_kotisivut_ls, company_kotipaikka_ls, company_kayntiosoite_ls,
                           company_postiosoite_ls, company_paatoimiala_ls,
                           company_yhtiomuoto_ls, company_liikevaihto_ls)))

df.to_excel('file.xlsx', header=header_list)

