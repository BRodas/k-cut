# A continuacion el algoritmo de corte minimo
# dado un grafo

# La implementacion de este algoritmo fue desarrollada por Raul Bernardo
# Rodas Herrera, el 20 de Septiembre del ano 2013.

# Se importan las librerias correspondientes
# Libreria para el manejo de grafos.
# Para obtener valores aleatorios
import random


#################################################
# Esta funcion modifica el grafo dado un par de nodos para contraer
def contraer(grafo, nodo_1, nodo_2):
    # Nodos unidos:	En esta parte lo que se hace es ordenar el string
    # que contiene los nodos que estan unidos
    nuevo_nodo = "%s,%s" % (nodo_1, nodo_2)
    nuevo_nodo = sorted([int(i) for i in nuevo_nodo.split(',')])
    nuevo_nodo = ','.join(str(i) for i in nuevo_nodo)
    # Listado de nodos que se mantienen y que se unen
    nodos = grafo.nodes()
    nodos_mantienen = set(nodos) - set([nodo_1]) - set([nodo_2])
    nodos_mantienen = [i for i in nodos_mantienen]
    #nodos_mantienen = [i for i in nodos if (i != nodo_1 and i != nodo_2)]
    # Se crea el grafo contraido, vacio
    contraccion = grafo.subgraph(nodos_mantienen)

    # Se agrega el nodo que se merge/unio
    # contraccion.add_node(nuevo_nodo)

    # Se agregan los arcos con peso, del nuevo nodo
    # Esta parte genera un listado con las distancias de los nodos que se
    # unieron.
    iterador = grafo.edges_iter(nbunch=[nodo_1, nodo_2], data="weight")

    # Con esta linea agregar los arcos que correspondian a la fucion de nodos
    lista_agregar = [(i[0], i[1], i[2]['weight'])
                     for i in iterador
                     if ([i[0], i[1]] != [nodo_1, nodo_2]
                         and [i[1], i[0]] != [nodo_1, nodo_2])]

    # Aqui se remplazan los nombres
    lista_agregar = [(nuevo_nodo, tupla[1], tupla[2])
                     if (tupla[0] == nodo_1 or tupla[0] == nodo_2)
                     else (tupla[0], nuevo_nodo, tupla[2])
                     for tupla in lista_agregar]

    # Finalmente se agrega la lista
    contraccion.add_weighted_edges_from(lista_agregar)

    # Se retorna el grafico contraido
    return contraccion


################################################
def transformar_a_conj(elemento):
    """Esta funcion transforma el elemento rapidamente en un conjunto"""
    if type(elemento) == str:
        conjunto = set([int(i) for i in elemento.split(',')])
    else:
        conjunto = set([elemento])

    return conjunto


# Funcion que chequea pertenencia
def chequeadora_pertenencia(arco_inicial, arco_chequear):

    # que la condicionparta siendo False, significa que el archo a chequear no
    # deberia ser parte del listado de no seleccionables.
    condicion = False

    # Primero voy a transformar los nodos de "arco_chequear" en un conjunto
    conj_1 = transformar_a_conj(arco_chequear[0])
    conj_2 = transformar_a_conj(arco_chequear[1])

    # Lo mismo pero con el "arco_inicial"
    subconj_1 = transformar_a_conj(arco_inicial[0])
    subconj_2 = transformar_a_conj(arco_inicial[1])

    # Chequeo si los elemento de "arco_inicial" estan en "arco_chequear"
    if subconj_1.issubset(conj_1) and subconj_2.issubset(conj_2):
        condicion = True
    elif subconj_2.issubset(conj_1) and subconj_1.issubset(conj_2):
        condicion = True

    return condicion


