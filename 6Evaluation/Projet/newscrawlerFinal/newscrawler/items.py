# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewscrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    title = scrapy.Field()
    dateArrive = scrapy.Field()
    dateDepart = scrapy.Field()
    nombreNuits = scrapy.Field()
    #etoiles = scrapy.Field()
    #adresse = scrapy.Field()
    localisation = scrapy.Field()
    prix = scrapy.Field()
    prixbis = scrapy.Field()
    avis = scrapy.Field()
    #notes = scrapy.Field()
    images = scrapy.Field()
