#Import required modules
import scrapy
from scrapy import Request
from scrapytwo.items import oneillItem  #Import items defined in items.py
from scrapy.loader import ItemLoader
import pandas as pd


#Load csv file to read inputs
csv = pd.read_csv(r'C:\Users\Prathap\PycharmProjects\pk_workspace\SCRAPYTWO\Greendeck Business Analyst Assignment Task 4 - Sheet1.csv')
brand_list = csv["Brand"]
reference_list = csv["Reference"]
google_code_list = csv["Google Search Code"]
category_list = csv["Category"]
name_list = csv["Name"]

#Class spider to crawl through web pages
class firstSpider(scrapy.Spider):
    name = "firstspi"   #Spider name
    allowed_domains = ["oneill.com"]    #Allowed domains

    def start_requests(self):
        #Sending url request for all reference codes
        for i in range(len(brand_list)):
            url = "https://www.oneill.com/fr/en/search?q={}".format(google_code_list[i])    #Define url using 'google reference code'
            yield Request(url=url, callback=self.parse, meta={'brand': brand_list[i],   #Passing corresponding brand name for reference code
                                                              'reference': reference_list[i],   #Passing reference code
                                                              'search_code': google_code_list[i],   #Passing google reference code
                                                              'category': category_list[i], #Passing corresponding category name for reference code
                                                              'name': name_list[i]})    #Passing corresponding product name for reference code

    def parse(self, response, **kwargs):
        l = ItemLoader(item=oneillItem(), selector=response)    #Assign item loader to target the item class defined(oneillItem()), selecting from the response
        brand = response.meta.get('brand')  #Collect brand name from meta data
        reference = response.meta.get('reference')  #Collect reference code from meta data
        search_code = response.meta.get('search_code')  #Collect search code from meta data
        category = response.meta.get('category')    #Collect category name from meta data
        name = response.meta.get('name')    #Collect name of the product from meta data
        product = response.xpath('//a[@class="product-tile__main-body"]/@href').extract()   #Capture the selector list object for product url as string
        l.add_value('Brand', brand) #Assigning item - 'brand'
        l.add_value('Reference', reference) #Assigning item - 'reference code'
        l.add_value('Google_Search_Code', search_code)  #Assigning item - 'Google Search Code'
        l.add_value('Category', category)   #Assigning item - 'Category'
        l.add_value('Name', name)   #Assigning item - 'Product Name'
        if product != []:
            l.add_value('Product_Page_URL', 'https://www.oneill.com'+product[0])    #Format and complete 'Product Page URL' if exist and assign the item
        else:
            l.add_value('Product_Page_URL', product)    #Assign the empty value as it is to 'Product Page URL' to the item
        l.add_xpath('Price_Euros', '//span[@class="sales"]/span[@class="value"]/@content')  #Assigning item - 'Price(Euros)'
        yield l.load_item()