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

from genericpath import getsize
import config as cf
import sys
default_limit = 1000000
sys.setrecursionlimit(default_limit*10)
import controller
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""
def newController():
    """
    Se crea una instancia del controlador
    """
    control = controller.newController()
    return control

def loadData():
    """
    Solicita al controlador que cargue los datos en el modelo
    """
    control = newController()
    albums, artist, tracks = controller.loadData(control)
    return  albums, tracks, artist

def printBestArtist(artist):
    size = lt.size(artist)
    if size:
        print(' Estos son los mejores artistas: ')
        for artist in lt.iterator(artist):
            print('Nombre: ' + artist['name'] + ' Popularidad: ' +
                  artist['artist_popularity'] + 'Seguidores: ' + artist['followers'] +
                  'Generos asociados:'+ artist['genres'])
    else:
        print('No se encontraron artistas')

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Mostrar albumes por periodo de tiempo dado")
    print("3- Encontrar los artistas más populares")
    print("4- Clasificar las canciones por popularidad")
    print("5- Encontrar la cancion mas popular de un artista")
    print("6- Encontrar la discografia de un artista")
    print("7- Clasificar las canciones por mayor distribucion")
    print("0- Salir")
"""
Menu principal
"""
control = newController()

while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        muestra = int(input("Ingrese el tamaño de la muestra: "))
        albums, artist, tracks = loadData()
        if (muestra > lt.size(albums)) or (muestra > lt.size(artist)) or (muestra > lt.size(tracks)):
            print("La muestra no debe ser mas grande que el tamaño de los datos")
        else:
            print("Cargando información de los archivos....")
            albums = lt.subList(albums, 1, muestra)
            artist = lt.subList(artist, 1, muestra)
            tracks = lt.subList(tracks, 1, muestra)
            print('Albums cargados: ' + str(lt.size(albums)))
            print('Artistas cargados: ' + str(lt.size(artist)))
            print('Tracks cargados: ' + str(lt.size(tracks)))
            #print(albums)
            print('Ultimos 3 elementos de albums: \n' + str(lt.getElement(albums, lt.size(albums))) +','+ str(lt.getElement(albums, lt.size(albums)-1))+','+ str(lt.getElement(albums, lt.size(albums)-2)))
            print('Ultimos 3 elementos de canciones: \n'+str(lt.getElement(tracks, lt.size(tracks))) +','+ str(lt.getElement(tracks, lt.size(tracks)-1))+','+ str(lt.getElement(tracks, lt.size(tracks)-2)))
            print('Ultimos 3 elementos de artistas: \n'+str(lt.getElement(artist, lt.size(artist))) +','+ str(lt.getElement(artist, lt.size(artist)-1))+','+ str(lt.getElement(artist, lt.size(artist)-2))) 
    elif int(inputs[0]) == 2:
        print("Ingrese el periodo de tiempo que desea usar")
        año_inicial = int(input("Año inicial: "))
        año_final = int(input("Año Final: "))
        listaalbums = controller.listarAlbums(albums, año_inicial, año_final)
        print("Cargando albumes por periodo de tiempo dado ....")
        print("El total de albums en el intervalo es de:", lt.size(listaalbums))
        print('Primeros 3 elementos del periodo dado son: \n' + str(lt.getElement(listaalbums, 1)) +'\n'+ str(lt.getElement(listaalbums, 2))+'\n'+ str(lt.getElement(listaalbums, 3)))
        print('Ultimos 3 elementos del periodo dado son: \n' + str(lt.getElement(listaalbums, lt.size(listaalbums))) +'\n'+ str(lt.getElement(listaalbums, lt.size(listaalbums)-1))+'\n'+ str(lt.getElement(listaalbums, lt.size(listaalbums)-2)))
    elif int(inputs[0]) == 3:
        number = input("Ingrese el TOP de artistas que desea consultar: ")
        artist = controller.getBestArtist(artist, int(number))
        print("Encontrando los artistas más populares....")
        print("El top", number, "de artistas son:")
        printBestArtist(artist)
    elif int(inputs[0]) == 4:
        print("Clasificando las canciones por popularidad....")
        controller.sortTracks(tracks)
        if lt.size(tracks) >= 3:
            print(f"\nLos 3 primeros tracks en la lista son: {str(lt.getElement(tracks, 1))}, {str(lt.getElement(tracks, 2))}, {str(lt.getElement(tracks, 3))}")
            print(f"\nLos 3 ultimos tracks en la lista son: {str(lt.getElement(tracks, lt.size(tracks)-2))}, {str(lt.getElement(tracks, lt.size(tracks)-1))}, {str(lt.getElement(tracks, lt.size(tracks)))}")
        else:
            print(tracks)
    elif int(inputs[0]) == 5:
        name = str(input("Ingrese al artista que desea consultar la cancion mas popular: "))
        print("Encontrando la cancion mas popular de", name, "....")
        controller.sortTracks(tracks)
        artist_disc = controller.findArtistDisco(artist, tracks, name)
        if len(artist_disc) != None:
            print(f"\nLa discografia de {name} es de {len(artist_disc)} canciones")
            print(f"\nLa cancion mas popular de {name} es: {artist_disc[0]}")
        else:
            print(f"\n{name} no tiene canciones dentro de la muestra de datos dada.")
    elif int(inputs[0]) == 6:
        name = input("Ingrese al artista que desea consultar su discografia:")
        print("Encontrando la discografia de", name,"....")
    elif int(inputs[0]) == 7:
        print("Clasificando las canciones por mayor distribucion....")
    else:
        sys.exit(0)
sys.exit(0)
