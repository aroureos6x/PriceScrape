#!/usr/bin/python3

import csv,os,sys
from datetime import datetime,timedelta

abspath = os.path.dirname(os.path.abspath(__file__))

def check_mtimes():
	'''
	Checks the modification times of all csv files and returns those
	that have been modified in the past hour
	'''
	files = []
	paths = [
	os.path.join(abspath,'..','data','crypto_csvs','minute'),
	os.path.join(abspath,'..','data','stocks_csvs','minute')
	]
	now = datetime.utcnow()
	for path,type in zip(paths,['crypto','stocks']):
		for file in os.listdir(path):
			mtime = os.stat(os.path.join(path,file)).st_mtime
			mdate = datetime.utcfromtimestamp(mtime)
			#checks if file has been modified in the past hour
			if mdate > now - timedelta(hours=1) and mdate < now:
				files.append(os.path.join(path,file))
	return files

def get_data(file):
	'''
	Reads the data of the file and returns the data that is corresponding
	to the past hour, classified to open,high,low,close prices + the 
	date and hour that the data is referring to.
	param file: string - name of file to read data from
	'''
	prices = []
	now = datetime.utcnow()
	#collecting prices from file
	with open(file,'r',encoding='utf-8') as file:
		reader = csv.reader(file)
		for row in reader:
			#skip empty rows
			if not row:
				continue
			#check date
			date = datetime.strptime(row[0],'%Y-%m-%d %H:%M:%S')
			#if date is right -> save price
			temp2 = datetime(now.year,now.month,now.day,now.hour,0,0)
			temp1 = temp2 - timedelta(hours=1)
			if date > temp1 and date <= temp2:
				prices.append(row[1])
			else:
				continue
	if not prices:
		raise NoPricesCollected(file.name)
	#classifying prices
	prices = {
		'date' : datetime(now.year,now.month,now.day,now.hour,0,0),
		'open' : prices[0],
		'high' : max(prices),
		'low' : min(prices),
		'close' : prices[-1]
	}

	return prices

def add_data(file,prices):
	'''
	Appends the new hourly data to the corresponding csv file with hourly data
	param file: string - path to minute data file
	param prices: dictionary containing {'date':x,open':x,'high':x,'low':x,'close':x} prices
				  to be added to the hourly data file
	'''
	#extracting the name of the ticker from the path given with the file value
	filename = file[file.rfind('m')+1:]
	filepath = os.path.join(file[:file.find('csvs')+4],'hour',f'h{filename}')
	#creating the file and adding the column names if it doesn't exist
	if not os.path.exists(filepath):
		with open(filepath, 'w', encoding='utf-8') as file:
			file.write('date,open,high,low,close\n')
	#appending the data into the file
	with open(filepath, 'a', encoding='utf-8') as file:
		writer = csv.writer(file,lineterminator='\n')
		writer.writerow([str(i) for i in prices.values()])

class NoPricesCollected(Exception):
	pass

if __name__ == '__main__':
	date = datetime.today()
	date = datetime(date.year,date.month,date.day,date.hour,date.minute,0)
	#find files that have been modified
	files = check_mtimes()
	if not files:
		sys.stderr.write(f'{date} [CONV]: No files have been modified in the past hour.\n')
		sys.exit(1)
	#read and write data for each file that has been modified
	for file in files:
		try:
			data = get_data(file)
			add_data(file,data)
		except NoPricesCollected as err:
			sys.stderr.write(f'{date} [CONV]: No prices have been collected from {str(err)}.\n')

