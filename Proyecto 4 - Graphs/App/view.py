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

import config as cf
import sys
sys.setrecursionlimit(200000)
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import orderedmap as om
from DISClib.Algorithms.Sorting import selectionsort as sl
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

tripsfile = "Bikeshare-ridership-2021-utf8-small.csv"

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Comprar bicicletas para las estaciones con más viajes de origen")
    print("3- Planear paseos turísticos por la ciudad")
    print("4- Reconocer los componentes fuertemente conectados del sistema")
    print("5- Planear una ruta rápida para el usuario")
    print("6- Reportar rutas en un rango de fechas para los usuarios anuales")
    print("7- Planear el mantenimiento preventivo de bicicletas")
    print("0- Salir")

#catalog = None
def compare(t1,t2):
    if (t1 == t2):
        return 0
    elif (t1 < t2):
        return -1
    else:
        return 1
"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        cont = controller.init()
        print("Cargando información de los archivos ....")
        graphType = input('Elige el tipo de grafo a cargar (dirigido/no dirigido): ')
        if graphType == 'dirigido':
            graphType = 'Directed'
        elif graphType == 'no dirigido':
            graphType = 'NotDirected'
        catalog = controller.loadTrips(cont, tripsfile, graphType)
        numEdges = controller.totalConnections(cont, graphType)
        numVertex = controller.totalStations(cont, graphType)
        print('Numero de vertices: ' + str(numVertex))
        print('Numero de arcos: ' + str(numEdges))

    elif int(inputs[0]) == 2:
        controller.req1(catalog)

    elif int(inputs[0]) == 3:
        pass

    elif int(inputs[0]) == 4:
        mapa = mp.newMap()
        ordenados = om.newMap('RBT')
        componentes, numeroComponentes = controller.req3(catalog)
        print("Hay en total",numeroComponentes,"componentes fuertemente conectados (SCC) en el sistema/grafo")

        for i in lt.iterator(mp.keySet(componentes['idscc'])):
            info = me.getValue(mp.get(componentes["idscc"], i))
            if mp.contains(mapa, info):
                value = me.getValue(mp.get(mapa, info))
                value += 1
            else:
                value = 1
            mp.put(mapa, info, value)
        for x in lt.iterator(mp.keySet(mapa)):
            jaja = me.getValue(mp.get(mapa, x))
            om.put(ordenados, x, jaja)
            print("Componente:",x, "Numero de estaciones:", jaja)


    elif int(inputs[0]) == 5:
        nameOrigen, nameDestino = input("Ingrese el origen: "), input("Ingrese el destino: ")
        controller.req4(catalog, nameOrigen, nameDestino)

    elif int(inputs[0]) == 6:
        fechaInicial = input("Ingrese la fecha inicial: ")
        fechaFinal = input("Ingrese la fecha final: ")
        controller.req5(catalog, fechaInicial, fechaFinal)
    elif int(inputs[0]) == 7:                                   #ARREGLAR EL VIEW UWU
        bikeId = input("Ingrese el ID de la bicicleta: ")
        estacionesStart = mp.newMap()
        estacionesEnd = mp.newMap()
        contador = 0
        totalHoras = 0
        req6 = controller.req6(catalog, bikeId)
        for i in lt.iterator(mp.keySet(req6)):
            info = me.getValue(mp.get(req6, i))
            totalHoras += int(info['Trip Duration'])
            contador += 1

            keystart = info['Start Station Id']+"///"+info['Start Station Name']
            if mp.contains(estacionesStart, keystart):
                contador = me.getValue(mp.get(estacionesStart, keystart))
                contador += 1
                mp.put(estacionesStart, keystart, contador)
            else:
                mp.put(estacionesStart, keystart, 1)

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

    
        print("Total de viajes con la bicicleta de ID",bikeId, "son:", contador)
        print("El total de horas de utilización de la bicicleta:", round(totalHoras/3600,2))
        print("La estacion con mas viajes de salida es:\n", b,"\n","trips:",a)
        print("La estacion con mas viajes de entrada es:\n", d,"\n","trips:", c)
    else:
        sys.exit(0)
sys.exit(0)
