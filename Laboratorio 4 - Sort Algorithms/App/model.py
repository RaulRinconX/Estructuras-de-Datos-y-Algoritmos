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


import config as cf
import time
from DISClib.ADT import list as lt
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf

"""
Se define la estructura de un catálogo de libros.
El catálogo tendrá tres listas, una para libros, otra para autores
y otra para géneros
"""

# Construccion de modelos


def newCatalog():
    """
    Inicializa el catálogo de libros. Crea una lista vacia para guardar
    todos los libros, adicionalmente, crea una lista vacia para los autores,
    una lista vacia para los generos y una lista vacia para la asociación
    generos y libros. Retorna el catalogo inicializado.
    """
    catalog = {'books': None,
               'authors': None,
               'tags': None,
               'book_tags': None}

    catalog['books'] = lt.newList('ARRAY_LIST')
    catalog['authors'] = lt.newList('SINGLE_LINKED',
                                    cmpfunction=compareauthors)
    catalog['tags'] = lt.newList('SINGLE_LINKED',
                                 cmpfunction=comparetagnames)
    catalog['book_tags'] = lt.newList('ARRAY_LIST')

    return catalog


# Funciones para agregar informacion al catalogo

def addBook(catalog, book):
    # Se adiciona el libro a la lista de libros
    lt.addLast(catalog['books'], book)
    # Se obtienen los autores del libro
    authors = book['authors'].split(",")
    # Cada autor, se crea en la lista de libros del catalogo, y se
    # crea un libro en la lista de dicho autor (apuntador al libro)
    for author in authors:
        addBookAuthor(catalog, author.strip(), book)
    return catalog


def addBookAuthor(catalog, authorname, book):
    """
    Adiciona un autor a lista de autores, la cual guarda referencias
    a los libros de dicho autor
    """
    authors = catalog['authors']
    posauthor = lt.isPresent(authors, authorname)
    if posauthor > 0:
        author = lt.getElement(authors, posauthor)
    else:
        author = newAuthor(authorname)
        lt.addLast(authors, author)
    lt.addLast(author['books'], book)
    return catalog


def addTag(catalog, tag):
    """
    Adiciona un tag a la lista de tags
    """
    t = newTag(tag['tag_name'], tag['tag_id'])
    lt.addLast(catalog['tags'], t)
    return catalog


def addBookTag(catalog, booktag):
    """
    Adiciona un tag a la lista de tags
    """
    t = newBookTag(booktag['tag_id'], booktag['goodreads_book_id'])
    lt.addLast(catalog['book_tags'], t)
    return catalog


# Funciones para creacion de datos

def newAuthor(name):
    """
    Crea una nueva estructura para modelar los libros de
    un autor y su promedio de ratings
    """
    author = {'name': "", "books": None,  "average_rating": 0}
    author['name'] = name
    author['books'] = lt.newList('ARRAY_LIST')
    return author


def newTag(name, id):
    """
    Esta estructura almancena los tags utilizados para marcar libros.
    """
    tag = {'name': '', 'tag_id': ''}
    tag['name'] = name
    tag['tag_id'] = id
    return tag


def newBookTag(tag_id, book_id):
    """
    Esta estructura crea una relación entre un tag y
    los libros que han sido marcados con dicho tag.
    """
    booktag = {'tag_id': tag_id, 'book_id': book_id}
    return booktag


# Funciones de consulta

def getBooksByAuthor(catalog, authorname):
    """
    Retorna un autor con sus libros a partir del nombre del autor
    """
    posauthor = lt.isPresent(catalog['authors'], authorname)
    if posauthor > 0:
        author = lt.getElement(catalog['authors'], posauthor)
        return author
    return None


def getBestBooks(catalog, number):
    """
    Retorna los mejores libros
    """
    books = catalog['books']
    bestbooks = lt.newList()
    for cont in range(1, number+1):
        book = lt.getElement(books, cont)
        lt.addLast(bestbooks, book)
    return bestbooks


def countBooksByTag(catalog, tag):
    """
    Retorna los libros que fueron etiquetados con el tag
    """
    tags = catalog['tags']
    bookcount = 0
    pos = lt.isPresent(tags, tag)
    if pos > 0:
        tag_element = lt.getElement(tags, pos)
        if tag_element is not None:
            for book_tag in lt.iterator(catalog['book_tags']):
                if tag_element['tag_id'] == book_tag['tag_id']:
                    bookcount += 1
    return bookcount


def bookSize(catalog):
    return lt.size(catalog['books'])


def authorSize(catalog):
    return lt.size(catalog['authors'])


def tagSize(catalog):
    return lt.size(catalog['tags'])


def bookTagSize(catalog):
    return lt.size(catalog['book_tags'])


# Funciones utilizadas para comparar elementos dentro de una lista

def compareauthors(authorname1, author):
    if authorname1.lower() == author['name'].lower():
        return 0
    elif authorname1.lower() > author['name'].lower():
        return 1
    return -1


def comparetagnames(name, tag):
    if (name == tag['name']):
        return 0
    elif (name > tag['name']):
        return 1
    return -1


# funciones para comparar elementos dentro de algoritmos de ordenamientos

def compareratings(book1, book2):
    # TODO modificar operador de comparacion lab 4
    return (float(book1['average_rating']) < float(book2['average_rating']))


# Funciones de ordenamiento

def sortBooks(catalog, size):
    # TODO completar los cambios del return en el sort para el lab 4
    sub_list = lt.subList(catalog['books'], 1, size)
    start_time = getTime()
    sorted_list = sa.sort(sub_list, compareratings)
    end_time = getTime()
    delta_time = deltaTime(start_time, end_time)
    return sorted_list, delta_time


# Funciones para medir tiempos de ejecucion

def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def deltaTime(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed
