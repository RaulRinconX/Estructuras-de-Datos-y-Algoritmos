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

import config as cf
import model
import csv
csv.field_size_limit(2147483647)
import os#Por repl.it
os.system("pip install pycountry")#Por repl.it
import pycountry as pc


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""
#-------------
#	Iniciar catalogo
#-------------
def initCatalog():
	catalog = model.newCatalog()
	return catalog

#-------------
# Cargar catalogo
#-------------
def loadCatalog(dataFiles, catalog):
	albums, artists, tracks = dataFiles
	loadCSVFile(albums, artists, tracks, catalog)

def loadCSVFile(albumFile, artistFile, trackFile, catalog, sep=",", e = "utf-8-sig"):

	albumFile = cf.data_dir + albumFile
	artistFile = cf.data_dir + artistFile
	trackFile = cf.data_dir + trackFile
	
	with open(artistFile, encoding=e) as artistF:
		bufferArtist = csv.DictReader(artistF)
		for artist in bufferArtist:
			model.addArtist(catalog, artist)
	
	with open(trackFile, encoding=e) as trackF:
		bufferTrack = csv.DictReader(trackF)
		for track in bufferTrack:
			model.addTrack(catalog, track)
		
	with open(albumFile, encoding=e) as albumF:
		bufferAlbum = csv.DictReader(albumF)
		for album in bufferAlbum:
			model.addAlbum(catalog, album)

	model.purify(catalog)
	
#-------------
#Requerimientos
#-------------

def r1AlbumsInYear(catalog, year):
	return model.examAlbumsInYear(catalog, int(year))
	
def r2ArtistByPopularity(catalog, popularity:int):
	return model.findArtistByPopularity(catalog, popularity)

def r3FindTracksByPopularity(catalog, popularity:int):
	return model.findTracksByPopularity(catalog, popularity)

def r4TrackMostPopularByArtist(catalog, artist, market):
	artist = model.getNameArtist(catalog, artist)
	market = pc.countries.get(name=market).apha_2
	return model.findArtistMostPopularTrack(catalog, artist, market)

def r5TracksByArtist(catalog, artist):
	artist = model.getNameArtist(catalog, artist)
	return model.getDiscographyByArtist(catalog, artist)

def r6TracksMostDistributedByArtists(catalog, market, artist, number:int):
	artist = model.getNameArtist(catalog, artist)
	market = pc.countries.get(name=market).apha_2
	return model.clasifyMostDistributedTracks(catalog, artist, market, number)

def sizeCatalog(catalog):
	return model.sizeCatalog(catalog)