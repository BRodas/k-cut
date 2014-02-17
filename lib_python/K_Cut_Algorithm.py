# K-Cut algorithm
# A continuacion el algoritmo K-Cut

# Se importan las librerias a usar
# Esta libreria es la que tiene la rutina que calcula el corte minimo
import Min_Cut_Kargers
# Esta libreria crea una red
import networkx as nx
# Libreria para importar el CSV
import numpy
# Libreria del tiempo
from datetime import datetime


#################################################
def K_Cut(arcos_con_pesos=[(1, 2, 70), (2, 4, 10), (3, 4, 105),
                           (1, 3, 1)], porc_error=0.005,
          K_obj=2):
    """Funcion que calcula un K-Cut.

    arcos_con_pesos, es un LISTADO de TUPLAS/LISTAS.
    Ejemplo: [(nodo11, nodo12, dist1), (nodo21, nodo22, dist2), ...]

    porc_error, es un decimal que indica cual es el error porcentual"""

    #################################################
    # La idea es armar en esta parte el grafo
    # Se crea la instancia del GRAFO
    G = nx.MultiGraph()
    # Se agregan los arcos con peso, que en este caso son las distancias
    # entre los vertices.
    # El formato es (nodo_1,nodo_2, distancia_entre_nodos)
    #G.add_weighted_edges_from()
    G.add_weighted_edges_from(arcos_con_pesos)

    #################################################
    # Se resuelve el GRAFO INICIAL
    num_nodos = len(G.nodes())
    numerador = numpy.log(porc_error)
    factorial = num_nodos * numpy.true_divide(num_nodos - 1, 2) - 1
    denominador = numpy.log(1 - numpy.true_divide(1, factorial))
    # Con esto se calcula el numero de iteraciones
    itera = int(numpy.true_divide(numerador, denominador))
    print "Num. Iteraciones %s %s" % (itera, '\n')
    # En el siguiente diccionario se guardaran los grafos resultantes
    # dado el arco inicial entregado.
    listado_grafos = []
    # Realizo una iteracion arco por arco
    for arco in G.edges_iter():
        # Calcula el min cut para CADA arco.
        #print arco
        Grafo_final = Min_Cut_Kargers.min_cut(G, itera, arco)
        Grafo_final.arco_inicial = arco
        listado_grafos.append(Grafo_final)

    # Terminada la iteracion arco por arco, ordeno segun la suma del corte y en
    # orden ascendente.
    listado_grafos.sort(key=lambda x: x.Suma_corte_minimo,
                        reverse=False)

    ################################################
    # Aqui comienza la seleccion tipo "greedy", que corresponde al tercer paso
    # del algoritmo Min-Cut.

    # Conjunto de arcos
    conj_arcos_final = set(G.edges())
    conj_arcos_cortados = set()
    K = 1
    # Se van recorriendo los grafos uno por uno
    for grafo in listado_grafos:

        # Se chequea si el conjunto de corte del presente grafo esta contenido
        # en la union de los que ya han pasado.
        if not grafo.conj_arcos_cortados.issubset(conj_arcos_cortados):
            # Voy a sumar un cluster
            K += 1
            # Voy a agregar aquel conjunto de arcos cortados al acumulado de
            # conjunto de arcos cortados
            conj_arcos_cortados.update(grafo.conj_arcos_cortados)
            # Ademas voy a restar estos arcos cortados del conjunto de arcos
            # que se entrega al final.
            conj_arcos_final.difference_update(grafo.conj_arcos_cortados)
            # Si llegue a la cantidad de clusters que queria
            if K == K_obj:
                # Termino el ciclo
                break

    # Se muestra el conjunto de arcos que se cortaron
    print "los cortados: %s %s" % (conj_arcos_cortados, '\n')
    # Lo que devuelve el conjunto
    return conj_arcos_final


#################################################
def dist_inv_entre_puntos(listado, listado_2):
    """Esta funcion se le entrega un listado de coordenadas (X,Y), y
    luego se calculan las distancias todos con todos. Devuelve un
    listado con los nodos y la distancia entre ellos."""

    # Se transforman los listado a arreglos numpy
    listado = numpy.array(listado)
    listado_2 = numpy.array(listado_2)
    # Luego creo un par de listas donde voy a guardar los resultados
    resultado = []
    # Luego se recorre elemento por elemento el primer listado entregado
    for indice in range(len(listado)):
        # Ademas se recorre el segundo listado entregado. Notese que lo que se
        # esta llenando es el triangulo inferior de la matriz
        for indice_2 in range(indice + 1, len(listado_2)):
            # Y se calcula la distancia entre estos nodos
            resultado.append((int(indice + 1),
                              int(indice_2 + 1), float(1) /
                              numpy.sqrt(
                                  numpy.sum(
                                      numpy.power(
                                          listado[indice] -
                                          listado_2[indice_2], 2)))))

    return resultado

# El famoso main
if __name__ == '__main__':

    #listado = [(1, 2, float(1) / 70),
    #           (1, 3, float(1) / 95),
    #           (1, 4, float(1) / 105),
    #           (1, 5, float(1) / 83),
    #           (2, 3, float(1) / 25),
    #           (2, 4, float(1) / 35),
    #           (2, 5, float(1) / 13),
    #           (3, 4, float(1) / 10),
    #           (3, 5, float(1) / 14),
    #           (4, 5, float(1) / 24)]

    error_porcentual = 0.05

    # Primero se importa el archivo
    datos_brutos = numpy.genfromtxt('../Ejemplos/DB_Toy0.csv',
                                    delimiter=';')

    # Calculo de distancia entre los puntos
    # Lo que se quiera testear
    for K in range(4, 5):
        print "K %s %s" % (K, '\n')
        print "Hora Inicio %s %s" % (datetime.now(), '\n')
        # Calculo la distancia entre los nodos
        listado = dist_inv_entre_puntos(datos_brutos[:, 0:2],
                                        datos_brutos[:, 0:2])
        resultado = K_Cut(listado, error_porcentual, K)
        print "resultado del cluster %s %s" % (resultado, '\n')
