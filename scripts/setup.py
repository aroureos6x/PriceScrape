#!/usr/bin/python3

import os,sys,getpass

abspath = os.path.dirname(os.path.abspath(__file__)) 

def write_cronjob(ticker,type):
	'''
	Writes a cronjob that executes price_scrape.py and saves the data
	to the ticker's corrseponding file
	param ticker: string - ticker
	param type: string - 'stocks' or 'crypto'
	'''
	#create sting that indicates time
	time = '* * * * *'
	if type == 'stocks':
		time = '* 14-21 * * 1-5'
	#create strng that indicates output file
	path = os.path.abspath(__file__)
	outfile = f'{abspath}/../data/{type}_csvs/minute/m{ticker}.csv'
	errfile = f'{abspath}/../data/log/error.log'
	#combine into cmd
	cmd = f'{time} {abspath}/price_scrape.py {ticker} >> {outfile} 2>> {errfile}'
	#write command in crontab
	command = f'(crontab -l; echo "{cmd}") | sort - | uniq - | crontab -' #sort and uniq are added to ensure no duplicates
	#sys.stdout.write(command + '\n')
	#execute command
	os.system(command)

def write_reset_data(tickers):
	'''
	Creates and writes a bash script that will be used to clear
	data files.
	'''
	with open(f'{abspath}/reset_data.sh','w',encoding='utf-8') as file:
	#write shebang line
		file.write("#!/bin/bash\n")
	#write initial printf
		file.write('printf "" ')
		for ticker, type in tickers:
			path = f'{abspath}/../data/{type}_csvs/minute/m{ticker}.csv'
			file.write(f'> {path} ')


def write_rest():
	'''
	Writes one by one the rest cron jobs.
	param tickers: list -> strings of tickers
	'''
	#time
	time = '0 * * * *'
	#write convert_data.py command
	errfile = f'{abspath}/../data/log/error.log'
	cmd1 = f'{abspath}/convert_data.py 2>> {errfile}'
	#write reset_data.sh command
	cmd2 = f'{abspath}/reset_data.sh 2>> {errfile}'
	#write upload using git commands
	cmd3 = f"cd {abspath}/../data && git add . && git commit -m 'added data' && git pull && git push"
	#write final crontab command
	cmd = f'{time} {cmd1} ; {cmd2} ; {cmd3} ;'
	#write command in crontab
	command = f'(crontab -l; echo "{cmd}") | sort - | uniq - | crontab -' #sort and uniq are added to ensure no duplicates
	os.system(command)

if __name__ == '__main__':
	#ask to empty crontab
	if '-e' in sys.argv:
		os.system('echo "" | crontab -')

	#use sys.stdin to read input
	tickers = []
	for i in sys.stdin:
		#use regular expressions to get name of ticker and type
		ticker, type = i[:i.find(',')], i[i.find(',')+1:].strip()
		write_cronjob(ticker,type)
		tickers.append((ticker,type))
	if '-r' in sys.argv:
		write_reset_data(tickers)
		#change permissions for reset_data.sh
		os.system(f'sudo chmod +x {abspath}/reset_data.sh')
	write_rest()
	sys.stdout.write('Crontab setup complete.\n')
