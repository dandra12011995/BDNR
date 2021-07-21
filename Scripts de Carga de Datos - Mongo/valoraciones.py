import json
from json import JSONDecodeError
def get_database():
    from pymongo import MongoClient
    import pymongo

    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    from pymongo import MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client['ProyectoFinal-Mongo-v2']
    
# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":    
    
    # Get the database
    dbname = get_database()

    valoraciones = dbname["Valoraciones"]
    pelicula = dbname["Pelicula"]
    # Opening JSON file
    f = open('ratings_small.json',encoding='UTF-8')
    
    # returns JSON object as 
    # a dictionary
    data = json.load(f)
    
    # Iterating through the json
    # list
    contador = 0
    completado = 0
    for i in data:
        objectId = pelicula.find_one({ "id": i.get('movieId')})
        if ( objectId!= None):
            item = {
                "idPelicula" : objectId.get('_id'),
                "idUsuario" : i.get('userId'),
                "valoracion" : i.get('rating'),
                "fecha": i.get('timestamp')
            }
            valoraciones.insert_one(item)
        contador = contador + 1
        if contador == 5000:
            contador = 0
            completado = completado + 1
            if completado != 21:
                print("Completado: ",completado * 5 ,"%")

    f.close()
    print("TERMINO INSERT")