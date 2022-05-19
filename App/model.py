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
from DISClib.ADT import map as m
from DISClib.ADT import graph as gr
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort as sa
from DISClib.Utils import error as error
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newAnalyzer():
    """ Inicializa el analizador

   stops: Tabla de hash para guardar los vertices del grafo
   connections: Grafo para representar las rutas entre estaciones
   components: Almacena la informacion de los componentes conectados
   paths: Estructura que almancena los caminos de costo minimo desde un
           vertice determinado a todos los otros vértices del grafo
    """
    try:
        analyzer = {
                    'stations': None,
                    'connections': None,
                    'components': None,
                    'paths': None
                    }

        analyzer['stations'] = m.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=compareStopIds)

        analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              comparefunction=compareStopIds)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')

# Funciones para agregar informacion al catalogo

def addstationConnections(analyzer, trip):
    
    origin = trip['Start Station Id']
    destination = trip['End Station Id']
    time = trip['Trip  Duration']
    
    addStation(analyzer, origin)
    
    addStation(analyzer, destination)
    
    addConnection(analyzer, origin, destination, time)
    
    addRouteStation(analyzer, origin, trip)
    
    return analyzer

def addRouteStation(analyzer, stationID, info):
    
    entry = m.get(analyzer['stations'], stationID)
    
    if entry is None:
        station = newStation(stationID)
        m.put(analyzer['stations'], stationID, station)
    else:
        station = me.getValue(entry)
    lt.addLast(station['endstations'], info)
    return analyzer

def addStation(analyzer, stationID):
    """
    Adiciona una estación como un vertice del grafo
    """
    try:
        if not gr.containsVertex(analyzer['connections'], stationID):
            gr.insertVertex(analyzer['connections'], stationID)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addStation')


def addConnection(analyzer, origin, destination, time):
    """
    Adiciona un arco entre dos estaciones
    """
    edge = gr.getEdge(analyzer['connections'], origin, destination)
    if edge is None:
        gr.addEdge(analyzer['connections'], origin, destination, time)
    return analyzer

# Funciones para creacion de datos

def newStation(stationID):
    
    station = {'startstation': stationID,
               'endstations': lt.newList('SINGLE_LINKED')}
    
    return station

# Funciones de consulta

def totalStops(analyzer):
    """
    Retorna el total de estaciones (vertices) del grafo
    """
    return gr.numVertices(analyzer['connections'])

def totalConnections(analyzer):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(analyzer['connections'])

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento

def compareStopIds(stop, keyvaluestop):
    """
    Compara dos estaciones
    """
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1
    
    
# Funcinoes support

def formatVertex(trip):
    """
    Se formatea el nombrer del vertice con el id de la estación
    seguido de la ruta.
    """
    name = trip['Start Station Id']
    name2 = trip['End Station Id']
    return name, name2
