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
    return client['ProyectoFinal-Hoberman-v2']
    
# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":    
    
    # Get the database
    dbname = get_database()

    movies = dbname["Pelicula"]

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
            "descripcion" : i.get('overview'),
            "poster" : i.get('poster_path'),
            "+18" : i.get('adult'),
            "fecha" : i.get('release_date'),
            "promedio_votos" : i.get('vote_average'),
            "cant_votos" : i.get('vote_count'),
            "duracion" : i.get('runtime'),
            "lenguaje_original" : i.get('original_language'),
            #"popularidad": i.get('popularity'),
            "presupuesto" : i.get('budget'),
            #"estado": i.get('status'),
            #"tituloOriginal": i.get('original_title'),
            "lema": i.get('tagline'),
            "ganancia" : i.get('revenue'),
            "video": i.get('video'),
            "idiomas" : idiomas,
            "generos" : generos
        }
        movies.insert_one(item)
        contador = contador + 1
        if contador == 5000:
            contador = 0
            completado = completado + 1
            print("Completado: ",completado * 10 ,"%")
    print("TERMINO INSERT")

    f.close()
 