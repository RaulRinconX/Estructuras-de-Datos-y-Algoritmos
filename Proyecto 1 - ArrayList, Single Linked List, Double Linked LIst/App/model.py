"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


from gettext import Catalog
from heapq import merge
from unicodedata import name
from datetime import date, datetime
import time
from webbrowser import get
import config as cf
from DISClib.ADT import list as lt
from DISClib.Algorithms.Sorting import insertionsort as insertion
from DISClib.Algorithms.Sorting import mergesort as merge
from DISClib.Algorithms.Sorting import quicksort as quick
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.DataStructures import singlelinkedlist as slt
from DISClib.Algorithms.Sorting import mergesort as merge
from DISClib.Algorithms.Sorting import quicksort as quick
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newCatalog():
    """
    Inicializa el catálogo de spotify. Crea una lista vacia para guardar
    todos los albumes, adicionalmente, crea una lista vacia para los artistas,
    una lista vacia para los tracks. Retorna el catalogo inicializado.
    """
    catalog = {'albums': None,
               'artist': None,
               'tracks': None}

    catalog['albums'] = lt.newList('ARRAY_LIST') 
    catalog['artist'] = lt.newList('ARRAY_LIST')
    catalog['tracks'] = lt.newList('ARRAY_LIST')

    return catalog

# Funciones para agregar informacion al catalogo
def AddAlbum(catalog, album):
    t = newAlbum(album['id'], album['name'], album['release_date'], album['artist_id'], album['album_type'], album['available_markets'], album['total_tracks'])
    lt.addLast(catalog["albums"], t)
    return catalog
def AddArtist(catalog, artist):
    t = newArtist(artist['id'], artist['name'], artist['artist_popularity'], artist['followers'], artist['genres'])
    lt.addLast(catalog["artist"], t)
    return catalog
def addTrack(catalog, track):
    t = newTrack(track['name'], track['id'],  track['duration_ms'], track['popularity'], track['artists_id'], track['available_markets'], track['album_id'])
    lt.addLast(catalog["tracks"], t)
    return catalog

# Funciones para creacion de datos

def newArtist(id, name, artist_popularity, followers, genres):
    """
    Crea una nueva estructura para guardar los artistas que hay.
    """
    artist = {'id':"", 'name': "", "artist_popularity": "", 'followers': "", 'genres':''}
    artist['id'] = id
    artist['name'] = name
    artist['artist_popularity'] = artist_popularity
    artist['followers'] = followers
    artist['genres'] = genres
    return artist


def newAlbum(id, name, release_date, artist_id, album_type, available_markets, total_tracks):
    """
    Esta estructura almacena los album de un artista.
    """
    album = {'id':"", 'name': '', 'release_date': '', 'artist_id': '', 'album_type':'','available_markets': '', 'total_tracks': ''}
    album['id'] = id
    album['name'] = name
    album['release_date'] = release_date
    album['artist_id'] = artist_id
    album['album_type'] = album_type
    album['available_markets'] = available_markets
    album['total_tracks'] = total_tracks
    return album


def newTrack(name, id, duration_ms, popularity, artists_id, available_markets, album_id):
    """
    Esta estructura almacena las canciones que hay en el csv.
    """
    track = {'name': '', 'id': '', 'duration_ms': '', 'popularity': '', 'artists_id': '', 'available_markets': '', 'album_id' : ''}
    track['name'] = name
    track['id'] = id
    track['duration_ms'] = duration_ms
    track['popularity'] = popularity
    track['artists_id'] = artists_id
    track['available_markets'] = available_markets
    track['album_id'] = album_id
    return track


# Funciones de consulta
def getAlbumsByDate(catalog, authorname):
    """
    Retorna un autor con sus libros a partir del nombre del autor
    """
    posauthor = lt.isPresent(catalog['authors'], authorname)
    if posauthor > 0:
        author = lt.getElement(catalog['authors'], posauthor)
        return author
    return None

def getBestArtist(catalog, number):
    """
    Retorna los mejores artistas
    """
    bestartist = lt.newList()
    for cont in range(1, number+1):
        artist = lt.getElement(catalog, cont)
        lt.addLast(bestartist, artist)
    return bestartist
    """
    artist = lt.subList(catalog['artist'], 1, number)
    return artist
    """

def AlbumSize(catalog):
    return lt.size(catalog['albums'])
def ArtistsSize(catalog):
    return lt.size(catalog['artist'])
def TracksSize(catalog):
    return lt.size(catalog['tracks'])


# Funciones utilizadas para comparar elementos dentro de una lista
def cmpArtistByPopularity(artist1, artist2):
    if int(float(artist1['artist_popularity'])) == int(float(artist2['artist_popularity'])):
        return 0
    elif int(float(artist1['artist_popularity'])) > int(float(artist2['artist_popularity'])):
        return 1
    return -1
    
def cmpReleaseDate(album1, album2):
    
    """
    fecha1 = datetime.strptime(album1['release_date'], '%Y-%m-%d')
    fecha2 = datetime.strptime(album2['release_date'], '%Y-%m-%d')
    """
    fecha1 = album1['release_date']
    fecha2 = album2['release_date']
    if int(fecha1) == int(fecha2):
        return 0
    elif int(fecha1) > int(fecha2):
        return 1
    return -1

def cmpSongsByPopularity(song1, song2):
    if (song1['popularity'] != '') and (song2['popularity'] != ''):
        if int(float(song1['popularity'])) == int(float(song2['popularity'])):
            return int(float(song1['duration_ms'])) > int(float(song2['duration_ms']))
        elif int(float(song1['duration_ms'])) == int(float(song2['duration_ms'])):
            return song1['name'].rstrip() > song2['name'].rstrip()
        return int(float(song1['popularity'])) > int(float(song2['popularity']))

# Funciones de ordenamiento
def sortArtists(catalog):
    ordenar_artistas = quick.sort(catalog, cmpArtistByPopularity)
    return ordenar_artistas
    
def sortTracks(catalog):
    tracks_ordenados = quick.sort(catalog, cmpSongsByPopularity)
    return tracks_ordenados

def sortAlbum(catalog):
     ordenada = quick.sort(catalog, cmpReleaseDate)
     return ordenada

#REQUERIMIENTO 1

def listaPeriodoTiempoAlbums(catalog, fecha1, fecha2):
    nuevalista = lt.newList()
    for i in range(lt.size(catalog)):
         albumData = lt.getElement(catalog, i)
         if int(fecha1) <= int(albumData['release_date']) <= int(fecha2):
            lt.addLast(nuevalista, albumData)
    return nuevalista

#REQUERIMIENTO 4

def findArtistDisco(artist_list, track_list, name):
    artist_discography = []
    for artist in artist_list['elements']:
        if name == artist['name']:
            artist_id = artist['id']
            artist_id.rstrip()
    for track in track_list['elements']:
        track['artists_id'] = track['artists_id'].strip(" [] ").replace(" ","").replace("'", "").split(",")
        if len(track['artists_id']) > 1:
            for element in track['artists_id']:
                if artist_id == element:
                    artist_discography.append(track)
        elif len(track['artists_id']) == 1:
            if artist_id == track['artists_id'][0].rstrip():
                artist_discography.append(track)
    if len(artist_discography) == 0:
        print("No se encontraron canciones")
    else:
        return artist_discography

#REQUERIMIENTO 5

# Medir tiempos de ejecucion

def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def deltaTime(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed
