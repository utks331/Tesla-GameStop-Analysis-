##Extracting and visualizing data for the tesla and gamestop stocks
#1. Tesla Stock Data
import yfinance as yf;
import pandas as pd;
import requests;
from bs4 import BeautifulSoup;
import warnings;
import matplotlib.pyplot as plt
# Ignores all warnings 
warnings.filterwarnings('ignore',category=FutureWarning)
#Defining the function makegraph that accepts the stock data dataframe(cols = Date and close), revenue dataframe that accepts(cols = Date and revenue) and the stock name 
def makegraph(stock_data, revenue_data, stock):
    stock_specific_data = stock_data[stock_data.Date<='2021-06-14']
    revenue_specific_data = revenue_data[revenue_data.Date<='2021-04-30']
    fig,axes = plt.subplots(2,1,figsize = (12,8),sharex=True)
    # Stock Data 
    axes[0].plot(pd.to_datetime(stock_specific_data.Date),stock_specific_data.Close.astype('float'), label = "share-price", color = "blue")
    axes[0].set_ylabel("Price($US)")
    axes[0].set_title(f"{stock}-Historical Share price")
    #Revenue data
    axes[1].plot(pd.to_datetime(revenue_specific_data.Date),revenue_specific_data.Revenue.astype('float'), label = "Revenue", color = "green")
    axes[1].set_ylabel("Revenue($US Millions)")
    axes[1].set_title(f"{stock}-Historical Revenue price")
    plt.tight_layout()
    plt.show()
Tesla = yf.Ticker("TSLA")
tesla_data = Tesla.history(period = "max")
tesla_data.reset_index(inplace=True)
print(tesla_data.head())
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm " 
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
response = requests.get(url, headers=headers)
tables = pd.read_html(url)
tesla_revenue = tables[1]
tesla_revenue.columns = ['Date', 'Revenue']
tesla_revenue['Revenue'] = tesla_revenue['Revenue'].str.replace(',|\$','', regex=True)
tesla_revenue.dropna(inplace=True)
tesla_revenue = tesla_revenue[tesla_revenue['Revenue']!='']
print(tesla_revenue.tail(5))
#2. Extracting Gamestop stock 
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"
gamestop = yf.Ticker("GME")
gme_data = gamestop.history(period = "max")
gme_data.reset_index(inplace=True)
response = requests.get(url)
html_data = response.text
soup = BeautifulSoup(html_data,'html.parser')
tables = pd.read_html(url, match="GameStop Quarterly Revenue")
gme_revenue = tables[0]
gme_revenue.columns = ['Date', 'Revenue']
gme_revenue['Revenue'] = gme_revenue['Revenue'].str.replace(",|\$",'', regex=True)
gme_revenue.dropna(inplace=True)
gme_revenue = gme_revenue[gme_revenue['Revenue']!='']

#Plotting tesla stock graph 
makegraph(tesla_data,tesla_revenue,'Tesla')
makegraph(gme_data, gme_revenue,'Gamestop')


