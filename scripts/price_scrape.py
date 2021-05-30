#!/usr/bin/python3

import requests,sys
from bs4 import BeautifulSoup
from datetime import datetime

def get_price(ticker):
	'''
	Scrapes price of ticker from yahoo finance
	param ticker : string
	param type : string ('stocks' or 'crypto')
	'''
	url = f'https://finance.yahoo.com/quote/{ticker}'
	soup = BeautifulSoup(requests.get(url).text, 'html.parser')
	#first check if the market is open
	try:
		if 'open' in soup.find('div',{'class':'C($tertiaryColor) D(b) Fz(12px) Fw(n) Mstart(0)--mobpsm Mt(6px)--mobpsm'}).span.text:
			price = soup.find('span',{'class' : 'Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)'}).text
			return float(price.replace(',',''))
		else:
			raise MarketNotOpen
	except MarketNotOpen:
		# I need to catch and re-raise this exception as it is initially
		# raised within the try..except block
		raise MarketNotOpen
	except:
		raise TickerNonExistent

class MarketNotOpen(Exception):
	'''
	A custom exception to be raised when a market is closed
	'''
	pass

class TickerNonExistent(Exception):
	'''
	A custom exception to be raised when the ticker given does not exist
	or is not found.
	'''

if __name__ == '__main__':
	try:	
		date = datetime.utcnow()
		date = datetime(date.year,date.month,date.day,date.hour,date.minute,0)

		#checking if a ticker was given
		try:
			ticker = sys.argv[1].upper()
		except IndexError:
			sys.stderr.write(f'{str(date)} [CALL] : Ticker not given.\n')


		try:
			price = get_price(ticker)
			#stdout will be added to a csv file
			sys.stdout.write(f'{str(date)},{price}\n')
			sys.exit(0)
		#checking if market is open
		except MarketNotOpen:
			sys.stderr.write(f'{str(date)} [{ticker}] : Market is not open.\n')
			sys.exit(1)
		#checking if ticker given exists
		except TickerNonExistent:
			sys.stderr.write(f'{str(date)} [CALL] : Ticker: {ticker} does not exist.\n')
			sys.exit(2)
	except MemoryError as err:
		sys.stderr.write(f'{str(date)} [CALL] : Memory Error in {ticker}.\n')
