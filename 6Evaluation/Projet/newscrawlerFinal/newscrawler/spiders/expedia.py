import scrapy
from ..items import NewscrawlerItem
from pymongo import MongoClient
import unicodedata
import re
from scrapy import Request


class ExpediaFrSpider(scrapy.Spider):
    name = 'expedia'
    allowed_domains = ['expedia.fr']
    start_urls = ['https://www.expedia.fr/Hotel-Search?adults=2&d1=2021-02-01&d2=2021-02-07&destination=Dubaï%20%28et%20environs%29%2C%20Dubaï%2C%20Émirats%20arabes%20unis&directFlights=false&endDate=2021-02-07&guestRating=&hotelName=&latLong=25.266839%2C55.297733&localDateFormat=dd%2FMM%2Fyyyy&lodging=HOTEL&partialStay=false&popularFilter=HOTEL&price=4&regionId=553248635974547388&sort=RECOMMENDED&star=50&startDate=2021-02-01&useRewards=false',
    'https://www.expedia.fr/Hotel-Search?adults=2&d1=2021-02-01&d2=2021-02-07&destination=Dubaï%20%28et%20environs%29%2C%20Dubaï%2C%20Émirats%20arabes%20unis&directFlights=false&endDate=2021-02-14&latLong=25.266839%2C55.297733&localDateFormat=dd%2FMM%2Fyyyy&lodging=HOTEL&partialStay=false&popularFilter=HOTEL&price=4&regionId=553248635974547388&semdtl=&sort=RECOMMENDED&star=50&startDate=2021-02-08&theme=&useRewards=false&userIntent',
    'https://www.expedia.fr/Hotel-Search?adults=2&d1=2021-02-01&d2=2021-02-07&destination=New%20York%20%28et%20environs%29%2C%20New%20York%2C%20États-Unis%20d%27Amérique&directFlights=false&endDate=2021-02-07&latLong=40.75668%2C-73.98647&localDateFormat=dd%2FMM%2Fyyyy&lodging=HOTEL&partialStay=false&popularFilter=HOTEL&price=4&regionId=178293&semdtl=&sort=RECOMMENDED&star=50&startDate=2021-02-01&theme=&useRewards=false&userIntent',
    'https://www.expedia.fr/Hotel-Search?adults=2&d1=2021-02-01&d2=2021-02-07&destination=New%20York%20%28et%20environs%29%2C%20New%20York%2C%20États-Unis%20d%27Amérique&directFlights=false&endDate=2021-02-14&latLong=40.75668%2C-73.98647&localDateFormat=dd%2FMM%2Fyyyy&lodging=HOTEL&partialStay=false&popularFilter=HOTEL&price=4&regionId=178293&semdtl=&sort=RECOMMENDED&star=50&startDate=2021-02-08&theme=&useRewards=false&userIntent',
    'https://www.expedia.fr/Hotel-Search?adults=2&d1=2021-02-01&d2=2021-02-07&destination=Los%20Angeles%20%28et%20environs%29%2C%20Californie%2C%20États-Unis%20d%27Amérique&directFlights=false&endDate=2021-02-07&guestRating=&hotelName=&latLong=34.05072%2C-118.25477&localDateFormat=dd%2FMM%2Fyyyy&lodging=HOTEL&partialStay=false&popularFilter=HOTEL&price=4&regionId=178280&sort=RECOMMENDED&star=50&startDate=2021-02-01&useRewards=false',
    'https://www.expedia.fr/Hotel-Search?adults=2&d1=2021-02-01&d2=2021-02-07&destination=Los%20Angeles%20%28et%20environs%29%2C%20Californie%2C%20États-Unis%20d%27Amérique&directFlights=false&endDate=2021-02-14&latLong=34.05072%2C-118.25477&localDateFormat=dd%2FMM%2Fyyyy&lodging=HOTEL&partialStay=false&popularFilter=HOTEL&price=4&regionId=178280&semdtl=&sort=RECOMMENDED&star=50&startDate=2021-02-08&theme=&useRewards=false&userIntent',
    'https://www.expedia.fr/Hotel-Search?adults=2&d1=2021-02-01&d2=2021-02-07&destination=Tokyo%20%28et%20environs%29%2C%20Tokyo%20%28préfecture%29%2C%20Japon&directFlights=false&endDate=2021-02-07&latLong=35.675%2C139.76&localDateFormat=dd%2FMM%2Fyyyy&lodging=HOTEL&partialStay=false&popularFilter=HOTEL&price=4&regionId=179900&semdtl=&sort=RECOMMENDED&star=50&startDate=2021-02-01&theme=&useRewards=false&userIntent',
    'https://www.expedia.fr/Hotel-Search?adults=2&d1=2021-02-01&d2=2021-02-07&destination=Tokyo%20%28et%20environs%29%2C%20Tokyo%20%28préfecture%29%2C%20Japon&directFlights=false&endDate=2021-02-14&latLong=35.675%2C139.76&localDateFormat=dd%2FMM%2Fyyyy&lodging=HOTEL&partialStay=false&popularFilter=HOTEL&price=4&regionId=179900&semdtl=&sort=RECOMMENDED&star=50&startDate=2021-02-08&theme=&useRewards=false&userIntent',
    'https://www.expedia.fr/Hotel-Search?adults=2&d1=2021-02-01&d2=2021-02-07&destination=Tokyo%20%28et%20environs%29%2C%20Tokyo%20%28pr%C3%A9fecture%29%2C%20Japon&directFlights=false&endDate=2021-02-21&latLong=35.675%2C139.76&localDateFormat=dd%2FMM%2Fyyyy&lodging=HOTEL&partialStay=false&popularFilter=HOTEL&price=4&regionId=179900&semdtl=&sort=RECOMMENDED&star=50&startDate=2021-02-15&theme=&useRewards=false&userIntent',
    'https://www.expedia.fr/Hotel-Search?adults=2&d1=2021-02-01&d2=2021-02-07&destination=Tokyo%20%28et%20environs%29%2C%20Tokyo%20%28pr%C3%A9fecture%29%2C%20Japon&directFlights=false&endDate=2021-02-28&latLong=35.675%2C139.76&localDateFormat=dd%2FMM%2Fyyyy&lodging=HOTEL&partialStay=false&popularFilter=HOTEL&price=4&regionId=179900&semdtl=&sort=RECOMMENDED&star=50&startDate=2021-02-22&theme=&useRewards=false&userIntent',
    'https://www.expedia.fr/Hotel-Search?adults=2&d1=2021-02-01&d2=2021-02-07&destination=Los%20Angeles%20%28et%20environs%29%2C%20Californie%2C%20%C3%89tats-Unis%20d%27Am%C3%A9rique&directFlights=false&endDate=2021-02-21&latLong=34.05072%2C-118.25477&localDateFormat=dd%2FMM%2Fyyyy&lodging=HOTEL&partialStay=false&popularFilter=HOTEL&price=4&regionId=178280&semdtl=&sort=RECOMMENDED&star=50&startDate=2021-02-15&theme=&useRewards=false&userIntent',
    'https://www.expedia.fr/Hotel-Search?adults=2&d1=2021-02-01&d2=2021-02-07&destination=Los%20Angeles%20%28et%20environs%29%2C%20Californie%2C%20%C3%89tats-Unis%20d%27Am%C3%A9rique&directFlights=false&endDate=2021-02-28&latLong=34.05072%2C-118.25477&localDateFormat=dd%2FMM%2Fyyyy&lodging=HOTEL&partialStay=false&popularFilter=HOTEL&price=4&regionId=178280&semdtl=&sort=RECOMMENDED&star=50&startDate=2021-02-22&theme=&useRewards=false&userIntent',
    'https://www.expedia.fr/Hotel-Search?adults=2&d1=2021-02-01&d2=2021-02-07&destination=New%20York%20%28et%20environs%29%2C%20New%20York%2C%20%C3%89tats-Unis%20d%27Am%C3%A9rique&directFlights=false&endDate=2021-02-21&latLong=40.75668%2C-73.98647&localDateFormat=dd%2FMM%2Fyyyy&lodging=HOTEL&partialStay=false&popularFilter=HOTEL&price=4&regionId=178293&semdtl=&sort=RECOMMENDED&star=50&startDate=2021-02-15&theme=&useRewards=false&userIntent',
    'https://www.expedia.fr/Hotel-Search?adults=2&d1=2021-02-01&d2=2021-02-07&destination=New%20York%20%28et%20environs%29%2C%20New%20York%2C%20%C3%89tats-Unis%20d%27Am%C3%A9rique&directFlights=false&endDate=2021-02-28&latLong=40.75668%2C-73.98647&localDateFormat=dd%2FMM%2Fyyyy&lodging=HOTEL&partialStay=false&popularFilter=HOTEL&price=4&regionId=178293&semdtl=&sort=RECOMMENDED&star=50&startDate=2021-02-22&theme=&useRewards=false&userIntent',
    'https://www.expedia.fr/Hotel-Search?adults=2&d1=2021-02-01&d2=2021-02-07&destination=Duba%C3%AF%20%28et%20environs%29%2C%20Duba%C3%AF%2C%20%C3%89mirats%20arabes%20unis&directFlights=false&endDate=2021-02-21&latLong=25.266839%2C55.297733&localDateFormat=dd%2FMM%2Fyyyy&lodging=HOTEL&partialStay=false&popularFilter=HOTEL&price=4&regionId=553248635974547388&semdtl=&sort=RECOMMENDED&star=50&startDate=2021-02-15&theme=&useRewards=false&userIntent',
    'https://www.expedia.fr/Hotel-Search?adults=2&d1=2021-02-01&d2=2021-02-07&destination=Duba%C3%AF%20%28et%20environs%29%2C%20Duba%C3%AF%2C%20%C3%89mirats%20arabes%20unis&directFlights=false&endDate=2021-02-28&latLong=25.266839%2C55.297733&localDateFormat=dd%2FMM%2Fyyyy&lodging=HOTEL&partialStay=false&popularFilter=HOTEL&price=4&regionId=553248635974547388&semdtl=&sort=RECOMMENDED&star=50&startDate=2021-02-22&theme=&useRewards=false&userIntent']
    custom_settings = {
            'FEED_URI' : 'expedia.json',
            'FEED_FORMAT': 'json', 
            
           
        }

    # def parse(self, response):
    #     all_links = {
    #         name:response.urljoin(url) for name,url in zip(
    #         response.css(".uitk-flex-item.main-body.m-t-margin-two.l-t-margin-three.xl-t-margin-three"),
    #         response.css(".is-visually-hidden")
    #         )
    #     }
    #     for link in all_links.values():
    #         yield Request(link, callback=self.hotels)
    #         print(link)


    def parse(self, response):
        #requetes = response.xpath("//ol[starts-with(@class, 'results-list no-bullet')]")
        requetes = response.xpath("//li[starts-with(@class, 'uitk-spacing listing uitk-spacing-margin-blockstart-three horizontal')]")
        #requetes2 = response.xpath("//div[starts-with(@class, 'uitk-spacing uitk-spacing-margin-two')]")
        #requetes3 = response.xpath("//input[starts-with(@id, 'hotels-check-out')]")
        dateArrive = response.css("#hotels-check-in").css("::attr(value)").get()
        dateDepart =  response.css("#hotels-check-out").css("::attr(value)").get()
        id = response.css('.uitk-field.has-floatedLabel-label.has-icon.has-no-placeholder').css('input::attr(value)').get(),
        site = 'expedia'
        for i in requetes:
            yield{
            "site" : site,
            'id': id,
            'title' : i.css(".is-visually-hidden").css("h3::text").extract(),
            'dateArrive' : dateDepart,
            'dateDepart' : dateArrive,
            #adresse = i.css("#listings .address").css("::text").get(),#adresse de l'hotel
            'localisation' : i.css(".uitk-cell.all-cell-2-3.uitk-type-300 .overflow-wrap.uitk-spacing.uitk-spacing-padding-blockend-two.uitk-text-secondary-theme").css("::text").extract(),#localisation
            'prix' : i.css(".uitk-cell.loyalty-display-price.all-cell-shrink .uitk-cell.loyalty-display-price.all-cell-shrink").css("span::text").get(),#prix pour <ins>
            #avis = response.css(".listing__reviews.all-t-margin-two .uitk-type-300.pwa-theme--grey-700.all-r-padding-one").css("::text").get(),#nombre d'avis
            'avis' : i.css(".listing__reviews.all-t-margin-two .is-visually-hidden").css("::text").extract(),
            'nombreNuits' : i.css(".all-t-padding-one").css("::text").extract(),#nombre de nuits
            #etoiles = i.css(".all-b-padding-half .is-visually-hidden").css("::text").extract() ,#etoiles
            #notes = i.css(".uitk-type-300.uitk-type-bold.all-r-padding-one").css("::text").extract(),#notes
            #notesAvecavis = [unicodedata.normalize("NFKD",wor) for wor in response.css(".listing__reviews.all-t-margin-two .is-visually-hidden").css("::text").get()],
            'images' :i.css('img').xpath('@src').getall()#Images
            #response.css("#listings .property-image-link").css("img::attr(style)").get()#ImagesBis
            }
        
            # yield NewscrawlerItem(
            # id ="",
            # title = title,
            # dateArrive = dateArrive,
            # dateDepart = dateDepart,
            # nombreNuits = nombreNuits,
            #     #etoiles = etoiles,
            #     #adresse = adresse,
            # localisation = localisation,
            # prix = prix,
            # avis = avis,
            #     #notesAvecavis = notesAvecavis,
                #notes = notes,
                #images = images,
                
          