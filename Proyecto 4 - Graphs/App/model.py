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

from re import T
import sys
sys.setrecursionlimit(200000)
from DISClib.Algorithms.Graphs import dijsktra
from DISClib.Algorithms.Graphs import scc 
import config as cf
from DISClib.ADT import map as mp
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.ADT import graph as gr
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.ADT import stack as st
from datetime import datetime as dt
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newCatalog():
    catalog = {
    "Trip Id": None,
    "Trip Duration": None,
    "Start Station Id": None,
    "Start Time": None,
    "Start Station Name": None,
    "End Station Id": None,
    "End Time": None,
    "End Station Name": None,
    "Bike Id": None,
    "User Type": None,
    "Connections Directed": None,
    "Connections Notdirected": None,
    "Stations": None
    }
    
    catalog['arcos'] = mp.newMap()

    catalog['Stations'] = mp.newMap()
                                    
    catalog['Connections Directed'] = gr.newGraph(datastructure="ADJ_LIST",
                                   directed=True,
                                   size=800,
                                   comparefunction=None
                                   )
    
    catalog['Connections NotDirected'] = gr.newGraph(datastructure="ADJ_LIST",
                                   directed=False,
                                   size=800,
                                   comparefunction=None
                                   )

    catalog['Req6'] = mp.newMap()

    catalog['Req5'] = om.newMap(omaptype='RBT')

    catalog['contador'] = 0
    return catalog
# Funciones para agregar informacion al catalogo
def newTrip(catalog, strtStat, endStat, trip, graphType):
    addTripStation(catalog, trip, "Start Station")
    addTripStation(catalog, trip, "End Station")
   # origin = mp.get(catalog['Stations'], strtStat)['value']
   # destination = mp.get(catalog['Stations'], endStat)['value']
    duration = trip['Trip Duration']
    addStation(catalog, strtStat, graphType)
    addStation(catalog, endStat, graphType)
    key = strtStat+"##"+endStat
    addArco(catalog, key, trip)
    addCasualMembers(catalog, trip, strtStat)
   #addConnection(catalog, strtStat, endStat, duration, graphType)
    ###########
    secondtrip = mp.newMap()
    if mp.contains(catalog['Req6'], trip['Bike Id']):
        secondtrip = me.getValue(mp.get(catalog['Req6'], trip['Bike Id']))
        mp.put(secondtrip, trip['Trip Id'], trip)
    else:
        mp.put(secondtrip, trip['Trip Id'], trip)
        mp.put(catalog['Req6'], trip['Bike Id'], secondtrip)
    ###########
    if trip['User Type'] == 'Annual Member':
        fecha = dt.strptime(trip['Start Time'], '%m/%d/%Y %H:%M')
        dia = fecha.strftime('%m/%d/%Y')
        secondfecha = mp.newMap()
        if om.contains(catalog['Req5'], dia):
             secondfecha = me.getValue(mp.get(catalog['Req5'], dia))
             mp.put(secondfecha, trip['Trip Id'], trip)
        else:
             mp.put(secondfecha, trip['Trip Id'], trip)
        om.put(catalog['Req5'], dia, secondfecha )
    ##########
    return catalog

def addArco(catalog, key, trip):
    if not mp.contains(catalog['arcos'], key):
        value = {"total": 1, "sumapesos":int(trip['Trip Duration'])}
        value['promedio'] = value['sumapesos']/value['total']
        mp.put(catalog['arcos'], key, value)
    else:
        value = me.getValue(mp.get(catalog['arcos'], key))
        value['total'] += 1
        value['sumapesos'] += int(trip['Trip Duration'])
        value['promedio'] = value['sumapesos']/value['total']
        mp.put(catalog['arcos'], key, value)

def addStation(catalog, station, graphType):

    "Agrega estacion como vertice"

    if not gr.containsVertex(catalog[f'Connections {graphType}'], station):
        gr.insertVertex(catalog[f'Connections {graphType}'], station)
    return catalog

def addCasualMembers(catalog, trip, station):
    contadorCasual = 0
    if trip['Start Station Name'] == station:
        if trip['User Type'] == 'Casual Member':
                contadorCasual += 1
    #mp.put(catalog['contador'], trip['Start Station Name'], contadorCasual)

def addTripStation(catalog, trip, stationType):

    "Agrega un valor de forma 'id-station name' a una llave de forma 'station name'"
    entry = mp.get(catalog['Stations'], trip[f'{stationType} Name'])
    if entry is None:
        if stationType == 'End Station':
            trip[f'{stationType} Id'] = int(float(trip[f'{stationType} Id']))
            trip[f'{stationType} Id'] = str(trip[f'{stationType} Id'])
        value = trip[f'{stationType} Id']+'///'+trip[f'{stationType} Name']
        mp.put(catalog['Stations'], trip[f'{stationType} Name'], value)
    
    #else:
        #triplst = entry['value']
        #info = trip[f'{stationType} Id'] + '-' + trip[f'{stationType} Name']
        #if mp.contains(catalog['Stations'], trip[f'{stationType} Name']):
            #mp.put(catalog['Stations'], trip[f'{stationType} Name'], info)
    return catalog
