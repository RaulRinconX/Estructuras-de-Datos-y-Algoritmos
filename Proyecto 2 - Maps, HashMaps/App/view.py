"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import sys
import config as cf
import controller
import tracemalloc
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
default_limit = 1000
sys.setrecursionlimit(default_limit*10)

assert cf
from time import process_time



"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
	print("Bienvenido")
	print("1- Cargar información en el catálogo")
	print("2- Examinar los albumes en un año de interes")
	print("3- Encontrar artista por popularidad")
	print("4- Encontrar las canciones por popularidad")
	print("5- Encontrar la cancion mas popular de un artista")
	print("6- Encontrar la discografia de un artista")
	print("7- Clasificar las canciones dde artista con mayor distribucion")

catalog = None
filePrefix = ("spotify-albums-utf8", "spotify-artists-utf8" , "spotify-tracks-utf8")
fileSize = ("-01pct.csv","-small.csv", "-large.csv", "-5pct.csv", "-10pct.csv", "-20pct.csv", "-30pct.csv", "-50pct.csv", "-80pct.csv")
file = [[f'{prefix}{size}' for prefix in filePrefix] for size in fileSize]

def first(year):
	totalNum, firstMonth, askedAlbums = controller.r1AlbumsInYear(catalog, year)
	print(f"El numero total de albumes en el anio {year} es de: {totalNum}")
	print(f"El numero de albumes en enero del anio {year} es de: {firstMonth}")
	
	for i in range(1,7):
		album = lt.getElement(askedAlbums, i)
		print(f"Nombre: {album['name']}")
		print(f"Fecha de publicacion: {album['release_date']}")
		print(f"Tipo de album: {album['album_type']}")
		print(f"Artista asociado al album: {album['artist_album_name']}")
		print(f"Numero de canciones del album: {album['total_tracks']}")
		print()
	
def second(popularity):
	totalArtist, threeFirstP, threeLastP = controller.r2ArtistByPopularity(catalog, popularity)
	print(f"El numero total de artistas con la popularidad {popularity} es de: {totalArtist}")	
	print("PRIMEROS 3 ARTISTAS: \n")
	for i in range(1,4):
		artist = lt.getElement(threeFirstP, i)
		print(f"Nombre: {artist['name']}")
		print(f"Popularida del artista: {artist['artist_popularity']}")
		print(f"Segidores del artista: {artist['followers']}")
		for genres in range(lt.size(artist['genres'])):
			print(f"Generos asociados: {lt.getElement(artist['genres'], genres)}")
		print()
	print("ULTIMOS 3 ARTISTAS: \n")
	for i in range(1,4):
		artist = lt.getElement(threeLastP, i)
		print(f"Nombre: {artist['name']}")
		print(f"Popularida del artista: {artist['artist_popularity']}")
		print(f"Segidores del artista: {artist['followers']}")
		for genres in range(lt.size(artist['genres'])):
			print(f"Generos asociados: {lt.getElement(artist['genres'], genres)}")
		print()
def third(popularity):
	totalTracks, threeFirstP, threeLastP = controller.r3FindTracksByPopularity(catalog, popularity)
	print(f"El numero total de canciones con la popularidad {popularity} es de: {totalTracks}")	
	print("PRIMERAS 3 CANCIONES: \n")
	for i in range(1,4):
		track = lt.getElement(threeFirstP, i)
		print(f"Nombre: {track['name']}")
		print(f"Nombre del album al que pertenece: {track['album_name']}")
		for artist in range(lt.size(track['artists_name'])):
			print(f"Artistas involucrados: {lt.getElement(track['artists_name'], artist)}")
		print(f"Popularidad de la cancion: {track['popularity']}")
		print(f"Duracion de la cancion en minutos: {track['duration_ms']/60000}")
		print(f"Enlace externo de Spotify: {track['href']}")
	#	print(f"Letra: {track['lyrics']}")
		print()
	print("ULTIMAS 3 CANCIONES: \n")
	for i in range(1,4):
		track = lt.getElement(threeLastP, i)
		print(f"Nombre: {track['name']}")
		print(f"Nombre del album al que pertenece: {track['album_name']}")
		for artist in range(lt.size(track['artists_name'])):
			print(f"Artistas involucrados: {lt.getElement(track['artists_name'], artist)}")
		print(f"Popularidad de la cancion: {track['popularity']}")
		print(f"Duracion de la cancion en minutos: {track['duration_ms']/60000}")
		print(f"Enlace externo de Spotify: {track['href']}")
	#	print(f"Letra: {track['lyrics']}")
		print()
	

