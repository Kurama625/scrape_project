#Import required modules
import requests
from lxml import html
import pandas as pd
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
import os

#Define necessity for the request
cookie = '"country":"DEU"; "billingCurrency":"EUR"; "indicativeCurrency":""'
params = {"country": "DEU"}
headers = {"cookie": cookie,
          "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/77.0.3865.90 Safari/537.36"}

#Define Pandas Dataframe to temporarily store scraped data, setting 'next_page' value to begin with and the page count n
df = pd.DataFrame()
next_page = True
n = 1

#Continue scraping the web content till end of page (till 'next_page' value is nill)
while next_page:
    url = 'https://www.matchesfashion.com/intl/mens/shop/shoes?page={}&amp;noOfRecordsPerPage=240'.format(n)    #Define URL
    resp = requests.get(url=url, params=params, headers=headers)    #Sending request (method 'GET')
    tree = html.fromstring(resp.content)    #Creating HTML tree
    product_name = tree.xpath('//div[@class="lister__item__title"]/text()') #Fetching product names
    brand_name = tree.xpath('//div[@class="lister__item__details"]/text()') #Fetching brand names
    price = tree.xpath('//span[@class="lister__item__price-full"]/text()')  #Fetching prices

    #Formatting the list of prices as per requirement
    price_list = []
    for each in price:
        cost = each[1:]
        price_list.append(cost)

    image_url = tree.xpath('//img[starts-with(@class, "lazy")]/@data-original') #Fetching image URLs

    #Formatting the list of image URLs
    image_url_list = []
    for i in image_url:
        temp1 = "http:"+i
        image_url_list.append(temp1)

    product_url = tree.xpath('//a[contains(@class, "productMainLink")]/@href')  #Fetching product URLs

    #Formatting the list of product URLs
    product_url_list = []
    for j in product_url:
        temp2 = "https://www.matchesfashion.com"+j
        product_url_list.append(temp2)

    data = {'Name': product_name, 'Brand': brand_name, 'Price(EUR)': price_list, 'Image URL':image_url_list, 'Product URL': product_url_list}   #Creating dictionary of scraped data
    df1 = pd.DataFrame(data=data)   #Creating a temporary pandas dataframe
    df = df.append(df1, ignore_index=True)  #Recursive addition of scraped data to predefined dataframe
    try:
        next_page = tree.xpath('//li[@class="next"]')   #Fetching 'next_page' node from the HTML(if exist)
        n = n + 1   #Increment in page number
    except:
        break   #End the loop if 'next_page' is not found(end of page)

df.to_csv("scrape_matches_fashion.csv") #Writing to csv file from the dataframe

#Downloading the images using image_url to a folder in D drive
for image in image_url_list:
    val = str(str(image).split("product/")[1]).split("_")[0]    #Define a value using image_url to set file-name
    f = open("D:\python_img\{}.jpg".format(val), "wb")  #Oprn the file with path using the value
    f.write(requests.get(image).content)    #Download the image and write to the file
    f.close()   #Close the file

#Uploading to the google drive
gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)
path = r'D:\python_img'
for x in os.listdir(path):
    f = drive.CreateFile({'title': x})
    f.SetContentFile(os.path.join(path, x))
    f.Upload()
    f = None

#END OF CODE