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

from __future__ import division
import sys
default_limit = 1000
sys.setrecursionlimit(default_limit*10)
from gettext import Catalog
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from datetime import datetime as dt
from tabulate import tabulate
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

def newCatalog():
  catalog = {
  "players":None,
  "translatorShort":None,
  "translatorLong":None,
  "filled":None,
  }
  catalog["players"]=mp.newMap()#Map<Id, Player>
  catalog["translatorShort"]=mp.newMap()#Map<Player.shortname,Id>
  catalog["translatorLong"]=mp.newMap()#Map<Player.fullname, Id>
  catalog["filled"]=newReqs()
  return catalog

def newPlayer():
  player = {
  "short name":"",
  "long name":"",
  "age":0,
  "height":0,
  "weight":0,
  "d-o-b":None,
  "nacionality":"",
  "contract_value":0,
  "release_clause_eur":0,
  "wage":0,
  "club":"",
  "asosiation date":None,
  "league":"",
  "potential":0.0,
  "overall":0,
  "positions":lt.newList(),
  "reputation":0.0,
  "tags":lt.newList(),
  "comments":"",
  "req6a":mp.newMap()
  }
  return player

def newReqs():
  reqs = {
  "req1":mp.newMap(),#Map<Club, List<Player>>
  "req2":mp.newMap(),#Map<Position, BST<Players(overall)>
  "req3":mp.newMap(),#Map<Tag,BST<Players(wage)>
  "req4":mp.newMap(),#Map<Trait, BST<Players(Date Of Birth)>>
  "req5":mp.newMap(),#Map<Propiety, Map<Player, Value>>
  "norm":mp.newMap(),#Map<Propiety, (float('inf'), float('-inf'))
  "req6b":mp.newMap()#Map<Position, List<Player>>
  }
  return reqs

def addData(catalog,playerData):
  #Build translators
  buildTranslator(catalog, playerData)
  
  #Build req1
  buildReq1(catalog, playerData)
  
  #Build req2
  buildReq2(catalog, playerData)
  
  #Build req3
  buildReq3(catalog, playerData)
  
  #Build req4
  buildReq4(catalog, playerData)

  #Build req5
  
  buildReq5(catalog, playerData)
  #Build player
  buildPlayer(catalog, playerData)



def buildTranslator(catalog, playerData):
  mp.put(catalog["translatorShort"], playerData["short_name"], playerData["sofifa_id"])
  mp.put(catalog["translatorLong"], playerData["long_name"], playerData["sofifa_id"])

def buildReq1(catalog, playerData):
  players = me.getValue(mp.get(catalog["filled"]["req1"], playerData["club_name"])) if mp.contains(catalog["filled"]["req1"], playerData["club_name"]) else lt.newList(cmpfunction=clubJoined)
  
  playerInfo1 = lt.newList()
  lt.addLast(playerInfo1, playerData["sofifa_id"])
  lt.addLast(playerInfo1, dt.strptime(playerData["club_joined"], "%Y-%m-%d"))
  
  lt.addLast(players, playerInfo1)
  mp.put(catalog["filled"]["req1"], playerData["club_name"], players)

def buildReq2(catalog, playerData):
  positionsData = playerData["player_positions"].split(",")
  for pos in positionsData:
    positions = me.getValue(mp.get(catalog["filled"]["req2"], pos)) if mp.contains(catalog["filled"]["req2"], pos) else om.newMap("BST", overall) #First level
    
    playerInfo2 = lt.newList()
    lt.addLast(playerInfo2, playerData["sofifa_id"])
    lt.addLast(playerInfo2, float(playerData["potential"]))
    lt.addLast(playerInfo2, float(playerData["wage_eur"]))
    
    om.put(positions, playerData["overall"], playerInfo2)
    mp.put(catalog["filled"]["req2"], pos, positions)

def buildReq3(catalog, playerData):
  tagsData = playerData["player_tags"].replace("#","").split(",")
  for tag in tagsData:
    tags = me.getValue(mp.get(catalog["filled"]["req3"], tag)) if mp.contains(catalog["filled"]["req3"], tag) else om.newMap("BST", wage_eur)
    
    om.put(tags, playerData["wage_eur"], playerData["sofifa_id"])
    mp.put(catalog["filled"]["req3"], tag, tags)

