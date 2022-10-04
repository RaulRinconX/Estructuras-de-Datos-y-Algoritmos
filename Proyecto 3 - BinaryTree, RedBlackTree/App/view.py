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
from time import process_time
import controller as cnt
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from tabulate import tabulate
from datetime import datetime as dt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Reportar las cinco adquisiciones más recientes de un club (First)")
    print("3- Reportar los jugadores de cierta posición dentro de un rango de desempeño, potencial y salario (Second)")
    print("4- Reportar los jugadores dentro de un rango salarial y con cierta etiqueta (Third)")
    print("5- Reportar los jugadores con cierto rasgo característico y nacidos en un periodo de tiempo (Fourth)")
    print("6- Graficar el histograma de una propiedad para los jugadores FIFA (Fifth) ")
    print("7- Req 6")
    print("0- Salir")
    
catalog = None
file = cf.data_dir+"fifa-players-2022-utf8-large.csv"

"""
Menu principal
"""

# print("\nTiempo:",t1End-t1Start,"segundos\n")
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:                                      # 1 == CARGA DE DATOS
        print("\nCargando información de los archivos ....")
        t1Start = process_time()
        catalog = cnt.newCatalog()
        cnt.loadCatalog(file, catalog)
        t1End = process_time()
        llaves = mp.keySet(catalog["players"])                  
        valores = mp.valueSet(catalog["players"])
        print("\nTiempo de carga:",t1End-t1Start,"segundos\n")   # TIEMPO DE CARGA
        print(f"Total de jugadores es de {lt.size(llaves)}\n")   # TOTAL DE JUGADORESS
        print("\nLos 5 primeros y 5 ultimos jugadores son:\n")
        primerasLlaves = lt.subList(llaves, 1, 5)
        primerosValores = lt.subList(valores, 1, 5)
        ultimosValores = lt.subList(valores, lt.size(valores)-6, 5)
        headers = [['Nombre','Edad','Altura','Peso','Nacionalidad','Overall','Potencia', 'Salario','Liga','Club','Vinculacion']]
        for i in range(1, lt.size(primerasLlaves)+1):
            valor = lt.getElement(primerosValores, i)
            header = valor['short name'], valor["age"], valor["height"], valor["weight"], valor["nacionality"], valor["overall"], valor["potential"], valor["wage"], valor["league"], valor["club"], dt.strftime(valor["asosiation date"], "%Y-%m-%d")
            headers.append(header)
            valorFinal = lt.getElement(ultimosValores, i)
            headerFinal = valorFinal['short name'], valorFinal["age"], valorFinal["height"], valorFinal["weight"], valorFinal["nacionality"], valorFinal["overall"], valorFinal["potential"], valorFinal["wage"], valorFinal["league"], valorFinal["club"], dt.strftime(valorFinal["asosiation date"], "%Y-%m-%d")
            headers.append(headerFinal)
        print(tabulate(headers, headers="firstrow", tablefmt='fancy_grid',stralign='left', numalign='left'))

    elif int(inputs[0]) == 2:                                   # REQUERIMIENTO 1
        jugadores = catalog["players"]
        llaves = mp.keySet(catalog["players"])
        valores = mp.valueSet(catalog["players"])
        club = str(input("Ingrese el club a buscar:"))
        t1Start = process_time()
        idjugadores = cnt.requerimiento1(catalog, club)
        headers = [['Nombre','Edad','Nacimiento','Overall','Nacionalidad','Valor Contrato','Salario', 'Valor Clausula', 'Vinculacion', 'Posiciones', 'Comentarios', 'Tags']]
        print("\nLos cinco jugadores más recientemente vinculados al",club,"son:\n")
        for i in range(1, 6):
            valor = cnt.translator(catalog, lt.getElement(idjugadores, i))
            header = valor['short name'], valor["age"], dt.strftime(valor["d-o-b"], "%Y-%m-%d"), valor["overall"], valor["nacionality"], valor["contract_value"], valor["wage"], "", dt.strftime(valor["asosiation date"], "%Y-%m-%d"), #valor["positions"], valor["comments"], valor["tags"]
            headers.append(header)
        t1End = process_time()
        print("\nTiempo de respuesta:",t1End-t1Start,"segundos\n")
        print(tabulate(headers, headers="firstrow", tablefmt='fancy_grid',stralign='left', numalign='left'))

    elif int(inputs[0]) == 3:                                    # REQUERIMIENTO 2
        posicion = input("Ingrese la posicion a consultar: ")
        minoverall = input("Ingrese el overall minimo: ")
        maxoverall = input("Ingrese el overall maximo: ")
        minpotential = float(input("Ingrese el potential minimo: "))
        maxpotential = float(input("Ingrese el potential maximo: "))
        mineuros = int(input("Ingrese el rango salarial minimo: "))
        maxeuros = int(input("Ingrese el rango salarial maximo: "))
        primeros, ultimos = cnt.requerimiento2(catalog, posicion, maxoverall, minoverall, maxpotential,minpotential, mineuros, maxeuros)
        headers = [['Nombre','Edad','Nacimiento','Overall','Potencial','Nacionalidad','Valor Contrato','Salario', 'Valor Clausula', 'Vinculacion', 'Posiciones', 'Comentarios', 'Tags']]
        for i in range(1, lt.size(primeros)+1):
            x = lt.getElement(primeros,i)
            valor = cnt.translator(catalog, lt.firstElement(x))
            header = valor['short name'], valor["age"], dt.strftime(valor["d-o-b"], "%Y-%m-%d"), valor["overall"], valor["potential"], valor["nacionality"], valor["contract_value"], valor["wage"], "", dt.strftime(valor["asosiation date"], "%Y-%m-%d") #valor["positions"], valor["comments"], valor["tags"]
            headers.append(header)
        for i in range(1, lt.size(ultimos)+1):
            x = lt.getElement(ultimos,i)
            valor = cnt.translator(catalog, lt.firstElement(x))
            header = valor['short name'], valor["age"], dt.strftime(valor["d-o-b"], "%Y-%m-%d"), valor["overall"],  valor["potential"],valor["nacionality"], valor["contract_value"], valor["wage"], "", dt.strftime(valor["asosiation date"], "%Y-%m-%d") #valor["positions"], valor["comments"], valor["tags"]
            headers.append(header)
        print(tabulate(headers, headers="firstrow", tablefmt='fancy_grid',stralign='left', numalign='left'))

    elif int(inputs[0]) == 4:                                  #REQUERIMIENTO 3
        jugadores = catalog["players"]
        llaves = mp.keySet(catalog["players"])
        valores = mp.valueSet(catalog["players"])
        min_wage = int(input('Ingrese el valor inferior del rango de salario: '))
        max_wage = int(input('Ingrese el valor superior del rango de salario: '))
        player_tg = input('Ingrese un tag asociado al jugador: ')
        time_strt = process_time()
        players = cnt.requerimiento3(catalog, min_wage, max_wage, player_tg)
        headers = [['Nombre','Edad','Nacimiento','Nacionalidad','Valor Contrato','Salario', 'Club', 'Liga']] #'Liga', 'Potencial', 'Overall', 'Posiciones', 'Comentarios', 'Tags']]
        print(f"El numero de jugadores con esa caracteristica y rango salarial son: {lt.size(players)}")
        if lt.size(players) >= 6:
            print("\nLos primeros 3 y ultimos 3 jugadores con esa característica y rango salarial son: \n")
            for i in range(1,4):
                valor = lt.getElement(players, i)
                header = valor['long name'], valor["age"], dt.strftime(valor["d-o-b"], "%Y-%m-%d"), valor["nacionality"], valor["contract_value"], valor["wage"], valor['club'], valor['league'], 
                valor['potential'], valor['overall'], valor['positions'], valor["comments"], valor["tags"]
                headers.append(header)
            for i in range(lt.size(players) - 1,lt.size(players) + 1):
                valor = lt.getElement(players, i)
                header = valor['long name'], valor["age"], dt.strftime(valor["d-o-b"], "%Y-%m-%d"), valor["nacionality"], valor["contract_value"], valor["wage"], valor['club'], valor['league'], 
                valor['potential'], valor['overall'], valor['positions'], valor["comments"], valor["tags"]
                headers.append(header)
        else:
            print("\nLos unicos jugadores con esa característica y rango salarial son: \n")
            for i in range(1, lt.size(players) + 1):
                valor = lt.getElement(players, i)
                header = valor['long name'], valor["age"], dt.strftime(valor["d-o-b"], "%Y-%m-%d"), valor["nacionality"], valor["contract_value"], valor["wage"], valor['club'], valor['league'], 
                valor['potential'], valor['overall'], valor['positions'], valor["comments"], valor["tags"]
                headers.append(header)
        time_stop = process_time()
        print(tabulate(headers, headers="firstrow", tablefmt='fancy_grid',stralign='left', numalign='left'))
        print("\nTiempo de respuesta:",time_stop-time_strt,"segundos\n")
        
    elif int(inputs[0]) == 5:                                    # REQUERIMIENTO 4
        traits = input("Ingrese el trait a buscar: ")
        dobmax = input("Ingrese la fecha mas reciente: ")
        dobmin = input("Ingrese la fecha mas antigua: ")
        headers = [['Nombre','Edad','Nacimiento','Overall','Potencial','Nacionalidad','Valor Contrato','Salario', 'Valor Clausula', 'Vinculacion', 'Posiciones', 'Comentarios', 'Tags']]
        total, primeros, ultimos = cnt.requerimiento4(catalog, traits, dobmax, dobmin)
        print("Total de jugadores que cumplen las caracteristicas:", total)
        for i in range(1, lt.size(primeros)+1):
            x = lt.getElement(primeros, i)
            valor = cnt.translator(catalog, lt.firstElement(x))
            header = valor['long name'], valor["age"], dt.strftime(valor["d-o-b"], "%Y-%m-%d"), valor["overall"], valor["potential"], valor["nacionality"], valor["contract_value"], valor["wage"], "", dt.strftime(valor["asosiation date"], "%Y-%m-%d") #valor["positions"], valor["comments"], valor["tags"]
            headers.append(header)
        for i in range(1, lt.size(ultimos)+1):
            x = lt.getElement(ultimos, i)
            valor = cnt.translator(catalog, lt.firstElement(x))
            header = valor['long name'], valor["age"], dt.strftime(valor["d-o-b"], "%Y-%m-%d"), valor["overall"], valor["potential"], valor["nacionality"], valor["contract_value"], valor["wage"], "", dt.strftime(valor["asosiation date"], "%Y-%m-%d") #valor["positions"], valor["comments"], valor["tags"]
            headers.append(header)
        print(tabulate(headers, headers="firstrow", tablefmt='fancy_grid',stralign='left', numalign='left'))

    elif int(inputs[0]) == 6:                                    #REQUERIMIENTO 5
        N = int(input("ingrese numero de segmentos para el histograma (N): "))
        X = int(input("ingrese Numero de niveles para el histograma (X): "))
        propiedad = input("Escoga una propiedad: overall, potential, value_eur, wage_eur, age, height_cm, weight_kg, release_clause_eur: ")
        tstart = process_time()
        cnt.requerimiento5(catalog, N, X, propiedad)
        tEnd = process_time()
        print("\nTiempo de respuesta:",tEnd-tstart,"segundos\n")
        print("En el histograma se usaron ", mp.size(catalog["players"]), "jugadores")
        print("Histograma de", propiedad, "con", N, "segmentos y", X, "jugadores por asterisco" )
        print("NOTA: cada * representa ",X," jugadores\n")

    elif int(inputs[0]) == 7:                                    #REQUERIMIENTO 6
        nombrecorto = input("ingrese el nombre corto: ")
        posicion = input("Ingrese la posicion: ")
        cnt.requerimiento6(catalog, nombrecorto, posicion)
    else:
        sys.exit(0)
sys.exit(0)
