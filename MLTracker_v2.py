from bs4 import BeautifulSoup
import requests
import time
import datetime
import pandas as pd
import csv
from IPython.display import display



def item(url):

    page = requests.get(url)

    soup1 = BeautifulSoup(page.content, 'html.parser')
    

    # Let's get the item's title

    title = soup1.find(class_ = 'ui-pdp-title').get_text()

    title2 = title.replace('\xa0', ' ') # Arranging minor detail in the title

    #Now its price, and let's make it int

    price = soup1.find(class_ = 'andes-money-amount__fraction').get_text()

    price2 = price.replace('.', '')

    price_int = int(price2) 

    return title2, price_int


# Now let's get the exchange rate

def exchange_rate():
    url2 = 'https://dolarhoy.com/'

    page2 = requests.get(url2)

    soup2 = BeautifulSoup(page2.text, 'html.parser')

    dolar_blue = soup2.find_all(class_ = 'venta')[9].get_text()

    dolar_blue_f = float(dolar_blue)

    return dolar_blue_f


# Here comes the dolar blue price

def dolar_price(price_int, dolar_blue_f):

    usd_price = round(price_int / dolar_blue_f, 2)

    return usd_price


# Time for the timestamp
def date():
    today = datetime.date.today()
    return today

#Now we create the csv -- After the first run of this program we can comment out this part since it is not the idea to keep creating this csv

def new_csv(title, ars_price, dolar_blue, usd_price, date):
    header = ['Title', 'ARS Price', 'Dólar Blue', 'USD Price', 'Date']
    data = [title, ars_price, dolar_blue, usd_price, date]

    with open('PriceTracker.csv', 'w', newline='', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerow(data)

    return data

# We eventually need to append more data to the csv:

def append_csv(data):
    with open('PriceTracker.csv', 'a+', newline='', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(data)

def timer():

    print("""
          "Select how often you would  like to perform the tracking:

            1: Every 1 hour
            2: Every 1 day
            3: Every 1 week
            4: Every 1 month
            5: Another time interval of your choice""")
    #60 = 1 minute, 3600 = 1 hour, 86400 = 1 day, 604800 = 1 week, 2592000 = 1 month
    while True:
        try:
            time = int(input("> "))
            break
        except ValueError:
            print("Invalid input. Please enter a valid number.")
        

    
    if time == 1:
        return 3600
    elif time == 2:
        return 86400
    elif time == 3:
        return 604800
    elif time == 4:
        return 2592000
    else:
        while True:
            try:
                seconds = int(input("Please write your desired intereval. The unit of measure is second (if you write 60, then it will be 1 minute): "))
                break
            except ValueError:
                print("Invalid input. Please enter a valid number.")
        
        return seconds
#Keeps running with your PC on
def loop(timer):
    global url
    while(True):
        title, ars_price = item(url)
        dolar_blue = exchange_rate()
        usd_price = dolar_price(ars_price, dolar_blue)
        today = date()

        data = [title, ars_price, dolar_blue, usd_price, today]

        append_csv(data) #= new_csv(title, ars_price, dolar_blue, usd_price, today)
        time.sleep(timer) # 60 = 1 minute, 3600 = 1 hour, 86400 = 1 day, 604800 = 1 week, 2592000 = 1 month

########################################################

#Main branch:


url = input('Insert the link of the item to track: ') # Link of the Item we are going to track -- In order to paste it in terminal, just right click on it and it will be copied. 

title, ars_price = item(url) # Title and ARS price of the tracked item

dolar_blue = exchange_rate() # Today's Exchange rate of ARS/USD in dolarhoy.com

usd_price = dolar_price(ars_price, dolar_blue) # Price in usd of the tracked item

today = date() # Today's date

data = new_csv(title, ars_price, dolar_blue, usd_price, today) # Input and creation of the csv file

period = timer() # To customize how often the tracking will be done


loop(period) # Loop to track and append new info for as long as the PC is on power, every once in a specific amount of time (in seconds). You can always directly select a number in seconds from here

# Keep in mind that this is a file whose purpose is to keep running, so if you want to stop it, just go to the terminal and press CTRL+C




