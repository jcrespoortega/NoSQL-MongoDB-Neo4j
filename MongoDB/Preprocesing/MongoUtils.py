from pymongo import MongoClient
from bson import json_util

class MongoUtils():

    def __init__(self):
        self.ip_mongo = '127.0.0.1'
        self.puerto_mongo = 27017

    def importa_ficheros (self):
        print("Importando autores.json")
        with open('autores.json') as autores:
            self.sendMongo(autores, 'PracticaDDBB', 'autores')


        print("Importando publicaciones.json")
        with open('publicaciones.json') as pubs:
            self.sendMongo(pubs, 'PracticaDDBB', 'publicaciones')




    def sendMongo(self, file, database, collection):

        connection = MongoClient(self.ip_mongo, self.puerto_mongo)
        db = connection.get_database(database)
        posts = db.get_collection(collection)
        data = json_util.loads(file.read())
        result = posts.insert_many(data)
        result.inserted_ids

        connection.close()