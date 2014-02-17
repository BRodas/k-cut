# Se importa la libreria que selecciona de manera aleatoria
import random
# Se importa la libreria numpy
import numpy
# Libreria que se usa para poder ordenar las instancias
import operator


#################################################
class entregaID:
    def __init__(self, coords, ID):
        self.coords = coords
        self.ID = str(ID)


#################################################
class vector_resultante:
    # El metodo inicial
    def __init__(self, vector_muestra, vector_poblacion, distancia):

        # Distancia euclideana
        if distancia == 'euclideana':
            self.distancia = numpy.sqrt(
                numpy.sum(
                    numpy.power(
                        numpy.array(vector_muestra.coords)
                        -
                        numpy.array(vector_poblacion.coords), 2)))
        elif distancia == 'bloques':
            self.distancia = numpy.sum(
                numpy.abs(
                    numpy.array(vector_muestra.coords)
                    -
                    numpy.array(vector_poblacion.coords)))
        # Aqui se pueden agregar diferentes "elif" con otras distancias,
        # como por ejemplo la Manhathan (de bloques).
        self.ID = str(vector_poblacion.ID)
        self.coords = vector_poblacion.coords
        self.nombre = "%s,%s" % (vector_muestra.coords,
                                 vector_poblacion.coords)
        # AGREGAR UN ID, OJO PENSAR EN  CAMBIAR UN POCO LA ESTRUCTURA
        # self.ID =
        self.vector_muestra = vector_muestra.coords
        self.vector_poblacion = vector_poblacion.coords


#################################################
def funcion_distancias(muestra_aleatoria, listado_vectores, dist):
    """Esta funcion calcula la matriz de distancia entre
    los vectores de la muestra y los TODOS los vectores."""

    # Transformacion de los listados en arreglos NumPy
    muestra_aleatoria = numpy.array(muestra_aleatoria)
    listado_vectores = numpy.array(listado_vectores)

    # Se calcula la distancia. Cada vector de la muestra se calcula con
    # cada vector de la poblacion total entregada
    matriz_distancias = [[vector_resultante(i, j, dist)
                          for j in listado_vectores]
                         for i in muestra_aleatoria]

    return matriz_distancias


#################################################
# Funcion que chequea la existencia del elemento en el listado
def chequeo_valores_unicos(objeto_chequear,
                           listado_con_objetos,
                           listado_con_objetos_2=None):

    cond_1 = False
    cond_2 = False

    for objeto in listado_con_objetos:
        if objeto.ID == objeto_chequear.ID:
            cond_1 = True

    for objeto_2 in listado_con_objetos_2:
        if objeto_2.ID == objeto_chequear.ID:
            cond_2 = True

    if (cond_1 or cond_2):
        return False

    return True


#################################################
def dist(v1, v2):
    v1 = numpy.array(v1)
    v2 = numpy.array(v2)
    return numpy.sqrt(numpy.sum(numpy.power(v1 - v2, 2)))


#################################################
def find_IdColumn(matrix):
    min_sum = 999999999999999
    ID = None
    for index in range(len(matrix)):
        if min_sum > numpy.sum(matrix[index, :]):
            min_sum = numpy.sum(matrix[index, :])
            ID = index

    return ID


#################################################
def propiedades(conj_clusters, beta=0.95):
    """ ."""

    IDmed = [None for i in range(len(conj_clusters))]

    for s in range(len(conj_clusters)):
        ls = len(conj_clusters[s])
        Cen = numpy.zeros((ls, ls))

        for i in range(int(beta * ls) - 1):
            for j in range(i + 1, int(beta * ls)):
                Cen[i, j] = dist(conj_clusters[s][i].coords,
                                 conj_clusters[s][j].coords)
                Cen[j, i] = Cen[i, j]

        IDmed[s] = conj_clusters[s][find_IdColumn(Cen)]

    # A continuacion se forma el problema reducido como sigue
    Dred = [[None for ind_k in range(ind_s + 1, len(conj_clusters))]
            for ind_s in range(len(conj_clusters) - 1)]
    for ind_s in range(len(conj_clusters) - 1):
        for ind_k in range(len(conj_clusters) - ind_s - 1):
            Dred[ind_s][ind_k] = dist(
                IDmed[ind_s].coords, IDmed[ind_k].coords)

    return Dred, IDmed


