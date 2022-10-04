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
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
assert cf

"""
Se define la estructura de un catálogo de libros.
El catálogo tendrá tres listas, una para libros, otra para autores
y otra para géneros
"""
#CLASE 
"""
for k in lt.iterator(mp.KeySet(mapa))
    print("llave" )


def compareKeys(k1, entry):
    k2 = me.getKey(entry)

print('size:', len(mapa["table"]["elementes"]))
"""
# Construccion de modelos


def newCatalog():
    """ Inicializa el catálogo de libros

    Crea una lista vacia para guardar todos los libros

    Se crean indices (Maps) por los siguientes criterios:
    Autores
    ID libros
    Tags
    Año de publicacion

    Retorna el catalogo inicializado.
    """
    catalog = {'books': None,
               'bookIds': None,
               'authors': None,
               'tags': None,
               'tagIds': None,
               'years': None,
               'titles': None}

    """
    Esta lista contiene todo los libros encontrados
    en los archivos de carga.  Estos libros no estan
    ordenados por ningun criterio.  Son referenciados
    por los indices creados a continuacion.
    """
    catalog['books'] = lt.newList('SINGLE_LINKED', compareBookIds)

    """
    A continuacion se crean indices por diferentes criterios
    para llegar a la informacion consultada.  Estos indices no
    replican informacion, solo referencian los libros de la lista
    creada en el paso anterior.
    """

    """
    Este indice crea un map cuya llave es el identificador del libro
    """
    catalog['bookIds'] = mp.newMap(10000,
                                   maptype='CHAINING',
                                   loadfactor=2,
                                   comparefunction=compareMapBookIds)

    """
    Este indice crea un map cuya llave es el autor del libro
    """
    catalog['authors'] = mp.newMap(800,
                                   maptype='CHAINING',
                                   loadfactor=2,
                                   comparefunction=compareAuthorsByName)
    """
    Este indice crea un map cuya llave es la etiqueta
    """
    catalog['tags'] = mp.newMap(34500,
                                maptype='PROBING',
                                loadfactor=0.5,
                                comparefunction=compareTagNames)
    """
    Este indice crea un map cuya llave es el Id de la etiqueta
    """
    catalog['tagIds'] = mp.newMap(34500,
                                  maptype='PROBING',
                                  loadfactor=0.5,
                                  comparefunction=compareTagIds)
    """
    Este indice crea un map cuya llave es el año de publicacion
    """
    catalog['years'] = mp.newMap(40,
                                 maptype='PROBING',
                                 loadfactor=0.5,
                                 comparefunction=compareMapYear)

    # TODO modificaciones para el laboratorio 6
    """
    Este indice crea un map cuya llave es el titulo del libro
    La columna 'title' del archivo books.csv
    """
    catalog['title'] = mp.newMap(10000,
                                 maptype='PROBING',
                                 loadfactor=2,
                                 comparefunction=compareTitles
                                  )

    return catalog


# Funciones para creacion de datos

def newAuthor(name):
    """
    Crea una nueva estructura para modelar los libros de un autor
    y su promedio de ratings. Se crea una lista para guardar los
    libros de dicho autor.
    """
    author = {'name': "",
              "books": None,
              "average": 0,
              "average_rating": 0}
    author['name'] = name
    author['books'] = lt.newList('SINGLE_LINKED', compareAuthorsByName)
    return author


def newBookTag(name, id):
    """
    Esta estructura crea una relación entre un tag y los libros que han sido
    marcados con dicho tag.  Se guarga el total de libros y una lista con
    dichos libros.
    """
    tag = {'name': '',
           'tag_id': '',
           'total_books': 0,
           'books': None,
           'count': 0.0}
    tag['name'] = name
    tag['tag_id'] = id
    tag['books'] = lt.newList()
    return tag


# Funciones para agregar informacion al catalogo

def addBook(catalog, book):
    """
    Esta funcion adiciona un libro a la lista de libros,
    adicionalmente lo guarda en un Map usando como llave su Id.
    Adicionalmente se guarda en el indice de autores, una referencia
    al libro.
    Finalmente crea una entrada en el Map de años, para indicar que este
    libro fue publicaco en ese año.
    """
    lt.addLast(catalog['books'], book)
    mp.put(catalog['bookIds'], book['goodreads_book_id'], book)
    authors = book['authors'].split(",")  # Se obtienen los autores
    for author in authors:
        addBookAuthor(catalog, author.strip(), book)
    addBookYear(catalog, book)


def addBookYear(catalog, book):
    """
    Esta funcion adiciona un libro a la lista de libros que
    fueron publicados en un año especifico.
    Los años se guardan en un Map, donde la llave es el año
    y el valor la lista de libros de ese año.
    """
    try:
        years = catalog['years']
        if (book['original_publication_year'] != ''):
            pubyear = book['original_publication_year']
            pubyear = int(float(pubyear))
        else:
            pubyear = 2020
        existyear = mp.contains(years, pubyear)
        if existyear:
            entry = mp.get(years, pubyear)
            year = me.getValue(entry)
        else:
            year = newYear(pubyear)
            mp.put(years, pubyear, year)
        lt.addLast(year['books'], book)
    except Exception:
        return None


