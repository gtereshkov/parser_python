## -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib.request
import pandas as pd

# Парсим выгрузку из БД онлайнера в ДатаФрейм_1
dataframe_onliner = pd.read_excel('test_positions_onliner.xlsx', header=None, sheet_name='Лист1', usecols=[1, 2, 5])
dataframe_onliner.columns = ['manufacturer', 'machine_name', 'your_onliner_price']
print(dataframe_onliner)
#dict_onliner = dataframe_onliner.to_dict('index')

# Парсим файлик со ссылками на странички на онлайнере в ДатаФрейм_2
dataframe_lapka = pd.read_excel('positions_with_links.xlsx', header=None, sheet_name='Лист1', usecols=[1, 4])
dataframe_lapka.columns = ['machine_name', 'onliner_link']
print(dataframe_lapka)
#dict_lapka = dataframe_lapka.to_dict('index')

df1 = pd.merge(dataframe_onliner, dataframe_lapka, on='machine_name', how='outer')
df1['their_onliner_price'] = ''
df1 = df1[['manufacturer', 'machine_name', 'onliner_link', 'your_onliner_price', 'their_onliner_price']]
print(df1)

def get_price(link):
	html_doc = urllib.request.urlopen(link)
	soup = BeautifulSoup(html_doc, 'html.parser')
	soup.encoding = 'utf-8'

	if soup.find("a", class_="offers-description__link offers-description__link_subsidiary offers-description__link_nodecor") :
		parse_result = soup.find("a", class_="offers-description__link offers-description__link_subsidiary offers-description__link_nodecor").find("span", class_="helpers_hide_tablet")
		price = parse_result.text.strip()
	else :
		price = 'Net v nalichii'
	return price


for index, row in df1.iterrows():
	df1.at[index, 'their_onliner_price'] = get_price(df1.at[index, 'onliner_link'])
	print(df1.at[index, 'onliner_link'])
	
print(df1)

df1.to_csv('out1.csv')