#################################################
# Aqui se define la funcion que genera un grafo contraido
def contraer_hasta_2_nodos(grafo, arco_inicial=None):

    # Se estima este parametro, el cual es condicion de detencion
    num_vertices_grafo = len(grafo.nodes())

    # Variable que indica si se es la primera iteracion o no
    primera_iteracion = True
    # Mientras la cantidad de vertices sea mayor estricto que 2, procede:
    while num_vertices_grafo > 2:

        # El siguiente es el conjunto de donde se elige el arco al azar, notese
        # que se sustrae el arco seleccionado como arco_inicial
        if primera_iteracion:
            # Al final de esta iteracion la variable se marca como False
            conjunto_eleccion_arco = set(grafo.edges()).difference(
                [arco_inicial])
            listado_seleccion = list(conjunto_eleccion_arco)
            elem_rand = random.choice(listado_seleccion)
            indice_arco_azar = grafo.edges().index(elem_rand)
            primera_iteracion = False
        # Puesto que se esta en la segunda iteracion, o mayor
        else:
            # Se crea/limpia el listado_no_elegible
            listado_no_elegible = []
            # Aqui comienzan las modificaciones respectivas.
            for arco in grafo.edges():
                # Este se_elige_arco puede parecer confuso, en realidad es un
                # se elige para no ser elegido, es por eso que si es True la
                # respuesta de la funcion para a incorporarse al listado de no
                # seleccionados.
                se_elige_arco = chequeadora_pertenencia(arco_inicial,
                                                        arco)
                if se_elige_arco:
                    listado_no_elegible.append(arco)

            conjunto_eleccion_arco = set(grafo.edges()).difference(
                listado_no_elegible)
            listado_seleccion = list(conjunto_eleccion_arco)
            elem_rand = random.choice(listado_seleccion)
            indice_arco_azar = grafo.edges().index(elem_rand)
            primera_iteracion = False

        nodo_1 = grafo.edges()[indice_arco_azar][0]
        nodo_2 = grafo.edges()[indice_arco_azar][1]

        # Contrae en UN SOLO nodo los nodos del vertice elegido.
        # Recordar que esto actualiza el grafo
        grafo = contraer(grafo, nodo_1, nodo_2)

        # Se estima este parametro, el cual es condicion de detencion
        num_vertices_grafo = len(grafo.nodes())

    # Retorna el grafo final
    return grafo


#################################################
# Aqui se define la funcion, recordar que G,
# es una instancia "grafo" del tipo "networkX"
def min_cut(grafo, num_iteraciones=1000, arco_inicial=None):

    # Suma del corte inicial, esto es infinito
    suma_corte_minimo = 9999999999999999

    # Se establece el conjunto de arcos cortados de manera vacia
    conj_arcos_cortados = set()

    ### ESTE FOR ES PARALELIZABLE ###
    # Numero de iteraciones buscando el valor minimo
    for iteracion in range(num_iteraciones):

        # Se contrae el grafo
        resultado = contraer_hasta_2_nodos(grafo, arco_inicial)

        # Suma del MultiGrafo resultante.
        iterador = resultado.edges_iter(data="weight")
        suma_corte = sum([i[2]["weight"] for i in iterador])

        # Si se supera el valor anterior
        if suma_corte < suma_corte_minimo:
            # Suma del corte
            suma_corte_minimo = suma_corte
            # Se guarda el mejor grafo hasta el minuto
            grafo_final = resultado

    ##################################################
    # A continuacion lleno el conjunto de arcos cortados
    # Si el primer nodo de los dos resultantes es un entero:
    nodo_1 = grafo_final.nodes()[0]
    nodo_2 = grafo_final.nodes()[1]
    if type(nodo_1) == int:
        # El segundo obligadamente es un String
        conj_arcos_cortados = set(
            [tuple(sorted((nodo_1, int(i))))
             for i in nodo_2.split(',')])
    # si no es un entero, entonces es un String
    else:
        # en ese caso el segundo puede ser un entero
        if type(nodo_2) == int:
            # en cuyo caso se hace la misma idea que el primer "if"
            conj_arcos_cortados = set(
                [tuple(sorted((int(i), nodo_2)))
                 for i in nodo_1.split(',')])
        # Por otro lado si es tambien un String
        else:
            conj_arcos_cortados = set(
                [tuple(sorted((int(i), int(j))))
                 for i in nodo_1.split(',')
                 for j in nodo_2.split(',')])

    # Se asignan nuevos atributos
    grafo_final.Suma_corte_minimo = suma_corte_minimo
    grafo_final.conj_arcos_cortados = conj_arcos_cortados

    return grafo_final