def newYear(pubyear):
    """
    Esta funcion crea la estructura de libros asociados
    a un año.
    """
    entry = {'year': "", "books": None}
    entry['year'] = pubyear
    entry['books'] = lt.newList('SINGLE_LINKED', compareYears)
    return entry


def addBookAuthor(catalog, authorname, book):
    """
    Esta función adiciona un libro a la lista de libros publicados
    por un autor.
    Cuando se adiciona el libro se actualiza el promedio de dicho autor
    """
    authors = catalog['authors']
    existauthor = mp.contains(authors, authorname)
    if existauthor:
        entry = mp.get(authors, authorname)
        author = me.getValue(entry)
    else:
        author = newAuthor(authorname)
        mp.put(authors, authorname, author)
    lt.addLast(author['books'], book)
    author['average'] += float(book['average_rating'])
    totbooks = lt.size(author['books'])
    if (totbooks > 0):
        author['average_rating'] = author['average'] / totbooks


def addTag(catalog, tag):
    """
    Adiciona un tag a la tabla de tags dentro del catalogo y se
    actualiza el indice de identificadores del tag.
    """
    newtag = newBookTag(tag['tag_name'], tag['tag_id'])
    mp.put(catalog['tags'], tag['tag_name'], newtag)
    mp.put(catalog['tagIds'], tag['tag_id'], newtag)


def addBookTag(catalog, tag):
    """
    Agrega una relación entre un libro y un tag.
    Para ello se adiciona el libro a la lista de libros
    del tag.
    """
    bookid = tag['goodreads_book_id']
    tagid = tag['tag_id']
    entry = mp.get(catalog['tagIds'], tagid)

    if entry:
        tagbook = mp.get(catalog['tags'], me.getValue(entry)['name'])
        tagbook['value']['total_books'] += 1
        tagbook['value']['count'] += int(tag['count'])
        book = mp.get(catalog['bookIds'], bookid)
        if book:
            lt.addLast(tagbook['value']['books'], book['value'])


def addBookTitle(catalog, book):
    # TODO modificaciones para el laboratorio 6
    """
    Completar la descripcion de addBookTitle

    """
    titles = catalog['title']
    mp.put(titles, book['title'], book)

# ==============================
# Funciones de consulta
# ==============================


def getBooksByAuthor(catalog, authorname):
    """
    Retorna un autor con sus libros a partir del nombre del autor
    """
    author = mp.get(catalog['authors'], authorname)
    if author:
        return me.getValue(author)
    return None


def getBooksByTag(catalog, tagname):
    """
    Retornar la lista de libros asociados a un tag
    """
    tag = mp.get(catalog['tags'], tagname)
    books = None
    if tag:
        books = me.getValue(tag)['books']
    return books


def getBooksByYear(catalog, year):
    """
    Retorna los libros publicados en un año
    """
    year = mp.get(catalog['years'], year)
    if year:
        return me.getValue(year)['books']
    return None


def getBooksByTitle(catalog, title):
    # TODO modificaciones para el laboratorio 6
    """
    Completar la descripcion de getBookByTitle
    """
    titulo = mp.get(catalog['title'], title)
    if titulo:
       return me.getValue(titulo)
    return None


def booksSize(catalog):
    """
    Número de libros en el catago
    """
    return lt.size(catalog['books'])


def authorsSize(catalog):
    """
    Numero de autores en el catalogo
    """
    return mp.size(catalog['authors'])


def tagsSize(catalog):
    """
    Numero de tags en el catalogo
    """
    return mp.size(catalog['tags'])


def titlesSize(catalog):
    # TODO modificaciones para el laboratorio 6
    """
    Completar la descripcion de titlesSize
    """
    return mp.size(catalog['title'])

# ==============================
# Funciones de Comparacion
# ==============================


def compareBookIds(id1, id2):
    """
    Compara dos ids de dos libros
    """
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1


def compareMapBookIds(id, entry):
    """
    Compara dos ids de libros, id es un identificador
    y entry una pareja llave-valor
    """
    identry = me.getKey(entry)
    if (int(id) == int(identry)):
        return 0
    elif (int(id) > int(identry)):
        return 1
    else:
        return -1


def compareAuthorsByName(keyname, author):
    """
    Compara dos nombres de autor. El primero es una cadena
    y el segundo un entry de un map
    """
    authentry = me.getKey(author)
    if (keyname == authentry):
        return 0
    elif (keyname > authentry):
        return 1
    else:
        return -1


def compareTagNames(name, tag):
    tagentry = me.getKey(tag)
    if (name == tagentry):
        return 0
    elif (name > tagentry):
        return 1
    else:
        return -1


def compareTagIds(id, tag):
    tagentry = me.getKey(tag)
    if (int(id) == int(tagentry)):
        return 0
    elif (int(id) > int(tagentry)):
        return 1
    else:
        return 0


def compareMapYear(id, tag):
    tagentry = me.getKey(tag)
    if (id == tagentry):
        return 0
    elif (id > tagentry):
        return 1
    else:
        return 0


def compareYears(year1, year2):
    if (int(year1) == int(year2)):
        return 0
    elif (int(year1) > int(year2)):
        return 1
    else:
        return 0


def compareTitles(title1, title2):
    # TODO modificaciones para el laboratorio 6
    """
    Completar la descripcion de compareTitles
    """
    if title1 == title2:
        return 1
    else: 
        return 0
