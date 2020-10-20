# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst
from w3lib.html import remove_tags

#Define the items need to be scraped from the web page
class oneillItem(scrapy.Item):
    #Define item - 'Brand'
    Brand = scrapy.Field(
        input_processor= MapCompose(remove_tags),   #Taking methods as argument to scrape and removing the html tags
        output_processor= TakeFirst()
    )
    Reference = scrapy.Field(
        input_processor= MapCompose(remove_tags),   #Taking methods as argument to scrape and removing the html tags
        output_processor= TakeFirst()
    )
    Google_Search_Code = scrapy.Field(
        input_processor= MapCompose(remove_tags),   #Taking methods as argument to scrape and removing the html tags
        output_processor= TakeFirst()
    )
    Category = scrapy.Field(
        input_processor= MapCompose(remove_tags),   #Taking methods as argument to scrape and removing the html tags
        output_processor= TakeFirst()
    )
    Name = scrapy.Field(
        input_processor= MapCompose(remove_tags),   #Taking methods as argument to scrape and removing the html tags
        output_processor= TakeFirst()
    )
    Product_Page_URL = scrapy.Field(
        input_processor= MapCompose(remove_tags),   #Taking methods as argument to scrape and removing the html tags
        output_processor= TakeFirst()
    )
    Price_Euros = scrapy.Field(
        input_processor= MapCompose(remove_tags),   #Taking methods as argument to scrape and removing the html tags
        output_processor= TakeFirst()
    )