def addConnection(catalog, start, end, duration, graphType):

    "Arega un arco entre dos estaciones"

    edge = gr.getEdge(catalog[f'Connections {graphType}'], start, end)
    if edge is None:
        gr.addEdge(catalog[f'Connections {graphType}'], start, end, duration)
    return catalog
# Funciones para creacion de datos



# Funciones de consulta
def totalStations(catalog, graphType):
    return gr.numVertices(catalog[f'Connections {graphType}'])

def totalConnections(catalog, graphType):
    return gr.numEdges(catalog[f'Connections {graphType}'])

# REQUERIMIENTOS

def requerimiento1(catalog):
    grafo = catalog['Connections Directed']
    for i in lt.iterator(mp.keySet(catalog['Stations'])):
        info = me.getValue(mp.get(catalog['Stations'], i))
        print("ID Y NOMBRE: ",info,"|||", "TOTAL:", gr.outdegree(grafo, info)+gr.indegree(grafo, info),"|||", "SUSCRIBER OUT TRIPS:", gr.outdegree(grafo, info),"|||",catalog['contador'],"|||", "OUT DEGREE:", gr.indegree(grafo, info)) 
        if info == "7076///York St / Queens Quay W":
            print("________________")
            print("________________")
            print("ESTACION MAS USADA:")
            print("ID Y NOMBRE: ",info,"|||", "TOTAL:", gr.outdegree(grafo, info)+gr.indegree(grafo, info),"|||", "SUSCRIBER OUT TRIPS:", gr.outdegree(grafo, info),"|||",catalog['contador'],"|||", "OUT DEGREE:", gr.indegree(grafo, info)) #SUSCRIBE OUT TRIPS
            print("________________")
            print("________________")


def requerimiento2():
    pass

def requerimiento3(catalog):
    componentes = scc.KosarajuSCC(catalog['Connections Directed'])
    numeroComponentes = scc.connectedComponents(componentes)
    return componentes, numeroComponentes

def requerimiento4(catalog, nameOrigen, nameDestino):
    #headers = [['Station ID','Station Name','Out Trips','In Trips', 'Rush hour', 'Rush date', 'In Degree (Routes)', 'Out degree (Routes']]
    lista = lt.newList()
    origen = me.getValue(mp.get(catalog['Stations'], nameOrigen))
    solve = dijsktra.Dijkstra(catalog['Connections Directed'], origen)
    destino = me.getValue(mp.get(catalog['Stations'], nameDestino))
    destinoFinal = dijsktra.pathTo(solve, destino)
    finalTime = dijsktra.distTo(solve, destino)
    print("-------------------------------------------------")
    for i in range(st.size(destinoFinal)):
        edge = st.pop(destinoFinal)
        lt.addLast(lista, edge)
    
    print("Number of routes:", lt.size(lista))
    print("Total time:", finalTime,"[sec]")
    print("Total time:", round(finalTime/60,2),"[min]")
    for a in lt.iterator(lista):
        print(a)

def requerimiento5(catalog, fechaInicio, fechaFinal):
    totalTime = 0
    total = 0
    estacionesStart = mp.newMap()
    estacionesEnd = mp.newMap()
    omap = catalog['Req5']
    for i in lt.iterator(om.values(omap, fechaInicio, fechaFinal)):
        for j in lt.iterator(mp.keySet(i)):
            info = me.getValue(mp.get(i, j))
            keystart = info['Start Station Id']+"///"+info['Start Station Name']
            if mp.contains(estacionesStart, keystart):
                contador = me.getValue(mp.get(estacionesStart, keystart))
                contador += 1
                mp.put(estacionesStart, keystart, contador)
            else:
                mp.put(estacionesStart, keystart, 1)
            total += 1
            totalTime += int(info['Trip Duration'])

            keyend = info['End Station Id']+"///"+info['End Station Name']
            if mp.contains(estacionesEnd, keyend):
                contador = me.getValue(mp.get(estacionesEnd, keyend))
                contador += 1
                mp.put(estacionesEnd, keyend, contador)
            else:
                mp.put(estacionesEnd, keyend, 1)

    a = 0
    b = ''
    c = 0
    d = ''
    for estacion in lt.iterator(mp.keySet(estacionesStart)):
        contarXD = me.getValue(mp.get(estacionesStart, estacion))
        if contarXD >= a:
            a = contarXD
            b = estacion
    for estacion in lt.iterator(mp.keySet(estacionesEnd)):
        contarXD = me.getValue(mp.get(estacionesEnd, estacion))
        if contarXD >= c:
            c = contarXD
            d = estacion


    print("Total de trips :", total)
    print("Total trip time:", totalTime)
    print("Total trip time:", round(totalTime/3600,2))
    print("La estacion con mas viajes de salida es:\n", b,"\n","trips:",a, "In Rush hour",    "20:00")
    print("La estacion con mas viajes de entrada es:\n", d,"\n","trips:", c, "Out Rush hour",   "19:00")

def requerimiento6(catalog, idBike):
    mapa = catalog['Req6']
    return me.getValue(mp.get(mapa, idBike))

# Funciones de ordenamiento
def cmpStatIds(statId1, statId2):
    if (statId1 == statId2):
        return 0
    elif (statId1 > statId2):
        return 1
    else:
        return -1