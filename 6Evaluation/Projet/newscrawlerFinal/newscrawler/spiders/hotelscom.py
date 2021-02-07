import scrapy
from ..items import NewscrawlerItem
from pymongo import MongoClient




client = MongoClient() #verif que ca fonctionne sur toutes les machines

database_hotelscom = client.refurbHotelscom
database_hotelscom['scrapy_items'].drop()

collection_product = database_hotelscom['scrapy_items']


class HotelComSpider(scrapy.Spider):
    name = 'hotelscom'
    allowed_domains = ['hotels.com']
    start_urls = ['https://fr.hotels.com/search.do?resolved-location=CITY%3A11594%3AUNKNOWN%3AUNKNOWN&f-price-currency-code=EUR&f-price-multiplier=6&f-price-min=1560&f-star-rating=5&f-accid=1&destination-id=11594&q-destination=Dubaï,%20Dubaï,%20Émirats%20arabes%20unis&q-check-in=2021-02-01&q-check-out=2021-02-07&q-rooms=1&q-room-0-adults=2&q-room-0-children=0',
    "https://fr.hotels.com/search.do?resolved-location=CITY%3A11594%3AUNKNOWN%3AUNKNOWN&f-price-currency-code=EUR&f-price-multiplier=6&f-price-min=1560&f-star-rating=5&f-accid=1&destination-id=11594&q-destination=Dubaï,%20Dubaï,%20Émirats%20arabes%20unis&q-check-in=2021-02-08&q-check-out=2021-02-14&q-rooms=1&q-room-0-adults=2&q-room-0-children=0",
    'https://fr.hotels.com/search.do?resolved-location=CITY%3A11594%3AUNKNOWN%3AUNKNOWN&f-price-currency-code=EUR&f-price-multiplier=6&f-price-min=1560&f-star-rating=5&f-accid=1&destination-id=11594&q-destination=Dubaï,%20Dubaï,%20Émirats%20arabes%20unis&q-check-in=2021-02-15&q-check-out=2021-02-21&q-rooms=1&q-room-0-adults=2&q-room-0-children=0',
    'https://fr.hotels.com/search.do?resolved-location=CITY%3A11594%3AUNKNOWN%3AUNKNOWN&f-price-currency-code=EUR&f-price-multiplier=6&f-price-min=1560&f-star-rating=5&f-accid=1&destination-id=11594&q-destination=Dubaï,%20Dubaï,%20Émirats%20arabes%20unis&q-check-in=2021-02-22&q-check-out=2021-02-28&q-rooms=1&q-room-0-adults=2&q-room-0-children=0',
    'https://fr.hotels.com/search.do?resolved-location=CITY%3A1506246%3AUNKNOWN%3AUNKNOWN&f-price-currency-code=EUR&f-price-multiplier=6&f-price-min=1560&f-star-rating=5&f-accid=1&destination-id=1506246&q-destination=New%20York,%20New%20York,%20États-Unis%20d%27Amérique&q-check-in=2021-02-01&q-check-out=2021-02-07&q-rooms=1&q-room-0-adults=2&q-room-0-children=0',
    'https://fr.hotels.com/search.do?resolved-location=CITY%3A1506246%3AUNKNOWN%3AUNKNOWN&f-price-currency-code=EUR&f-price-multiplier=6&f-price-min=1560&f-star-rating=5&f-accid=1&destination-id=1506246&q-destination=New%20York,%20New%20York,%20États-Unis%20d%27Amérique&q-check-in=2021-02-08&q-check-out=2021-02-14&q-rooms=1&q-room-0-adults=2&q-room-0-children=0',
    'https://fr.hotels.com/search.do?resolved-location=CITY%3A1506246%3AUNKNOWN%3AUNKNOWN&f-price-currency-code=EUR&f-price-multiplier=6&f-price-min=1560&f-star-rating=5&f-accid=1&destination-id=1506246&q-destination=New%20York,%20New%20York,%20États-Unis%20d%27Amérique&q-check-in=2021-02-15&q-check-out=2021-02-21&q-rooms=1&q-room-0-adults=2&q-room-0-children=0',
    'https://fr.hotels.com/search.do?resolved-location=CITY%3A1506246%3AUNKNOWN%3AUNKNOWN&f-price-currency-code=EUR&f-price-multiplier=6&f-price-min=1560&f-star-rating=5&f-accid=1&destination-id=1506246&q-destination=New%20York,%20New%20York,%20États-Unis%20d%27Amérique&q-check-in=2021-02-22&q-check-out=2021-02-28&q-rooms=1&q-room-0-adults=2&q-room-0-children=0',
    'https://fr.hotels.com/search.do?resolved-location=CITY%3A1439028%3AUNKNOWN%3AUNKNOWN&f-price-currency-code=EUR&f-price-multiplier=6&f-price-min=1530&f-star-rating=5&f-accid=1&destination-id=1439028&q-destination=Los%20Angeles,%20Californie,%20États-Unis%20d%27Amérique&q-check-in=2021-02-01&q-check-out=2021-02-07&q-rooms=1&q-room-0-adults=2&q-room-0-children=0',
    'https://fr.hotels.com/search.do?resolved-location=CITY%3A1439028%3AUNKNOWN%3AUNKNOWN&f-price-currency-code=EUR&f-price-multiplier=6&f-price-min=1530&f-star-rating=5&f-accid=1&destination-id=1439028&q-destination=Los%20Angeles,%20Californie,%20États-Unis%20d%27Amérique&q-check-in=2021-02-08&q-check-out=2021-02-14&q-rooms=1&q-room-0-adults=2&q-room-0-children=0',
    'https://fr.hotels.com/search.do?resolved-location=CITY%3A1439028%3AUNKNOWN%3AUNKNOWN&f-price-currency-code=EUR&f-price-multiplier=6&f-price-min=1530&f-star-rating=5&f-accid=1&destination-id=1439028&q-destination=Los%20Angeles,%20Californie,%20États-Unis%20d%27Amérique&q-check-in=2021-02-15&q-check-out=2021-02-21&q-rooms=1&q-room-0-adults=2&q-room-0-children=0',
    'https://fr.hotels.com/search.do?resolved-location=CITY%3A1439028%3AUNKNOWN%3AUNKNOWN&f-price-currency-code=EUR&f-price-multiplier=6&f-price-min=1530&f-star-rating=5&f-accid=1&destination-id=1439028&q-destination=Los%20Angeles,%20Californie,%20États-Unis%20d%27Amérique&q-check-in=2021-02-22&q-check-out=2021-02-28&q-rooms=1&q-room-0-adults=2&q-room-0-children=0',
    'https://fr.hotels.com/search.do?resolved-location=CITY%3A726784%3AUNKNOWN%3AUNKNOWN&f-price-currency-code=EUR&f-price-multiplier=6&f-price-min=1500&f-star-rating=5&f-accid=1&destination-id=726784&q-destination=Tokyo,%20Tokyo%20(préfecture),%20Japon&q-check-in=2021-02-01&q-check-out=2021-02-07&q-rooms=1&q-room-0-adults=2&q-room-0-children=0',
    'https://fr.hotels.com/search.do?resolved-location=CITY%3A726784%3AUNKNOWN%3AUNKNOWN&f-price-currency-code=EUR&f-price-multiplier=6&f-price-min=1500&f-star-rating=5&f-accid=1&destination-id=726784&q-destination=Tokyo,%20Tokyo%20(préfecture),%20Japon&q-check-in=2021-02-08&q-check-out=2021-02-14&q-rooms=1&q-room-0-adults=2&q-room-0-children=0',
    'https://fr.hotels.com/search.do?resolved-location=CITY%3A726784%3AUNKNOWN%3AUNKNOWN&f-price-currency-code=EUR&f-price-multiplier=6&f-price-min=1500&f-star-rating=5&f-accid=1&destination-id=726784&q-destination=Tokyo,%20Tokyo%20(préfecture),%20Japon&q-check-in=2021-02-15&q-check-out=2021-02-21&q-rooms=1&q-room-0-adults=2&q-room-0-children=0',
    'https://fr.hotels.com/search.do?resolved-location=CITY%3A726784%3AUNKNOWN%3AUNKNOWN&f-price-currency-code=EUR&f-price-multiplier=6&f-price-min=1500&f-star-rating=5&f-accid=1&destination-id=726784&q-destination=Tokyo,%20Tokyo%20(préfecture),%20Japon&q-check-in=2021-02-22&q-check-out=2021-02-28&q-rooms=1&q-room-0-adults=2&q-room-0-children=0'
    ]
    
    custom_settings = {
            'FEED_URI' : 'hotelscom.json',
            'FEED_FORMAT': 'json', 
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
           
        }
   
    def parse(self, response):
        requetes = response.xpath("//li[starts-with(@class, 'hotel vip')]")
        requetes2 = response.xpath("//li[starts-with(@class, 'hotel')]")
        requetes3 = response.xpath("//li[starts-with(@class, 'hotel sponsored')]")
        requetes4 = response.xpath("//li[starts-with(@class, 'hotel sponsored vip')]")
        #requetefinale = response.xpath("//ol[starts-with(@class, 'listings infinite-scroll-enabled')]")
        dateArrive = response.css("#q-localised-check-in").css("::attr(value)").extract()
        dateDepart = response.css("#q-localised-check-out").css("::attr(value)").extract()
        id = response.css(".widget-query-group.widget-query-destination").css("input::attr(value)").get()
        site = "hotels.com"
        for i in requetes:
            yield{
            'site' : site,
            'id' : id,
            'title' : i.css(".p-name").css("a::text").get(),
            'dateArrive' : dateArrive,
            'dateDepart' : dateDepart,
            #'adresse' : i.css(".address").css("::text").get(),#adresse de l'hotel
            'localisation' : i.css(".location-info.resp-module .map-link.xs-welcome-rewards").css("::text").extract()  ,#localisation
            'prix' : i.css(".price-link").css("ins::text").get(),#prix pour <ins>
            'prixbis' : i.css(".price-link").css("strong::text").get(),#prix pour <strong>
            'avis' : i.css(".small-view").css("span::text").get(),#nombre d'avis
            'nombreNuits' : i.css(".price-info").css("::text").get(),#nombre de nuits
            #'etoiles' : i.css(".star-rating-text").css("span::text").get(),#etoiles
            'notes' : i.css(".guest-reviews-badge").css("::text").get(),#notes
            'images' : i.css(".u-photo.use-bgimage.featured-img-tablet").css("::attr(style)").extract()#Images
            #response.css("#listings .property-image-link").css("img::attr(style)").getall`all()#ImagesBis
            }

        for i in requetes2:
            yield{
            'site' : site,
            'id' : id,
            'title' : i.css(".p-name").css("a::text").get(),
            'dateArrive' : dateArrive,
            'dateDepart' : dateDepart,
            #'adresse' : i.css(".address").css("::text").get(),#adresse de l'hotel
            'localisation' : i.css(".location-info.resp-module .map-link.xs-welcome-rewards").css("::text").extract(),#localisation
            'prix' : i.css(".price-link").css("ins::text").get(),#prix pour <ins>
            'prixbis' : i.css(".price-link").css("strong::text").get(),#prix pour <strong>
            'avis' : i.css(".small-view").css("span::text").get(),#nombre d'avis
            'nombreNuits' : i.css(".price-info").css("::text").get(),#nombre de nuits
            #'etoiles' : i.css(".star-rating-text").css("span::text").get(),#etoiles
            'notes' : i.css(".guest-reviews-badge").css("::text").get(),#notes
            'images' : i.css(".u-photo.use-bgimage.featured-img-tablet").css("::attr(style)").extract()#Images
            #response.css("#listings .property-image-link").css("img::attr(style)").getall`all()#ImagesBis
            }
        
        for i in requetes3:
            yield{
            'site' : site,   
            'id' : id,
            'title' : i.css(".p-name").css("a::text").get(),
            'dateArrive' : dateArrive,
            'dateDepart' : dateDepart,
            #'adresse' : i.css(".address").css("::text").get(),#adresse de l'hotel
            'localisation' : i.css(".location-info.resp-module .map-link.xs-welcome-rewards").css("::text").extract(),#localisation
            'prix' : i.css(".price-link").css("ins::text").get(),#prix pour <ins>
            'prixbis' : i.css(".price-link").css("strong::text").get(),#prix pour <strong>
            'avis' : i.css(".small-view").css("span::text").get(),#nombre d'avis
            'nombreNuits' : i.css(".price-info").css("::text").get(),#nombre de nuits
            #'etoiles' : i.css(".star-rating-text").css("span::text").get(),#etoiles
            'notes' : i.css(".guest-reviews-badge").css("::text").get(),#notes
            'images' : i.css(".u-photo.use-bgimage.featured-img-tablet").css("::attr(style)").extract()#Images
            #response.css("#listings .property-image-link").css("img::attr(style)").getall`all()#ImagesBis
            }

        for i in requetes4:
            yield{
            'site' : site,    
            'id' : id,
            'title' : i.css(".p-name").css("a::text").get(),
            'dateArrive' : dateArrive,
            'dateDepart' : dateDepart,
            #'adresse' : i.css(".address").css("::text").get(),#adresse de l'hotel
            'localisation' : i.css(".location-info.resp-module .map-link.xs-welcome-rewards").css("::text").extract(),#localisation
            'prix' : i.css(".price-link").css("ins::text").get(),#prix pour <ins>
            'prixbis' : i.css(".price-link").css("strong::text").get(),#prix pour <strong>
            'avis' : i.css(".small-view").css("span::text").get(),#nombre d'avis
            'nombreNuits' : i.css(".price-info").css("::text").get(),#nombre de nuits
            #'etoiles' : i.css(".star-rating-text").css("span::text").get(),#etoiles
            'notes' : i.css(".guest-reviews-badge").css("::text").get(),#notes
            'images' : i.css(".u-photo.use-bgimage.featured-img-tablet").css("::attr(style)").extract()#Images
            #response.css("#listings .property-image-link").css("img::attr(style)").getall`all()#ImagesBis
            }
        
        

        #yield scrapy.Request(requetes2, callback=self.parse)
        # yield NewscrawlerItem(
        #         #id = id,
        #         title = title,
        #         #dateArrive = dateArrive,
        #         #dateDepart = dateDepart,
        #         nombreNuits = nombreNuits,
        #         etoiles = etoiles,
        #         adresse = adresse,
        #         #localisation = localisation,
        #         prix = prix,
        #         #prixbis = prixbis,
        #         avis = avis,
        #         notes = notes,
        #         #images = images,
        # )
            
 
