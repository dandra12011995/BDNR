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

    peliculas = dbname["Pelicula"]

    # Opening JSON file
    f = open('movies_metadata.json',encoding='UTF-8')
    
    # returns JSON object as 
    # a dictionary
    data = json.load(f)
    
    # Iterating through the json
    # list
    contador = 0
    completado = 0
    for i in data:
        aux= i.get('genres')
        genres = json.loads(aux.replace('\'','\"'))
        generos = []
        if genres != None:
            for g in genres:
                generos.append({"nombre":g.get('name')})      
        else:
            generos = None  
        aux2 = i.get('spoken_languages')
        idiomas = None
        if (aux2!= None):
            try:
                spoken_lang = json.loads(aux2.replace('\'','\"'))
                if spoken_lang != None:
                    idiomas = []
                    for s in spoken_lang:
                        val = list(s.values())
                        idiomas.append({"nombre":s.get('name'),"iso": val[0]})
            except (JSONDecodeError) as e:
                pass
                                       
        item = {
            "id" : i.get('id'),
            "titulo" : i.get('title'),
            "fecha" : i.get('release_date'), 
            "descripcion" : i.get('overview'),
            "+18" : i.get('adult'),
            "duracion" : i.get('runtime'),
            "idiomas" : idiomas,
            "generos" : generos
        }
        peliculas.insert_one(item)
        contador = contador + 1
        if contador == 5000:
            completado = completado + 1
            print("Completado: ",completado * 10 ,"% - ","Último idPelicula procesado: ", i.get('id'))
            contador = 0  

    print("TERMINO INSERT")

    # Closing file
    f.close()
