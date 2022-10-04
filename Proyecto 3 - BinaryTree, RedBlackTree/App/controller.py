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

from time import strptime
import config as cf
import model as mdl
from DISClib.ADT import map as mp
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""
#-------------
#	Iniciar catalogo
#-------------
def newCatalog():
	catalog = mdl.newCatalog()
	return catalog

#-------------
# Cargar catalogo
#-------------
def loadCatalog(dataFile, catalog, e = "utf-8-sig"):
  with open(dataFile,encoding=e) as playersF:
    buffer = csv.DictReader(playersF)
    for player in buffer:
      mdl.addData(catalog, player)
  #mdl.buildReq6(catalog)               #REQ6???????
def translator(catalog, id):
  return mdl.translator(catalog, id)
def requerimiento1(catalog, club):
  return mdl.requerimiento1(catalog, club)
def requerimiento2(catalog, posicion, maxoverall, minoverall, maxpotential,minpotential, mineuros, maxeuros):
  return mdl.requerimiento2(catalog, posicion, maxoverall, minoverall, maxpotential,minpotential, mineuros, maxeuros)
def requerimiento3(catalog, min_wage, max_wage, player_tags):
  return mdl.requerimiento3(catalog, min_wage, max_wage, player_tags)
def requerimiento4(catalog, traits, dobmax, dobmin):
  return mdl.requerimiento4(catalog, traits, dobmax, dobmin)
def requerimiento5(catalog, N, X, propiedad):
  return mdl.requerimiento5(catalog, N, X, propiedad)
def requerimiento6(catalog, nombrecorto, posicion):
  return mdl.requerimiento6(catalog, nombrecorto, posicion)

