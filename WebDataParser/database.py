import json
from json import dumps

from pymongo import MongoClient


class Database:

    client = MongoClient("mongodb://127.0.0.1:27017/ProductList")
    db = client.get_default_database()

    @staticmethod
    def getProductInfo(condition):
        try:
            #condition = { "product_list.product": "shoes", "product_list.brand":"adidas" }
            d = Database.db.Product.aggregate([
                { "$match": condition },
                { "$unwind": "$product_list" },
                { "$match": condition },
                { "$group": {
                    "_id": "$_id",
                    "product_list": { "$push": "$product_list" }
                }},
                {
                    "$project":{"product_list" : 1, "_id":0}
                }
            ])            
            return list(d)
            
        except:
            return []

    @staticmethod
    def getFeatureList(condition):
        d = Database.getProductInfo(condition)
        p = d[0]["product_list"][0].keys()
        p.remove("product")
        return p
        


    @staticmethod
    def getProductList(condition): 
        d = Database.getProductInfo(condition) 
        listProduct = []
        Products = d[0]["product_list"]
        for product in Products:
            listProduct.append(product["product"])
        return list(set(listProduct))


    @staticmethod
    def getFeatureInfo(condition,feature):
        d = Database.getProductInfo(condition) 
        listProduct = d[0]["product_list"]
        listFeature = []
        for product in listProduct:
            ft = product[feature]
            if isinstance(ft, list):
                for f in product[feature]:
                    listFeature.append(f)
            else:
                listFeature.append(product[feature])
        return list(set(listFeature))


    @staticmethod
    def storeProductInfo():
        """
        This function is used only to push dummy data into database for prototyping. Actual data into database will come from
        scrapy application
        """
        bulk = Database.db.Product.update(
            {"Key":"amazon.com"},
            {"$set":
            { "product_list": 
                [
                    {
                        "product": "shoes",
                        "brand": "adidas",
                        "price": "50",
                        "size": ["4","6","7","8","9","10","11","12"],
                        "color": ["red","blue","green","white","black"]
                    },
                    {
                        "product": "shoes",
                        "brand": "nike",
                        "price": "100",
                        "size": ["4","6","7","8","9","10","11","12"],
                        "color": ["red","blue","green","white","black"]
                    },
                    {
                        "product": "shoes",
                        "brand": "nike",
                        "price": "70",
                        "size": ["4","6","7","10","11","12"],
                        "color": ["white","black"]
                    },
                    {
                        "product": "jeans",
                        "style": "tight fit",
                        "brand": "levis",
                        "price": "38",
                        "size": ["28","30","32","34","38"],
                        "color": ["blue","green","white","black"]
                    },
                    {
                        "product": "jeans",
                        "style": "regular fit",
                        "brand": "levis",
                        "price": "28",
                        "size": ["28","30","32","34","38"],
                        "color": ["blue","green","white","black"]
                    },
                    {
                        "product": "jeans",
                        "brand": "old navi",
                        "price": "28",
                        "size": ["28","30","32","34","38"],
                        "color": ["blue","green","black"]
                    },

                ]
            }
        },
        upsert = True
        )

