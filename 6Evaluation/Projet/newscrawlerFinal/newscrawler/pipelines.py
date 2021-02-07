# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import pymongo
from pymongo import MongoClient
import hashlib
import time
from elasticsearch import Elasticsearch
ES_LOCAL = True


class TextPipeline(object):

    def process_item(self, item, spider):
        if item:
            item["id"] = item["id"]
            item["title"] = item["title"]
            item["dateArrive"] = item['dateArrive']
            item["dateDepart"] = item['dateDepart']
            item["nombreNuits"] = item["nombreNuits"]
            #item["etoiles"] = item["etoiles"]
            #item["adresse"] = item["adresse"]
            item["localisation"] = item["localisation"]
            item["prix"] = item["prix"]
            item["prixbis"] = item["prixbis"]
            item["avis"] = item["avis"]
            #item["notes"] = item["notes"]
            item["images"] = item["images"]
            return item
        else:
            raise DropItem("Missing title in %s" % item)


def hashId(string):
    hashcode = str(int(time.time())).encode('utf-8')
    _id = hashlib.sha1(hashcode).hexdigest()[:11] + string
    return _id


class MongoPipeline(object):

    collection_name = 'scrapy_items'

    def open_spider(self, spider):
        self.client = pymongo.MongoClient()
        self.db = self.client["hotelscom"]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))
        return item


class IndexElasticSearch(object):
    def open_spider(self, spider):
        # verif ca fonctionne sur un autre pc ????
        self.es_client = Elasticsearch(
            hosts=["localhost" if ES_LOCAL else "elasticsearch"])

        mapping = {
            "mappings": {
                "properties": {
                    "title": {
                        "type": "search_as_you_type"
                    }
                }

            }
        }

        self.es_client.indices.create(
            index='suggest_hotels', body=mapping)

    def process_item(self, item, spider):
        item_dict = dict(item)
        p_suggest = {
            "title": item_dict['title'],
        }
        self.es_client.index(
            index="hotels", doc_type='hotels', id=item['id'], body=item_dict)
        self.es_client.index(index="hotels", body=p_suggest)
        return item