def buildReq4(catalog, playerData):
  traitsData = playerData["player_traits"].split(",")
  for trait in traitsData:
    traits = me.getValue(mp.get(catalog["filled"]["req4"], trait)) if mp.contains(catalog["filled"]["req4"], trait) else om.newMap("BST", dob)
   
    playerInfo2 = lt.newList()
    lt.addLast(playerInfo2, playerData["sofifa_id"])
    lt.addLast(playerInfo2, float(playerData["potential"]))
    lt.addLast(playerInfo2, float(playerData["overall"]))

    om.put(traits, playerData["dob"], playerInfo2)   
    mp.put(catalog["filled"]["req4"], trait, traits)

def buildReq5(catalog, playerData):
  extracted(catalog, playerData, "overall")
  extracted(catalog, playerData, "potential")
  extracted(catalog, playerData, "value_eur")
  extracted(catalog, playerData, "wage_eur")
  extracted(catalog, playerData, "age")
  extracted(catalog, playerData, "height_cm")
  extracted(catalog, playerData, "weight_kg")
  extracted(catalog, playerData, "release_clause_eur")

def extracted(catalog, playerData, key):
  compare = None
  if key == "overall" or "age" or "height_cm" or "weight_kg":
    compare = overall
  elif key == "potential":
    compare = potential
  elif key == "wage_eur" or "value_eur" or "release_clause_eur":
    compare = wage_eur
  if playerData[key] == '':
    playerData[key] = 0.0
  if (not mp.contains(catalog["filled"]["req5"], key)):
    mp.put(catalog["filled"]["req5"], key, om.newMap("RBT", compare))
  pair = me.getValue(mp.get(catalog["filled"]["req5"], key))
  if om.contains(pair, playerData[key]):
    pareja = om.get(pair,  playerData[key])
    lista = me.getValue(pareja)
    lt.addLast(lista, playerData)
  else:
    nueva = lt.newList()
    lt.addLast(nueva, playerData)
    om.put(pair, playerData[key], nueva)

def buildReq6(catalog):
  allIds = mp.keySet(catalog["players"])
  for i in range(1, lt.size(allIds)+1):
    playerId = lt.getElement(allIds, i)
    playerData = me.getValue(mp.get(catalog["players"], playerId))
    
    
    potMin, potMax = me.getValue(mp.get(catalog["filled"]["norm"], "potential")) if mp.contains(catalog["filled"]["norm"], "potential") else (float('inf'), float('-inf'))
    vrP = (playerData["potential"] - potMin)/(potMax-potMin)
    
    heiMin, heiMax = me.getValue(mp.get(catalog["filled"]["norm"], "height")) if mp.contains(catalog["filled"]["norm"], "height") else (float('inf'), float('-inf'))
    vrH = (playerData["height"] - heiMin)/(heiMax-heiMin)
    
    ageMin, ageMax = me.getValue(mp.get(catalog["filled"]["norm"], "age")) if mp.contains(catalog["filled"]["norm"], "age") else (float('inf'), float('-inf'))
    vrA = (playerData["age"] - ageMin)/(ageMax-ageMin)
    
    valMin, valMax = me.getValue(mp.get(catalog["filled"]["norm"], "value")) if mp.contains(catalog["filled"]["norm"], "value") else (float('inf'), float('-inf'))
    vrV = (playerData["contract_value"] - valMin)/(valMax-valMin)


def buildPlayer(catalog, playerData):
  player = newPlayer()
  
  player["short name"] = playerData["short_name"]
  player["long name"] = playerData["long_name"]
  player["comments"] = playerData["player_traits"]
  
  player["age"] = float(playerData["age"])
  player["height"] = float(playerData["height_cm"])
  player["weight"] = float(playerData["weight_kg"])
  
  if playerData["value_eur"] == '':
    playerData["value_eur"] = 0.0
    player["contract_value"] = playerData["value_eur"]
  else:
    player["contract_value"] = float(playerData["value_eur"])

  if playerData["release_clause_eur"] == '':
    playerData["release_clause_eur"] = 0
    player["release_clause_eur"] = playerData["release_clause_eur"]
  else:
    player["release_clause_eur"] = playerData["release_clause_eur"]
  

  player["wage"] = float(playerData["wage_eur"])
  player["reputation"] = float(playerData["international_reputation"])
  
  player["potential"] = float(playerData["potential"])
  
  player["overall"] = float(playerData["overall"])
  
  player["league"] = playerData["league_name"]
  player["club"] = playerData["club_name"]
  player["asosiation date"] = dt.strptime(playerData["club_joined"], "%Y-%m-%d")
  
  player["d-o-b"] = dt.strptime(playerData["dob"],"%Y-%m-%d")
  player["nacionality"] = playerData["nationality_name"]
  
  it = playerData["player_positions"].split(",")
  for pos in it:
    lt.addLast(player["positions"], pos)
    posList = me.getValue(mp.get(catalog["filled"]["req6b"], pos)) if mp.contains(catalog["filled"]["norm"], pos) else lt.newList()
    lt.addLast(posList, playerData["sofifa_id"])
    mp.put(catalog["filled"]["req6b"], pos, posList)
  normalizator(catalog, player["potential"], player["age"], player["height"], player["contract_value"])
  
  it = playerData["player_tags"].split(",")
  for tag in it:
    lt.addLast(player["tags"], tag)
  
  mp.put(catalog["players"], playerData["sofifa_id"], player)


