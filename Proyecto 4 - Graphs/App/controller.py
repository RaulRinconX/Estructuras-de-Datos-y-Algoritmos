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
import config as cf
import model
import csv
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import list as lt


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo
def init():
    return model.newCatalog()

# Funciones para la carga de datos
def loadTrips(catalog, tripsfile, graphType):

    tripsfile = cf.data_dir + tripsfile
    input_file = csv.DictReader(open(tripsfile, encoding="utf-8"),
                                delimiter=",")

    for trip in input_file:
            durationExists = (int(float(trip['Trip Duration'])) > 0 and trip['Trip Duration'] != "")
            tripStrtStatIdExists = (trip['Start Station Id'] != None or trip['Start Station Id'] != "")
            tripEndStatIdExists = (trip['End Station Id'] != None or trip['End Station Id'] != "")
            bikeIdExists = (trip['Bike Id'] != None or trip['Bike Id'] != "")
            
            if trip['Start Station Name'] == None or trip['Start Station Name'] == "":
                trip['Start Station Name'] = 'Unknow'
            if trip['End Station Name'] == None or trip['End Station Name'] == "":
                trip['End Station Name'] = 'Unknow'

            keyStart = trip['Start Station Id']+"///"+trip['Start Station Name']
            keyEnd = trip['End Station Id']+"///"+trip['End Station Name']
            diffTripStatIds = keyStart != keyEnd
            if (durationExists) and (diffTripStatIds) and (tripStrtStatIdExists) and (tripEndStatIdExists) and (bikeIdExists):
                 model.newTrip(catalog, keyStart, keyEnd, trip, graphType)
            contadorCasual = 0
            if trip['User Type'] == 'Casual Member':
                contadorCasual += 1
    catalog['contador'] = contadorCasual

    for arco in lt.iterator(mp.keySet(catalog['arcos'])):
        spliter = arco.split('##')
        valor = me.getValue(mp.get(catalog['arcos'], arco))
        model.addConnection(catalog, spliter[0], spliter[1], valor['promedio'], graphType)
        #lastTrip = trip
    #print(catalog['Stations'])
    return catalog

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
def totalStations(catalog, graphType):
    return model.totalStations(catalog, graphType)

def totalConnections(catalog, graphType):
    return model.totalConnections(catalog, graphType)

def req1(catalog):
    return model.requerimiento1(catalog)
def req3(catalog):
    return model.requerimiento3(catalog)

def req4(catalog, nameOrigen, nameDestino):
    return model.requerimiento4(catalog, nameOrigen, nameDestino)

def req5(catalog, fechaInicial, fechaFinal):
    return model.requerimiento5(catalog, fechaInicial, fechaFinal)
def req6(catalog, bikeId):
    return model.requerimiento6(catalog, bikeId)