# Mercado Libre Price Tracker

## Table of Contents


### Project Overview
This project aims to track the price of any good from MercadoLibre into a dataset that also contains its value in USD. It does so by leveraging the power of Python's web scrapping capabilities. 

### Data Sources

The information used by this project comes from two websites:

- Mercadolibre.com.ar (To get the info of the product you want)
- Dolarhoy.com (To get the Dólar Blue exchange rate)

### Tools

- Python - Web Scrapping, cleaning & formatting data
    - BeautifulSoup
    - os
    - requests
    - pandas
    - datetime
    - csv

### Preparation

The most important thing about this project was getting the right data from the web pages. Here is the code used to do so:

```python
url = "Here goes the link of the product you want to track. Right below is the example I used"

# 'https://articulo.mercadolibre.com.ar/MLA-1185361297-tijera-multiuso-de-acero-inoxidable-rompenueces-bremen-7721-_JM#reco_item_pos=0&reco_backend=machinalis-attributes-p2p&reco_backend_type=function&reco_client=home_cart-recommendations&reco_id=dff86d5e-c6f3-4018-a2fc-b3f086e76a0a'

page = requests.get(url)

soup1 = BeautifulSoup(page.content, 'html.parser')




# Let's get the item's title

title = soup1.find(class_ = 'ui-pdp-title').get_text()

title2 = title.replace('\xa0', ' ') # Arranging minor detail in the title

#Now its price, and let's make it int

price = soup1.find(class_ = 'andes-money-amount__fraction').get_text()

price2 = price.replace('.', '')

price_int = int(price2)
```

After getting everything from the product, it was time to get the exchange rate info:

```python
url2 = 'https://dolarhoy.com/'

page2 = requests.get(url2)

soup2 = BeautifulSoup(page2.text, 'html.parser')

dolar_blue = soup2.find_all(class_ = 'venta')[9].get_text()

dolar_blue_f = float(dolar_blue)

dolar_blue_f

usd_price = round(price_int / dolar_blue_f, 2)

usd_price
```

We also add a date since the idea is to keep tracking this product during long periods of time. 
```python
today = datetime.date.today()
```

After having all the data we want to add, it's time to create the csv file with all of it together: 
```python
#After the first run of this program we can comment out this part since it is not the idea to keep creating this csv

header = ['Title', 'ARS Price', 'Dólar Blue', 'USD Price', 'Date']
data = [title2, price_int, dolar_blue_f, usd_price, today]

with open('MLTracke3r.csv', 'w', newline='', encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerow(data)
```

We will also eventually need to append more data to the csv:
```python
with open('MLTracker.csv', 'a+', newline='', encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(data)
```

After we have each piece in place, it's time to create a function to automate this process:
```python
def price_tracker():
    url = 'https://www.mercadolibre.com.ar/lavarropas-automatico-samsung-ww70aa046b-inverter-blanco-200v-240v/p/MLA19906217#backend=item_decorator&backend_type=function&client=history-polycard'

    page = requests.get(url)

    soup1 = BeautifulSoup(page.content, 'html.parser')

    # Let's get the item's title

    title = soup1.find(class_ = 'ui-pdp-title').get_text()

    title2 = title.replace('\xa0', ' ') # Arranging minor detail in the title

    #Now its price, and let's make it int

    price = soup1.find(class_ = 'andes-money-amount__fraction').get_text()

    price2 = price.replace('.', '')

    price_int = int(price2) 

    url2 = 'https://dolarhoy.com/'

    page2 = requests.get(url2)

    soup2 = BeautifulSoup(page2.content, 'html.parser')

    dolar_blue = soup2.find_all(class_ = 'venta')[9].get_text()

    dolar_blue_f = float(dolar_blue)

    dolar_blue_f

    usd_price = round(price_int / dolar_blue_f, 2)

    usd_price

    today = datetime.date.today()

    
    data = [title2, price_int, dolar_blue_f, usd_price, today]

    with open('MLTracker.csv', 'a+', newline='', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(data)
```
Finally, we code the loop to keep track of the price for your desired time period (in seconds):
```python
# (Keeps running with your PC on)

while(True):
    price_tracker()
    time.sleep(86400) # 60 = 1 minute, 3600 = 1 hour, 86400 = 1 day, 604800 = 1 week, 2592000 = 1 month
```

### Limitations
- This script won't restart after you turn off your PC.

### Further improvements

- Allow the user to input the links of the products they want when it starts instead of pre-loading it in the code.
- Send you an email if the price drop below certain threshold
- Track the percentage of the change in price

### References

- The main idea of this project came from the youtuber [@AlexTheAnalyst](https://www.youtube.com/channel/UC7cs8q-gJRlGwj4A8OmCmXg).
- I used the help of [ChatGPT](https://chat.openai.com/) for some configurations as well
