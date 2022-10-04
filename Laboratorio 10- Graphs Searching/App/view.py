"""
 * Copyright 2020, Departamento de sistemas y Computación
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
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal uwu
 *
 """


import sys
import config
import threading
from App import controller
from DISClib.ADT import stack
assert config

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Variables
# ___________________________________________________


servicefile = 'bus_routes_14000.csv'
initialStation = None
searchMethod = None

# ___________________________________________________
#  Menu principal
# ___________________________________________________


def printMenu():
    print("\n")
    print("*******************************************")
    # TODO Lab 11, asegurarse de completar las opciones 4, 9 y 10
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de buses de singapur")
    print("3- Calcular componentes conectados")
    print("4- Establecer estación base:")
    print("5- Establecer metodo de busqueda y estación base:")
    print("6- Hay camino entre estacion base y estación: ")
    print("7- Ruta de costo mínimo desde la estación base y estación: ")
    print("8- Estación que sirve a mas rutas: ")
    print("9- Existe un camino de busqueda entre base y estación: ")
    print("10- Ruta de busqueda entre la estación base y estación: ")
    print("0- Salir")
    print("*******************************************")


def optionTwo(cont):
    print("\nCargando información de transporte de singapur ....")
    controller.loadServices(cont, servicefile)
    numedges = controller.totalConnections(cont)
    numvertex = controller.totalStops(cont)
    print('Numero de vertices: ' + str(numvertex))
    print('Numero de arcos: ' + str(numedges))
    print('El limite de recursion actual: ' + str(sys.getrecursionlimit()))


def optionThree(cont):
    print('El número de componentes conectados es: ' +
          str(controller.connectedComponents(cont)))


def optionFour(cont, initialStation):
    print('Calculando costo de caminos')
    controller.minimumCostPaths(cont, initialStation)
    print("FIN!")


def optionFive(cont, initialStation, searchMethod):
    # TODO Lab 11, conectar con la funcion del controller searchPaths
    controller.searchPaths(cont, initialStation, searchMethod)


def optionSix(cont, destStation):
    haspath = controller.hasPath(cont, destStation)
    print('Hay camino entre la estación base : ' +
          'y la estación: ' + destStation + ': ')
    print(haspath)


def optionSeven(cont, destStation):
    path = controller.minimumCostPath(cont, destStation)
    if path is not None:
        pathlen = stack.size(path)
        print('El camino es de longitud: ' + str(pathlen))
        while (not stack.isEmpty(path)):
            stop = stack.pop(path)
            print(stop)
    else:
        print('No hay camino')


def optionEight(cont):
    maxvert, maxdeg = controller.servedRoutes(cont)
    print('Estación: ' + maxvert + '  Total rutas servidas: '
          + str(maxdeg))


def optionNine(cont, destStation, searchMethod):
    # TODO Lab 11, conectar con la funcion del controller hasSearchPath
    haspath = None
    haspath = controller.hasSearchPath(cont, destStation, searchMethod)
    print(haspath)


def optionTen(cont, destStation, searchMethod):
    # TODO Lab 11, conectar con la funcion del controller searchPath
    path = None
    path = controller.searchPathTo(cont, destStation, searchMethod)
    if path is not None:
        pathlen = stack.size(path)
        print("La longitud es: " + str(pathlen))
        i = 0
        while i < pathlen:
            x = stack.pop(path)
            print(x)
            i += 1
    else:
        print('No hay camino')


"""
Menu principal
"""


def thread_cycle():
    while True:
        printMenu()
        inputs = input('Seleccione una opción para continuar\n>')

        if int(inputs) == 1:
            print("\nInicializando....")
            # cont es el controlador que se usará de acá en adelante
            cont = controller.init()

        elif int(inputs) == 2:
            optionTwo(cont)

        elif int(inputs) == 3:
            optionThree(cont)

        elif int(inputs) == 4:
            msg = "Estación Base: BusStopCode-ServiceNo (Ej: 75009-10): "
            initialStation = input(msg)
            optionFour(cont, initialStation)

        elif int(inputs) == 5:
            # TODO Lab 11, completar inputs opt 5, searchMethod, initialStation
            estacioninicial = input("Ingrese la estación base para la busqueda (Ej: 75009-10): ")
            print("Seleccione el método de busqueda ""dfs"" o ""bfs"": ")
            metodo = input("Ingrese la opción: ")
            optionFive(cont, estacioninicial, metodo)

        elif int(inputs) == 6:
            destStation = input("Estación destino (Ej: 15151-10): ")
            optionSix(cont, destStation)

        elif int(inputs) == 7:
            destStation = input("Estación destino (Ej: 15151-10): ")
            optionSeven(cont, destStation)

        elif int(inputs) == 8:
            optionEight(cont)

        elif int(inputs) == 9:
            # TODO Lab 11, completar inputs opt 9, destStation
            estaciondestino = input("Ingrese la estación base para la busqueda (Ej: 15151-10): ")
            print("Seleccione el método de busqueda ""dfs"" o ""bfs"": ")
            metodo = str(input("Ingrese la opción: "))
            optionNine(cont, estaciondestino, metodo)

        elif int(inputs) == 10:
            # TODO Lab 11, completar inputs opt 10, destStation
            estaciondestino = input("Ingrese la estación base para la busqueda (Ej: 15151-10): ")
            print("Seleccione el método de busqueda 'dfs' o 'bfs': ")
            metodo = str(input("Ingrese la opción: "))
            optionTen(cont, estaciondestino, metodo)

        else:
            sys.exit(0)
    sys.exit(0)


if __name__ == "__main__":
    threading.stack_size(67108864)  # 64MB stack
    sys.setrecursionlimit(2 ** 20)
    thread = threading.Thread(target=thread_cycle)
    thread.start()
