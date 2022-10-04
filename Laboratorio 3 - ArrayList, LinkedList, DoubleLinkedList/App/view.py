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
 *
 * Contribuciones
 *
 * Dario Correal
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones  y  por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


def newController():
    """
    Se crea una instancia del controlador
    """
    control = controller.newController()
    return control


def printMenu():
    """
    Menu de usuario
    """
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Consultar los Top x libros por promedio")
    print("3- Consultar los libros de un autor")
    print("4- Libros por género")
    print("0- Salir")


def loadData():
    """
    Solicita al controlador que cargue los datos en el modelo
    """
    books, authors, tags, book_tags = controller.loadData(control)
    return books, authors, tags, book_tags


def printAuthorData(author):
    """
    Recorre la lista de libros de un autor, imprimiendo
    la informacin solicitada.
    """
    if author:
        print('Autor encontrado: ' + author['name'])
        print('Promedio: ' + str(author['average_rating']))
        print('Total de libros: ' + str(lt.size(author['books'])))
        for book in lt.iterator(author['books']):
            print('Titulo: ' + book['title'] + '  ISBN: ' + book['isbn'])
    else:
        print('No se encontro el autor')


def printBestBooks(books):
    """
    Imprime los mejores libros solicitados
    """
    size = lt.size(books)
    if size:
        print(' Estos son los mejores libros: ')
        for book in lt.iterator(books):
            print('Titulo: ' + book['title'] + '  ISBN: ' +
                  book['isbn'] + ' Rating: ' + book['average_rating'])
    else:
        print('No se encontraron libros')


# Se crea el controlador asociado a la vista
control = newController()

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        bk, at, tg, bktg = loadData()
        print('Libros cargados: ' + str(bk))
        print('Autores cargados: ' + str(at))
        print('Géneros cargados: ' + str(tg))
        print('Asociación de Géneros a Libros cargados: ' +
              str(bktg))

    elif int(inputs[0]) == 2:
        number = input("Buscando los TOP ?: ")
        books = controller.getBestBooks(control, int(number))
        printBestBooks(books)

    elif int(inputs[0]) == 3:
        authorname = input("Nombre del autor a buscar: ")
        author = controller.getBooksByAuthor(control, authorname)
        printAuthorData(author)

    elif int(inputs[0]) == 4:
        label = input("Etiqueta a buscar: ")
        book_count = controller.countBooksByTag(control, label)
        print('Se encontraron: ', book_count, ' Libros')

    elif int(inputs[0]) == 0:
        sys.exit(0)

    else:
        continue
sys.exit(0)
