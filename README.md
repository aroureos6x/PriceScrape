# PriceScrape

## What is PriceScrape?

  PriceScrape is an easy-to-setup tool for Linux that collects prices of cryptocurrencies and stocks of your choice!
  
## How does it work?

  The prices are scraped from the yahoo finance website every minute and the prices are converted into hourly prices every hour.
  This is done by utilising cron. The data is stored in predetermined directories but the user has all the freedom to change
  the saving directory with a simple edit in crontab.
  
## How to setup?

  Setting up PriceScrape is pretty straightforward. All you have to do is to clone this repository, change permissions for PriceScrape/scripts/setup.py and   then run it. (please read "About setup.py" for more details on how it is run)
  
### Prerequisites:
    
    Python 3
    pip3
    cron and an already existing crontab
  You can find out how cron works here: https://phoenixnap.com/kb/set-up-cron-job-linux
  
  You must also create a list of the stocks and cryptocurrencies that you want their prices collected. The list must be a file where the tickers (as seen in yahoo finance) are written in the following format:
    
    BTC-USD,crypto
    ETH-USD,crypto
    AAPL,stocks
    TSLA,stocks
    
A demo list file is included in the repo.

### About setup.py

  setup.py must have the list mentioned in "Prerequisites" as input:
  
      $ /scripts/setup.py < /path/to/list
      
  setup.py options:<br>
    "-e" : empties crontab before writing in it<br>
    "-d" : installs required python modules<br>
    "-r" : will reset datafiles that containing minute prices every hour (after converting that data to hourly data)<br>
    All of these are by default off.
      
      $ /scripts/setup.py -e -r -d < /path/to/list