def normalizator(catalog, pPot, pAge, pHei, pVal):
  minPot, maxPot = me.getValue(mp.get(catalog["filled"]["norm"], "potential")) if mp.contains(catalog["filled"]["norm"], "potential") else (float('inf'), float('-inf'))
  minPot, maxPot = min(minPot, pPot), max(maxPot, pPot)
  
  minAge, maxAge = me.getValue(mp.get(catalog["filled"]["norm"], "age")) if mp.contains(catalog["filled"]["norm"], "age") else (float('inf'), float('-inf'))
  minAge, maxAge = min(minAge, pAge), max(maxAge, pAge)
  
  minHei, maxHei = me.getValue(mp.get(catalog["filled"]["norm"], "height")) if mp.contains(catalog["filled"]["norm"], "height") else (float('inf'), float('-inf'))
  minHei, maxHei = min(minHei, pHei), max(maxHei, pHei)
  
  minVal, maxVal = me.getValue(mp.get(catalog["filled"]["norm"], "value")) if mp.contains(catalog["filled"]["norm"], "value") else (float('inf'), float('-inf'))
  minVal, maxVal = min(minVal, pVal), max(maxVal, pVal)
  
  mp.put(catalog["filled"]["norm"], "potential", (minPot, maxPot))
  mp.put(catalog["filled"]["norm"], "age", (minAge, maxAge))
  mp.put(catalog["filled"]["norm"], "height", (minHei, maxHei))
  mp.put(catalog["filled"]["norm"], "value", (minVal, maxVal))


def translator(catalog, id):
  return me.getValue(mp.get(catalog["players"], id)) if mp.contains(catalog["players"], id) else None

def overall(oa1, oa2):
  oa1 = float(oa1) if type(oa1) == str and oa1!="" else -1
  oa2 = float(oa2) if type(oa2) == str and oa2!="" else -1
  return 0 if (oa1 == oa2) else (1 if (oa1 > oa2) else -1) 

def potential(pot1, pot2):
  return 0 if (pot1 == pot2) else (1 if (pot1 > pot2) else -1)

def wage_eur(weur1, weur2):
  return 0 if (int(float(weur1)) == int(float(weur2))) else (1 if (int(float(weur1)) > int(float(weur2))) else -1)

def cmpReq3(player1, player2):
  if (int(float(player1['wage'])) == int(float(player2['wage']))):
    if float(player1['overall']) == float(player2['overall']):
      if float(player1['potential']) == float(player2['potential']):
        if player1['long name'] > player2['long name']:
          return 1
        else:
          return -1
      elif float(player1['potential']) > float(player2['potential']):
        return 1
      else:
        return -1
    elif float(player1['overall']) > float(player2['overall']):
      return 1
    else:
      return -1
  elif (int(float(player1['wage'])) > int(float(player2['wage']))):
    return 1
  else:
    return -1

def dob(dob1, dob2):
  return 0 if (dob1 == dob2) else (1 if (dob1 > dob2) else -1)

def clubJoined(player1, player2):
  doj1 = lt.getElement(player1, 2)
  doj2 = lt.getElement(player2, 2)
  return 0 if (doj1 == doj2) else (1 if (doj1 > doj2) else -1)

def requerimiento1(catalog, club):
  mapa = catalog["filled"]["req1"]
  idjugador = lt.newList("ARRAY_LIST")
  llaves = mp.keySet(mapa)
  for i in range(1, lt.size(llaves)+1):
    clubes = lt.getElement(llaves, i)
    if clubes == club:
      equipos = mp.get(mapa, clubes)
      jugadores = me.getValue(equipos)
  for i in range(1, lt.size(jugadores)+1):
    x = lt.getElement(jugadores, i)
    jugador = lt.firstElement(x)
    lt.addLast(idjugador, jugador)
  return idjugador

