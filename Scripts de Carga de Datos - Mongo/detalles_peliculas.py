import json
import regex
import re
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

    detalles_pelicula = dbname["Detalles_Peliculas"]
    pelicula = dbname["Pelicula"]
    # Opening JSON file
    f2 = open('credits.json',encoding='UTF-8')
    
    # returns JSON object as 
    # a dictionary
    data2 = json.load(f2)
    
    # Iterating through the json
    # list
    contador = 4999
    contadorA = 0
    contadorC = 0
    completado = 0
    print("Comienza Insertar datos desde credits.json")
    for j in data2:
        aux = j.get('cast')
        actores = []
        aux = re.sub('\".*\"','\'Invalido\'',aux)
        #aux = aux.replace('\'\'','\'')
        aux = aux.replace('None','\"None\"')
        try:
            actors = json.loads(aux.replace('\'','\"'))
            if actors != None:
                for a in actors:
                    actores.append({"nombre":a.get('name'), "personaje":a.get('character')})      
            else:
                actores = None  

            aux2 = j.get('crew')
            crew = []
            aux2 = re.sub('\".*\"','\'Invalido\'',aux2)
            #aux2 = aux2.replace('\'\'','\'')
            aux2 = aux2.replace('None','\"None\"')
            crewMem = json.loads(aux2.replace('\'','\"'))
            if crewMem != None:
                for c in crewMem:
                    crew.append({"nombre":c.get('name'),"rol":c.get('job'),"departamento":c.get('department')})
            else:
                crew = None

            objectId = pelicula.find_one({ "id": j.get('id')})
            item = {
                "idPelicula": objectId.get('_id'),
                "actores": actores,
                "detras_escena": crew
            }
            detalles_pelicula.insert_one(item)
            contador = contador + 1
            if contador == 5000:
                contador = 0
                completado = completado + 1
                #print("Errores en actores: ", contadorA)
                #print("Errores en crew: ", contadorC)
                print("Completado: ",completado * 10 ,"% - ","idPelicula: ", j.get('id'))
        except JSONDecodeError as e:
            #contadorA = contadorA + 1 
            #print(j.get('id'))
            pelicula.delete_one({"id": j.get('id')})
            pass

    f2.close()
    print("TERMINO INSERT")
    # Closing file


    # Opening JSON file
    f = open('movies_metadata.json',encoding='UTF-8')
    
    # returns JSON object as 
    # a dictionary
    data = json.load(f)
    
    # Iterating through the json
    # list
    contador2 = 0
    completado = 0
    print("Comienza Update datos desde movies_metadata.json")
    for i in data:
        aux= i.get('production_companies')
        if (aux!= None):
            try:
                prod_comp = json.loads(aux.replace('\'','\"'))
                companias = []
                if prod_comp != None:
                    for g in prod_comp:
                        companias.append({"nombre":g.get('name')})      
                else:
                    companias = None  
            except JSONDecodeError:
                pass
        aux2 = i.get('production_countries')
        paises = None
        if (aux2!= None):
            try:
                prod_country = json.loads(aux2.replace('\'','\"'))
                if prod_country != None:
                    paises = []
                    for s in prod_country:
                        val = list(s.values())
                        paises.append({"nombre":s.get('name'),"iso": val[0]})
            except (JSONDecodeError, TypeError):
                pass

        objectId = pelicula.find_one({ "id": i.get('id')})  

        if (objectId != None):
            query = {"idPelicula": objectId.get('_id')}
            item = {
                "poster" : i.get('poster_path'),
                'compania_prod': companias, 
                "presupuesto" : i.get('budget'),
                "ganancia" : i.get('revenue'),
                'pais': paises,
                "cant_votos" : i.get('vote_count'),
                "promedio_votos" : i.get('vote_average'),
                "pagina" : i.get('homepage'),
                "lenguaje_original" : i.get('original_language'),
                "lema": i.get('tagline'),
                "video": i.get('video')     
            }
            new_values = {"$set": item}
            detalles_pelicula.update_one(query, new_values)
        contador2 = contador2 + 1
        if contador2 == 5000:
            completado = completado + 1
            print("Completado: ",completado * 10 ,"% - ","Último idPelicula procesado: ", i.get('id'))
            contador2 = 0  
    
    f.close()
    print("TERMINO UPDATE")