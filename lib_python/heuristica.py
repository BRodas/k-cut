# Se importa la libreria que selecciona de manera aleatoria
import random
# Se importa la libreria numpy
import numpy
# Libreria que se usa para poder ordenar las instancias
import operator


#################################################
class vector_resultante:
    # El metodo inicial
    def __init__(self, vector_muestra, vector_poblacion, distancia):
        # Distancia euclideana
        if distancia == 'euclideana':
            self.distancia = numpy.sqrt(
                numpy.sum(numpy.power(vector_muestra - vector_poblacion, 2)))
        elif distancia == 'bloques':
            self.distancia = numpy.sum(
                numpy.abs(vector_muestra - vector_poblacion))
        # Aqui se pueden agregar diferentes "elif" con otras distancias,
        # como por ejemplo la Manhathan (de bloques).

        self.nombre = "%s,%s" % (vector_muestra, vector_poblacion)
        self.vector_muestra = vector_muestra
        self.vector_poblacion = vector_poblacion


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
def chequeo_valores_unicos(objeto_chequear, listado_con_objetos):

    if listado_con_objetos == []:
        return True

    for objeto in listado_con_objetos:
        #print objeto
        #print objeto_chequear
        #print listado_con_objetos

        if str(objeto) == str(objeto_chequear):
            return False

    return True


#################################################
# Se define la clase para las propiedades de cada grupo
class propiedades:
    def __init__(self, listado_objetos, porc_radio_teorico, distancia):
        """Para la inicializacion de esta clase el:

        listado_objetos
        que se entrega es una lista de objetos,
        tal que cada uno de estos es de la clase

        vector_resultante"""

        # A continuacion el calculo del promedio
        suma = 0
        for objeto in listado_objetos:
            suma += objeto.distancia
        self.distancia_promedio = numpy.divide(suma, len(listado_objetos))

        # Luego se ve cual es el elemento mas cercano al promedio, y se declara
        # como el medoide.
        indice_medoide = numpy.argmin(
            numpy.abs([objeto.distancia for objeto in listado_objetos]
                      - self.distancia_promedio))
        self.medoide_vector = listado_objetos[indice_medoide].vector_poblacion

        # Se debe calcular la distancia del medoide a los otros valores
        distancias_al_medoide = [
            vector_resultante(self.medoide_vector,
                              objeto.vector_poblacion, distancia)
            for objeto in listado_objetos]

        # Por comodidad para mas adelante estos se ordenan
        distancias_al_medoide = sorted(distancias_al_medoide,
                                       key=operator.attrgetter('distancia'))

        # Se calcula el radio teorico del grupo, en base al medoide, y que
        # vectores pertenecen al radio teorico.
        indice_radio_teorico = int(
            len(distancias_al_medoide) * porc_radio_teorico)
        self.radio_teorico = distancias_al_medoide[
            indice_radio_teorico].distancia


#################################################
# Se define la heuristica
def heuristica_K_cut(listado_vectores=[range(i, i + 3) for i in range(5)],
                     tamano_muestra=None, cantidad_R=3,
                     porc_radio_teorico=.95,
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

    ##### PASO 1 #####
    # Seleccion aleatoria de una muestra de vectores, si no se da una cantidad
    # se considera toda la muestra.
    muestra_aleatoria = (listado_vectores
                         if tamano_muestra is None
                         else random.sample(listado_vectores, tamano_muestra))

    # Calculo de la distancia de los vectores muestra a TODA la poblacion.
    # Notese que la distancia se da como parametro
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
    # Recorrido por cada fila
    for fila in matriz_ordenada:
        # Se calcula el salto
        saltos = len(fila) / cantidad_R
        # Se seleccionan los objetos saltando segun los saltos indicados
        for objeto_agregar in [obj.vector_poblacion
                               for obj in fila[saltos::saltos]]:
            if chequeo_valores_unicos(objeto_agregar, nuevos_vectores_muestra):
                nuevos_vectores_muestra.append(objeto_agregar)

    ##### PASO INTERMEDIO #####
    # Antes de proceder al paso 4, voy a juntar todos los vectores muestra en
    # una sola lista.
    for vector in muestra_aleatoria:
        if chequeo_valores_unicos(numpy.array(vector),
                                  nuevos_vectores_muestra):
            nuevos_vectores_muestra.append(numpy.array(vector))

    ##### PASO 4 #####
    # Ahora con este nuevo vector se calcula la distancia a todo el resto.
    matriz_distancias = funcion_distancias(nuevos_vectores_muestra,
                                           listado_vectores, dist)

    ##### PASO 5 #####
    # Se ordenan la matriz (M_ini) de menor a mayor (por columnas) y se
    # guarda el ID de las muestras con respecto a la que se midio
    # la distancia.
    matriz_ordenada = [sorted(vector_a_ordenar,
                              key=operator.attrgetter('distancia'))
                       for vector_a_ordenar in matriz_distancias]

    ##### PASO 6 #####
    # Se forman los grupos considerando un corte de la matriz M_ini
    # que incluya un alto porcentaje de la data (98%).
    # Por lo tanto lo primero es contar TODOS los elementos de un arreglo.
    punto_corte = int(len(matriz_ordenada[0]) * .98)
    matriz_ordenada = numpy.array(matriz_ordenada)
    matriz_ordenada = matriz_ordenada[:, :punto_corte]

    ##### PASO 7 #####
    # Se calculan las propiedades de los super nodos,
    # el medoid y radio teorico del grupo. Este ultimo se define
    # como la distancia a la que mas del 95% de las muestras del
    # grupo son incluidas. De esta forma se pondera la distancia
    # entre super nodos incorporando la distancia de los medoids
    # y la distancia entre cluster restando los radios teoricos.
    listado_propiedades_grupo = [propiedades(grupo, porc_radio_teorico, dist)
                                 for grupo in matriz_ordenada]

    """Las cada elemento de la lista es una instancia de la
    clase "propiedades", los atributos son:

    propiedades.distancia_promedio: la distancia promedio entre
    todos los puntos del grupos.

    propiedades.medoide_vector: el elemento mas cercano a
    el promedio/centroide.

    propiedades.radio_teorico: radio teorico del grupo.
    """

    return listado_propiedades_grupo


#################################################
# Para realizar un testeo
if __name__ == '__main__':

    listado_vectores = [[5, 1], [2, 1], [1, 3], [4, 4], [4, 3], [4, 3],
                        [1, 4], [3, 4], [8, 9], [9, 8], [10, 10], [9, 7],
                        [6, 9], [7, 7], [8, 10], [8, 7], [12, 3],
                        [11, 1], [14, 1], [12, 2], [12, 1]]
    heuristica_K_cut(listado_vectores=listado_vectores,
                     tamano_muestra=3, cantidad_R=3)
