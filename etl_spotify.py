from dotenv import load_dotenv
import os
import base64
from requests import post, get, request

# Con esto busco los IDs en el archivo .env que configuré previamente
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# Esta función consulta la API de Spotify para conseguir el Token y así poder acceder a los datos de la misma (Dura una hora).

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,  
        "Content-Type": "application/x-www-form-urlencoded" 
    }
    
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    
    # Verifica si la solicitud fue exitosa (código de respuesta 200)
    if result.status_code == 200:
        json_result = result.json()
        token = json_result["access_token"]
        return token
    else:
        print("Error al obtener el token. Código de respuesta:", result.status_code)
        return None

# Esta función contiene el Token y las autenticación necesaria para cada query o consulta a la API.

def get_auth_header(token):
    return {"Authorization" : "Bearer " + token}

# Esta función busca los datos de un artista en concreto.

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"
    
    query_url = url + query
    result = get(query_url, headers = headers)
    json_result = result.json()["artists"]["items"]
    if len(json_result) == 0:
        print("No hay artista con este nombre...")
        return None
    
    return json_result[0]

# Esta función arroja las TOP 10 canciones del artista mediante su ID.

def songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=AR"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = result.json()["tracks"]
    return json_result


# Acá comienza el programa para la extracción de los datos.

token = get_token()
if token:
    print("Token de acceso:", token)
else:
    print("No se pudo obtener el token.")

# En la siguiente linea, el usuario puede elegir un artista en concreto.

nombre = input("Elija el nombre de un artista: ")   
result = search_for_artist(token, nombre)
artist_id = result["id"]
print(result["name"])

# Imprime en consola el artist_id 

#print(artist_id)

songs = songs_by_artist(token, artist_id)

# Iteración para enumerar y seleccionar solamente el nombre de las canciones

for i, song in enumerate(songs):
    print(f"{i + 1}. {song['name']}")