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
 * Contribuciones
 *
 * Dario Correal
 """

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


# Inicialización del controller

def newController():
    """
    Crea una instancia del modelo
    """
    control = {
        'model': None
    }
    control['model'] = model.newCatalog()
    return control


# Funciones para la carga de datos


def loadData(control):
    """
    Carga los datos de los archivos y cargar los datos en la
    estructura de datos
    """
    catalog = control['model']
    books, authors = loadBooks(catalog)
    tags = loadTags(catalog)
    booktags = loadBooksTags(catalog)
    return books, authors, tags, booktags


def loadBooks(catalog):
    """
    Carga los libros del archivo.  Por cada libro se toman sus autores y por
    cada uno de ellos, se crea en la lista de autores, a dicho autor y una
    referencia al libro que se esta procesando.
    """
    booksfile = cf.data_dir + 'GoodReads/books.csv'
    input_file = csv.DictReader(open(booksfile, encoding='utf-8'))
    for book in input_file:
        model.addBook(catalog, book)
    return model.bookSize(catalog), model.authorSize(catalog)


def loadTags(catalog):
    """
    Carga todos los tags del archivo y los agrega a la lista de tags
    """
    tagsfile = cf.data_dir + 'GoodReads/tags.csv'
    input_file = csv.DictReader(open(tagsfile, encoding='utf-8'))
    for tag in input_file:
        model.addTag(catalog, tag)
    return model.tagSize(catalog)


def loadBooksTags(catalog):
    """
    Carga la información que asocia tags con libros.
    """
    booktagsfile = cf.data_dir + 'GoodReads/book_tags.csv'
    input_file = csv.DictReader(open(booktagsfile, encoding='utf-8'))
    for booktag in input_file:
        model.addBookTag(catalog, booktag)
    return model.bookTagSize(catalog)


# Funciones de ordenamiento

def sortBooks(control, size):
    """
    Ordena los libros por average_rating
    """
    return model.sortBooks(control['model'], size)


# Funciones de consulta sobre el catálogo

def getBooksByAuthor(control, authorname):
    """
    Retrona los libros de un autor
    """
    author = model.getBooksByAuthor(control['model'], authorname)
    return author


def getBestBooks(control, number):
    """
    Retorna los mejores libros
    """
    bestbooks = model.getBestBooks(control['model'], number)
    return bestbooks


def countBooksByTag(control, tag):
    """
    Retorna los libros que fueron etiquetados con el tag
    """
    return model.countBooksByTag(control['model'], tag)
