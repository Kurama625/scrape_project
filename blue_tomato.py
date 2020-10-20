#Import required modules
import requests
from lxml import html
import pandas as pd

#Define the requirements for all requests
params = {"LAND AUSWÄHLEN": "Österreich"}
headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/77.0.3865.90 Safari/537.36"}

df = pd.DataFrame() #Define empty dataframe to store scraped data
next_page = True    #Define 'next_page' value to begin with
n = 1   #Set page number to 1

#Iterating over web url for all the pages
while next_page:
    url = "https://www.blue-tomato.com/de-AT/products/categories/Snowboard+Shop-00000000/?page={}".format(n)    #Define url with page number
    resp = requests.get(url=url, params=params, headers=headers)    #Send request
    tree = html.fromstring(resp.content)    #Create HTML tree
    product_name = tree.xpath('//div[@class="ellipsis"]/div/p/text()')  #Collecting product name using xpath
    brand_name = tree.xpath('//a[starts-with(@class, "name track-click track-load-producttile")]/@data-brand')  #Collect brand name using xpath
    price = tree.xpath('//span[@class="productdesc"]/span[1]/text()')   #Collect prices using xpath

    #Formatting the price list
    price_list = []
    for each in price:
        try:
            value = str(each.split("€")[1])[1:].replace(",", ".")
            price_list.append(value)
        except:
            continue

    image_url = tree.xpath('//li[@class="productcell "]/span/img/@src') #Collect image url using xpath

    #Formatting image url list
    image_url_list = []
    for each in image_url:
        temp = "http:"+each
        image_url_list.append(temp)

    product = tree.xpath('//span[@class="productdesc"]/a/@href')    #Collect product url using xpath

    #Formatting product url list
    product_url_list = []
    for each in product:
        product_url = "https://www.blue-tomato.com"+each
        product_url_list.append(product_url)

    data = {'Name': product_name, 'Brand': brand_name, 'Price(EUR)': price_list, 'Image URL': image_url_list, 'Product URL': product_url_list}  #Create dictionary of scraped data
    df1 = pd.DataFrame(data=data)   #Temporarily store the scraped data in a dataframe
    df = df.append(df1, ignore_index=True)  #Append the data to the predifined dataframe

    #Collecting 'next_page' value, if exists, from the page source
    try:
        next_page = tree.xpath('//li[@class="next browse"]/a/@data-label')  #Collect 'next-page' value using xpath
        n = n + 1   #Increment page number
    except:
        break   #If 'next-page' if None, break the while loop and proceed further

df.to_csv("scrape_blue_tomato.csv") #Write the scraped data from dataframe ton csv