#################################################
# Se define la heuristica
def heuristica_K_cut(listado_vectores=[range(i, i + 3) for i in range(5)],
                     tamano_muestra=None, cantidad_R=3, alpha=0.05,
                     porc_radio_teorico=.95, conjA_mas_conjL=True,
                     dist='euclideana'):
    """Esta funcion define una heuristica para seleccionar vectores.
    Que si bien no es exclusivo en este caso se ha creado para alimentar
    el algoritmo K-Cut.

    porc_radio_teorico: Es el porcentaje de elementos desde el cual
    se calcula el radio teorico

    listado_vectores: Es una LISTA de vectores (LISTA/TUPLA) de igual
    dimension

    cantidad_R: Es el numero de muestras equidistanciadas por columnas
    ya ordenadas."""

    ##### PASO 0 ####
    # Generacion de IDs
    listado_vectores = [entregaID(listado_vectores[i], i)
                        for i in range(len(listado_vectores))]

    ##### PASO 1 #####
    # Seleccion aleatoria de una muestra de vectores, si no se da una cantidad
    # se considera toda la muestra.
    muestra_aleatoria = (listado_vectores
                         if tamano_muestra is None
                         else random.sample(listado_vectores, tamano_muestra))

    # Calculo de la distancia de los vectores muestra a TODA la poblacion.
    # Notese que el tipo de distancia se da como parametro
    matriz_distancias = funcion_distancias(muestra_aleatoria,
                                           listado_vectores,
                                           dist)

    ##### PASO 2 #####
    # En este paso lo que se hace es ordenar el contenido de la matriz
    # Notese que con respecto al power point con que se ha armado esta
    # implementacion, la siguiente matriz estaria invertida.
    matriz_ordenada = [sorted(vector_a_ordenar,
                              key=operator.attrgetter('distancia'))
                       for vector_a_ordenar in matriz_distancias]

    ##### PASO 3 #####
    # Se seleccionan un numero fijo (R) de muestras equi-espaciadas dentro de
    # cada columna de M_ord. Lo que permite seleccionar muestras de partida que
    # se alejan progresivamente de las primeras muestras seleccionadas en forma
    # aleatoria.
    # NOTESE: Aqui la matriz esta transpuesta, por lo tanto son FILAS.
    nuevos_vectores_muestra = []
    # Se calcula el salto
    saltos = (len(matriz_ordenada[0]) - 1) / cantidad_R
    # Recorrido por cada fila
    for fila in matriz_ordenada:
        # Se seleccionan los objetos saltando segun los saltos indicados
        for objeto_agregar in [obj for obj in fila[saltos - 1::saltos]]:
            if chequeo_valores_unicos(objeto_agregar,
                                      nuevos_vectores_muestra,
                                      muestra_aleatoria):
                nuevos_vectores_muestra.append(objeto_agregar)
            else:
                inicio = fila.index(objeto_agregar)
                for objeto_alternativo in fila[inicio:]:
                    if chequeo_valores_unicos(objeto_alternativo,
                                              nuevos_vectores_muestra,
                                              muestra_aleatoria):
                        nuevos_vectores_muestra.append(objeto_alternativo)
                        break

    ### LINEA 5 DEL PSEUDOCODIGO
    # Calculo de la distancia de los vectores muestra a TODA la poblacion.
    # Notese que el tipo de distancia se da como parametro
    conj_L_distancias = funcion_distancias(nuevos_vectores_muestra,
                                           listado_vectores,
                                           dist)

    # paso 6 del pseudo codigo
    conj_L_ordenado = [sorted(vector_a_ordenar,
                              key=operator.attrgetter('distancia'))
                       for vector_a_ordenar in conj_L_distancias]

    if (conjA_mas_conjL is True):
        # paso 8 del pseudo codigo: la union
        matriz_ordenada = matriz_ordenada + conj_L_ordenado
    else:
        matriz_ordenada = conj_L_ordenado

    list_SN = [[] for i in range(len(matriz_ordenada))]

    # linea 12 pseudo codigo
    conj_y = [str(i) for i in range(len(listado_vectores))]
    i = 1

    # linea 14 pseudo codigo
    while len(conj_y) >= int(alpha * len(listado_vectores)):
        for ind_s in range(len(matriz_ordenada)):
            if matriz_ordenada[ind_s][i].ID in conj_y:
                list_SN[ind_s].append(matriz_ordenada[ind_s][i])
                conj_y.remove(matriz_ordenada[ind_s][i].ID)
        i += 1

    Dred, IdDred = propiedades(list_SN)

    return Dred, IdDred


#################################################
# Para realizar un testeo
if __name__ == '__main__':

    listado_vectores = [[5, 1], [2, 1], [1, 3], [4, 4], [4, 3], [4, 3],
                        [1, 4], [3, 4], [8, 9], [9, 8], [10, 10], [9, 7],
                        [6, 9], [7, 7], [8, 10], [8, 7], [12, 3],
                        [11, 1], [14, 1], [12, 2], [12, 1]]
    heuristica_K_cut(listado_vectores=listado_vectores,
                     tamano_muestra=3, cantidad_R=2, conjA_mas_conjL=False)
