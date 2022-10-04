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
 """
 
from gettext import Catalog
from DISClib.ADT.list import size
import config as cf
import model
import csv
import datetime
from datetime import datetime
import time
csv.field_size_limit(2147483647)
from DISClib.DataStructures import liststructure as lt


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def newController():
    """
    Crea una instancia del modelo
    """
    control = {
        'model': None
    }
    control['model'] = model.newCatalog()
    return control
    
# Funciones para la carga de datos
def loadData(control):
    """
    Carga los datos de los archivos y cargar los datos en la
    estructura de datos
    """
    catalog = control['model']
    albums = loadAlbums(catalog)
    tracks = loadTracks(catalog)
    artist = loadArtist(catalog)
    return albums, tracks, artist


def loadAlbums(catalog):
    """
    Carga la informacion de los albums.
    """
    albumfile = cf.data_dir + 'spotify-albums-utf8-large.csv'
    input_file = csv.DictReader(open(albumfile, encoding='utf-8'))
    for album in input_file:
        try:
            fecha = datetime.strptime(album['release_date'], '%Y-%m-%d')
            fecha = int(fecha.year)
            album['release_date'] = fecha
            model.AddAlbum(catalog, album)
        except:
            try:
                 fecha2 = datetime.strptime(album['release_date'],'%b-%y')
                 fecha2 = int(fecha2.year)
                 album['release_date'] = fecha2
                 model.AddAlbum(catalog, album)
            except:
                 fecha3 = datetime.strptime(album['release_date'], '%Y')
                 fecha3 = int(fecha3.year)
                 model.AddAlbum(catalog, album)
    #print(catalog['albums'])
    return catalog['albums']

def loadTracks(catalog):
    """
    Carga la informacion importante de los tracks.
    """
    tracksfile = cf.data_dir + 'spotify-tracks-utf8-large.csv'
    input_file = csv.DictReader(open(tracksfile, encoding='utf-8'))
    for track in input_file:
        model.addTrack(catalog, track)
    return catalog['tracks']


def loadArtist(catalog):
    """
    Carga los artistas del csv. 
    """
    artistfile = cf.data_dir + 'spotify-artists-utf8-large.csv'
    input_file = csv.DictReader(open(artistfile, encoding='utf-8'))
    for artist in input_file:            
        model.AddArtist(catalog, artist)
    return sortArtist(catalog['artist'])

# Funciones de ordenamiento
def sortArtist(control):
    return model.sortArtists(control)

def sortAlbums(control):
    """
    Ordena los libros por average_rating
    """
    return model.sortAlbum(control)

def sortTracks(catalog):
    return model.sortTracks(catalog)

# Funciones de consulta sobre el catálogo


def getBestArtist(control, number):
    """
    Retorna los mejores artistas
    """
    return model.getBestArtist(control, number)

def listarAlbums(control, fecha1, fecha2):
    return model.listaPeriodoTiempoAlbums(control, fecha1, fecha2)

def findArtistDisco(artist_list, track_list, name):
    return model.findArtistDisco(artist_list, track_list, name)