def forth(artistName, market):
	tracksArtistMarket, albumsArtistMarket = controller.r4TrackMostPopularByArtist(catalog, artistName, market)
	print(f"El numero total de canciones del artista en {market}es de: {tracksArtistMarket}")	

def fifth(artistName):
	singles,compilations, albums,threeFirstP, threeLastP, mostPopular = controller.r5TracksByArtist(catalog, artistName)
	print(f"El numero total de albumes sencillos es de: {singles}")	
	print(f"El numero total de albumes de recopilacion: {compilations}")	
	print(f"El numero total de albumes de tipo album es: {albums}")	
	print(" 3 PRIMEROS ALBUMES\n")
	for i in range(1,4):
		album = lt.getElement(threeFirstP, i)
		print(f"Fecha de publicacion del album: {album['release_date']}")
		print(f"Nombre: {album['name']}")
		print(f"Numero de canciones del album: {album['total_tracks']}")
		print(f"Tipo de album: {album['total_tracks']}")
		print(f"Artista asociado al album: {album['artist_album_name']}")
		print()

	print(" 3 ULTIMOS ALBUMES\n")
	for i in range(1,4):
		album = lt.getElement(threeLastP, i)
		print(f"Fecha de publicacion del album: {album['release_date']}")
		print(f"Nombre: {album['name']}")
		print(f"Numero de canciones del album: {album['total_tracks']}")
		print(f"Tipo de album: {album['total_tracks']}")
		print(f"Artista asociado al album: {album['artist_album_name']}")
		print()
	print("INFORMACION DE LA CANCION MAS POPULAR:\n")
	cancion = mostPopular
	print(cancion)

	"""
o El nombre de la canción.
o Los nombres de los artistas involucrados en la canción.
o El tiempo de duración (duration_ms).
o Su valor de popularidad (popularity).
o El enlace al audio de muestra (preview_url).
o La letra de la canción (lyrics).
	"""

def sixth(market, artistName, number):
	mostCountedMarket, threeFirstLast = controller.r6TracksMostDistributedByArtists(catalog, market, artistName, number)
"""
Menu principal
"""
"""
t1Start = process_time()
t1End = process_time()
print("\nTiempo de ejecucion:",t1End-t1Start,"segundos\n")
"""
def info(album):
	print("Informacion album:\n", album)	

while True:
	printMenu()
	inputs = input('Seleccione una opción para continuar\n')
	if int(inputs[0]) == 1:
		print("Cargando información de los archivos ....\n")
		t1Start = process_time()
		catalog = controller.initCatalog()
		controller.loadCatalog(file[1], catalog)
		t1End = process_time()
		print("El total de albumes es:", controller.sizeCatalog(catalog["albums"]))
		print("El total de artistas es:", controller.sizeCatalog(catalog["artists"]))
		print("El total de canciones es:", controller.sizeCatalog(catalog["tracks"]))
		print("\nTiempo de ejecucion:",t1End-t1Start,"segundos\n")
		keys = mp.keySet(catalog["albums"])
		size = lt.size(keys)
		frst = lt.subList(keys, 0, 3)
		last = lt.subList(keys, size-3, 3)
		newList = lt.newList()
		print("Primeros 3 albumes:\n")
		for i in range(1,3):
			album = mp.get(catalog["albums"], lt.getElement(frst, i))

			info(album)
		print("Ultimos 3 albumes:\n")
		for i in range(1,3):
			album1 = mp.get(catalog["albums"], lt.getElement(last, i))
			info(album1)

	elif int(inputs[0]) == 2:
		year = input("Ingrese el anio de interes:")
		if (len(year)!= 4):
			print("Anio incorrecto")
		else:
			t1Start = process_time()
			first(year)
			t1End = process_time()
			print("\nTiempo de ejecucion REQ 1:",t1End-t1Start,"segundos\n")
	elif int(inputs[0]) == 3:
		popularity = int(input("Ingrese la popularidad por la cual quiere buscar :"))
		t1Start = process_time()
		second(popularity)
		t1End = process_time()
		print("\nTiempo de ejecucion REQ 2:",t1End-t1Start,"segundos\n")
	elif int(inputs[0]) == 4:
		popularity = int(input("Ingrese la popularidad por la cual quiere buscar :"))
		t1Start = process_time()
		third(popularity)
		t1End = process_time()
		print("\nTiempo de ejecucion REQ 3:",t1End-t1Start,"segundos\n")
	elif int(inputs[0]) == 5:
		artistName = input("Ingrese el nombre del artista:")
		market = input("ingrese el lugar que quiere buscar:")
		forth(artistName, market)
	elif int(inputs[0]) == 6:
		pass
	elif int(inputs[0]) == 7:
		pass
	else:
		sys.exit(0)
sys.exit(0)