def requerimiento2(catalog, posicion, maxoverall, minoverall, maxpotential,minpotential, mineuros, maxeuros):
  finalfiltred = lt.newList('ARRAY_LIST')
  mapa = catalog["filled"]["req2"]
  pos = mp.get(mapa, posicion)
  tree = me.getValue(pos)
  filtrado = om.values(tree, minoverall, maxoverall)
  for i in range(1, lt.size(filtrado)+1):
    jugador = lt.getElement(filtrado, i)
    if minpotential <= lt.getElement(jugador, 2) <= maxpotential and mineuros <= lt.getElement(jugador, 3) <= maxeuros:
          lt.addLast(finalfiltred, jugador)
  primeros = lt.subList(finalfiltred, 1, 3)
  ultimos = lt.subList(finalfiltred, (lt.size(finalfiltred)-2), 3)
  return primeros, ultimos

def requerimiento3(catalog, min_wage, max_wage, player_tags):
  mapa = catalog['filled']['req3']
  player_ids = lt.newList('ARRAY_LIST')
  players = lt.newList('ARRAY_LIST')
  keys = mp.keySet(mapa)
  for i in range(1, lt.size(keys) + 1):
    player_tgs = lt.getElement(keys, i)
    player_wage_tree = me.getValue(mp.get(mapa, player_tgs))
    wage_list = sa.sort(om.keys(player_wage_tree, min_wage, max_wage), wage_eur)
    for j in range(1, lt.size(wage_list) + 1):
      player_wage = lt.getElement(wage_list, j)
      if (player_tgs.strip() == player_tags.strip()) and (int(float(player_wage)) >= min_wage) and (int(float(player_wage)) <= max_wage):
        player_id = me.getValue(mp.get(player_wage_tree, player_wage))
        lt.addLast(player_ids, player_id)
  for i in range(1, lt.size(player_ids) + 1):
    player = translator(catalog, lt.getElement(player_ids, i))
    lt.addLast(players, player)
  players = sa.sort(players, cmpReq3)
  return players

def sorter(lista1, lista2):
  return 0 if ( lt.getElement(lista1, 2) == lt.getElement(lista2, 2)) else (1 if (lt.getElement(lista1, 2) > lt.getElement(lista2, 2)) else -1)

def requerimiento4(catalog, traits, dobmax, dobmin):
  finalfiltred = lt.newList('ARRAY_LIST')
  mapa = catalog["filled"]["req4"]
  tag = mp.get(mapa, traits)
  tree = me.getValue(tag)
  jugadores = om.values(tree, dobmin, dobmax)
  for i in range(lt.size(jugadores)+1):
    jugador = lt.getElement(jugadores, i)
    lt.addLast(finalfiltred, jugador)
  ordenadojaja = sa.sort(finalfiltred, sorter)
  primeros = lt.subList(ordenadojaja, 1, 3)
  ultimos = lt.subList(ordenadojaja, lt.size(ordenadojaja)-2, 3)
  return lt.size(ordenadojaja), primeros, ultimos

def requerimiento5(catalog, N, X, propiedad):
  mapa = catalog["filled"]["req5"]
  headers = [['bin','count','lvl','mark']]
  jugadores = me.getValue(mp.get(mapa, propiedad)) #LLAVE: PROPIEDAD(overall, potential, etc...)VALUE: JUGADORES  #MAPA KEY: IDPLAYER VALUE: valor de la propiedad
  minkey = int(float(om.minKey(jugadores)))
  maxkey = int(float(om.maxKey(jugadores)))
  resta = maxkey - minkey
  divishion = resta/N        
  i = 0
  while i < N:
    cont = 0
    x = minkey
    minkey = x + divishion    
    rangos = om.values(jugadores, str(x), str(minkey))
    for a in range(1, lt.size(rangos)+1):
      lol = lt.size(lt.getElement(rangos, a))
      cont += lol
    escala = cont//X
    header = (round(x, 3), round(minkey, 3)), cont, escala, "*"*escala
    headers.append(header)
    i += 1
  print(tabulate(headers, headers="firstrow", tablefmt='fancy_grid',stralign='left', numalign='left'))

def requerimiento6(catalog, nombrecorto, posicion):
  mapa = catalog["filled"]["req6b"]
  valores = mp.valueSet(mapa)
  for i in range(1, mp.size(mapa)+1):
    print(lt.getElement(valores, i))
  """
  potencial, edad, altura, posición de juego (player_positions) y costo
  """
  print(mp.get(mapa,posicion))