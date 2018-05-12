import random
import math
import matplotlib.pyplot as plt


class AlgoritmoGenetico:

    def __init__(self):
        pass


    def generarMatrizIndividuos(self, vector, cantidadIndividuos):
        matrizIndividuos = []
        vectorIndividuos = []
        for i in range(cantidadIndividuos):
            vectorAuxiliar = []  #para romper con pop
            for i in range(len(vector)):
                vectorAuxiliar.append(vector[i])
            for i in range(len(vectorAuxiliar)):
                vectorIndividuos.append(vectorAuxiliar.pop(random.randrange(len(vectorAuxiliar))))
            matrizIndividuos.append(vectorIndividuos)
            vectorIndividuos = []
        return matrizIndividuos


    def generarMatrizOrdenes(self, cantidad, longitud):
        matrizOrdenes = []
        for j in range(cantidad):
            vector = []
            for i in range(longitud):   #generamos matriz de ordenes para base de individuos con 0 y 1
                if i < random.randrange(longitud):
                    vector.append(1)
                else:
                    vector.append(0)
            vectorOrden = []
            for i in range(longitud):
                vectorOrden.append(vector.pop(random.randrange(len(vector))))
            matrizOrdenes.append(vectorOrden)
        return matrizOrdenes




    #iniciar Individuos del almacen y de las ordenes
    def iniciarAlmacen(self, vectorProductos, cantidadIndividuos, cantidadOrdenes):
        self.cantidadIndividuos = cantidadIndividuos
        self.vectorProductos = vectorProductos
        self.matrizProductos = self.generarMatrizIndividuos(vectorProductos,cantidadIndividuos)
        self.matrizOrdenes = self.generarMatrizOrdenes(cantidadOrdenes ,len(vectorProductos))
        return self.matrizProductos, self.matrizOrdenes


    def convertirAlmacenMatriz(self, almacenActual):
        self.almacenActual = almacenActual
        contadorFilas = 0
        contadorColumnas = 0
        configuracionAlmacen = []
        vectorAuxiliar = [] #para appendear a matriz configuracionAlmacen


        i = 0
        while 1:
            if contadorFilas == 4:
                vectorAuxiliar = ['-','-','-','-','-']
                configuracionAlmacen.append(vectorAuxiliar)
                vectorAuxiliar = []
                contadorFilas = 0
            elif len(vectorAuxiliar) == 5:
                configuracionAlmacen.append(vectorAuxiliar)
                vectorAuxiliar = []
                contadorFilas = contadorFilas + 1
                contadorColumnas = 0
            elif contadorColumnas != 2:
                vectorAuxiliar.append(self.almacenActual[i])
                contadorColumnas = contadorColumnas + 1
                i = i + 1
            elif contadorColumnas == 2:
                vectorAuxiliar.append('-')
                contadorColumnas = 0
            if i == len(self.almacenActual) and len(configuracionAlmacen) == len(self.almacenActual)*5/16:
                break


        vectorAuxiliar = []

        for i in range(len(configuracionAlmacen[0])):
            vectorAuxiliar.append('-')
        configuracionAlmacen.insert(0, vectorAuxiliar)

        for i in range(len(configuracionAlmacen)):
            configuracionAlmacen[i].insert(0, '-')
            configuracionAlmacen[i].append('-')

        return configuracionAlmacen


    def fitnessManhattan(self, matrizAlmacen, poblacionOrdenes):
        vectorFitness = []

        for i in range(len(poblacionOrdenes)):
            distanciaX = 0
            distanciaY = 0
            distanciaManhattan = 0
            vectorFilas = []
            vectorColumnas = []
            vectorFilas.append(0)
            vectorColumnas.append(0)


            for j in range (len (poblacionOrdenes[i])):
                for k in range(len(self.matrizAlmacen)):
                    for h in range(len(self.matrizAlmacen[k])):
                        if matrizAlmacen[k][h] == poblacionOrdenes[i][j]:
                            vectorFilas.append(k)
                            vectorColumnas.append(h)
                            break


            vectorFilas.append(0)
            vectorColumnas.append(0)
            for i in range(len(vectorFilas)-1):
                distanciaX = distanciaX + abs((vectorFilas[i + 1] - vectorFilas[i]))
                distanciaY = distanciaY + abs((vectorColumnas[i +1] - vectorColumnas[i]))
            distanciaManhattan = distanciaX + distanciaY
            vectorFitness.append(distanciaManhattan)
        return vectorFitness


    def fitnessOrden(self, almacenActual, vectorOrdenes, cantidadIndividuos):
        self.almacenActual = almacenActual
        #self.vectorOrdenes = vectorOrdenes
        self.cantidadIndividuos = cantidadIndividuos

        vectorOrdenAuxiliar = []
        for i in range (len(vectorOrdenes)):
            if vectorOrdenes[i] == 1:
                vectorOrdenAuxiliar.append(i + 1)
        # print (vectorOrdenAuxiliar)
        # input("")

        poblacion = self.generarMatrizIndividuos(vectorOrdenAuxiliar, cantidadIndividuos) #cantidadIndividuos x longAlmacen

        self.matrizAlmacen = self.convertirAlmacenMatriz(self.almacenActual)
        vectorFitness = []


        # En el for (futuro while) se tiene que actualizar la poblacion, los nuevosPadres para ser mutados y el vectorFitness.
        # Para el vectorFitness tiene que cambiar poblacionOrdenes
        # La matrizAlmacen no cambia

        contador = 0

        while True:
            vectorFitness = self.fitnessManhattan(self.matrizAlmacen, poblacion)
            nuevosPadres = self.cruce(poblacion, vectorFitness, self.seleccionarMejorOrden)
            padresMutados = self.mutacion(nuevosPadres)
            poblacion = padresMutados

            contador = contador + 1

            if contador == 20:
                #print ("Las iteraciones han excedido el valor maximo")
                return min(vectorFitness)
                break

            contadorDiferencias = 0
            for i in range (len(vectorFitness) - 1):
                if vectorFitness[i] != vectorFitness[i + 1]:
                    contadorDiferencias = contadorDiferencias + 1

            if contadorDiferencias == 0:
                break

        return vectorFitness[0]  #Retornamos solo el [0] porque todos tienen el mismo valor de fitness


    def cruceDeOrden(self, padre1, padre2):
        ptoCruce1 = 0
        ptoCruce2 = 0
        while ptoCruce1 == ptoCruce2:
            ptoCruce1 = random.randrange(1, len(padre1))
            ptoCruce2 = random.randrange(1, len(padre1))
            if ptoCruce1 > ptoCruce2:
                aux = ptoCruce1
                ptoCruce1 = ptoCruce2
                ptoCruce2 = aux
        hijo1 = []
        hijo2 = []
        for i in range(len(padre1)):
            hijo1.append('-')
            hijo2.append('-')
        aux1 = []  #vector auxiliar para guardar los elementos del cruce del padre contrario
        aux2 = []
        for i in range(ptoCruce1, ptoCruce2):
            aux1.append(padre1[i])
            aux2.append(padre2[i])
            hijo1[i] = padre1[i]
            hijo2[i] = padre2[i]
        contador1 = ptoCruce2
        contador2 = ptoCruce2
        for i in range(ptoCruce2, len(padre1)):
            if padre2[i] not in hijo1:
                hijo1[contador1] = padre2[i]
                contador1 = contador1 + 1
            if contador1 == len(padre1):
                contador1 = 0
            if padre1[i] not in hijo2:
                hijo2[contador2] = padre1[i]
                contador2 = contador2 + 1
            if contador2 == len(padre2):
                contador2 = 0
        for i in range(ptoCruce2):
            if padre2[i] not in hijo1:
                hijo1[contador1] = padre2[i]
                contador1 = contador1 + 1
            if contador1 == len(padre1):
                contador1 = 0
            if padre1[i] not in hijo2:
                hijo2[contador2] = padre1[i]
                contador2 = contador2 + 1
            if contador2 == len(padre1):
                contador2 = 0
        return hijo1, hijo2


    def conseguirPadresDuplicacionHijos(self, poblacion, vectorFitness):
            norm = 0.0   #para normalizar
            fitnessNormalizado = []
            for i in range(len(vectorFitness)):
                norm = norm + 1.0 / vectorFitness[i]
            for i in range(len(vectorFitness)):
                fitnessNormalizado.append((1.0 / vectorFitness[i])/norm)

            #Seleccion de padres
            matrizPadres = []   #sera de cantidadIndividuos x productosPorOrden
            for i in range(self.cantidadIndividuos):
                valorRandom = random.randrange(1000) / 1000.0
                variableAuxiliar = 0
                for j in range(self.cantidadIndividuos):
                    variableAuxiliar = variableAuxiliar + fitnessNormalizado[j]
                    if valorRandom < variableAuxiliar:
                        matrizPadres.append(poblacion[j])
                        break
            return matrizPadres



    def generarPadresDuplicacionHijos(self, matrizPadres, seleccion):
        matrizTotalHijos = []
        for i in range( len(matrizPadres) - 1):
            hijo1 , hijo2 = self.cruceDeOrden(matrizPadres[i], matrizPadres[i+1])
            matrizTotalHijos.append(hijo1)
            matrizTotalHijos.append(hijo2)

        nuevosPadres = seleccion(matrizTotalHijos)
        return nuevosPadres

    def conseguirPadresMejoresPadres(self, poblacion, vectorFitness):
        matrizMejoresPadres = []
        for i in range( int(len(poblacion)/2) ):
            indice = vectorFitness.index(min(vectorFitness))
            matrizMejoresPadres.append(poblacion[indice])
            vectorFitness[indice] = max(vectorFitness) + 1
        return matrizMejoresPadres


    def generarPadresMejoresPadres(self, matrizPadres, cantidadTotal):
        i = 0
        while len(matrizPadres) < cantidadTotal:
            if i + 1 < len(matrizPadres):
                hijo1 , hijo2 = self.cruceDeOrden(matrizPadres[i], matrizPadres[i+1])
                matrizPadres.append(hijo1)
                if len(matrizPadres) == cantidadTotal:
                    break
                matrizPadres.append(hijo2)

            if i + 1 == len(matrizPadres):
                hijo1 , hijo2 = self.cruceDeOrden(matrizPadres[i], matrizPadres[0])
                matrizPadres.append(hijo1)
                if len(matrizPadres) == cantidadTotal:
                    break
                matrizPadres.append(hijo2)
            i = i + 1
        return matrizPadres




    def cruce(self, poblacion, vectorFitness, seleccion):
        matrizPadres = self.conseguirPadresMejoresPadres(poblacion, vectorFitness)
        nuevosPadres = self.generarPadresMejoresPadres(matrizPadres, len(poblacion))
        # matrizPadres = self.conseguirPadresDuplicacionHijos(poblacion, vectorFitness)
        # nuevosPadres = self.generarPadresDuplicacionHijos(matrizPadres, seleccion)
        return nuevosPadres


    def mutacion(self, matrizPadres):
        probabilidad = 0.5 #probabilidad de que ocurra una mutacion
        for i in range(len(matrizPadres)):
            if random.randrange(100)/100.0 < probabilidad:
                index1 = random.randrange(len(matrizPadres[i]))
                index2 = random.randrange(len(matrizPadres[i]))
                aux = matrizPadres[i][index1]
                matrizPadres[i][index1] = matrizPadres[i][index2]
                matrizPadres[i][index2] = aux
        return matrizPadres


    def seleccionarMejorOrden(self, matrizTotalHijos):
        matrizHijosCeroUno = self.convertirCeroUno(matrizTotalHijos)
        vectorUtilidad = self.fitnessManhattan(self.matrizAlmacen, matrizHijosCeroUno) #matrizTotalHijos Ordenes
        matrizNuevosPadres = []
        for i in range(self.cantidadIndividuos):
            index = vectorUtilidad.index(min(vectorUtilidad))
            vectorUtilidad[index] = max(vectorUtilidad) + 1
            matrizNuevosPadres.append(matrizTotalHijos[index])

        return matrizNuevosPadres


    def seleccionarMejorAlmacen(self, matrizTotalHijos):
        valorFitnessTotal = 0
        vectorFitnessTotal = []
        for i in range (len(matrizTotalHijos)):
            for j in range (len(self.matrizOrdenes)):
                valorFitnessTotal = valorFitnessTotal + self.fitnessOrden(matrizTotalHijos[i], self.matrizOrdenes[j], self.cantidadIndividuos)
            vectorFitnessTotal.append(valorFitnessTotal)  #genera un vector de (cantidadIndividuos*2 -2) porque los dos ultimos no se aparean
            valorFitnessTotal = 0

        matrizNuevosPadres = []
        for i in range(self.cantidadIndividuos):
            index = vectorFitnessTotal.index(min(vectorFitnessTotal))
            vectorFitnessTotal[index] = max(vectorFitnessTotal) + 1
            matrizNuevosPadres.append(matrizTotalHijos[index])
        return matrizNuevosPadres


    def convertirCeroUno(self, matriz):
        cantidadAlmacen = len(self.almacenActual)
        matrizCeroUno = []
        vectorAuxiliar = []
        for i in range(len(matriz)):
            for j in range(cantidadAlmacen):
                vectorAuxiliar.append(0)
            matrizCeroUno.append(vectorAuxiliar)
            vectorAuxiliar = []

        for i in range(len(matrizCeroUno)):
            for j in range(len(matriz[i])):
                matrizCeroUno[i][matriz[i][j] - 1] = 1

        return matrizCeroUno



def main():
    maximoIteraciones = 50
    cantidadAlmacen = 32
    cantidadOrdenes = 10
    cantidadIndividuos = 20
    productosPorOrden = 5
    vectorProductos = []
    #vectorOrdenes = []

    utilidadMejorAlmacen = 0;
    distribucionMejorAlmacen = []
    vectorMejoresUtilidades = []

    for i in range(cantidadAlmacen):   #generamos matriz de productos para base de individuos
        vectorProductos.append(i + 1)

    #creamos objetos de GA
    AGAlmacen = AlgoritmoGenetico()
    AGOrden = AlgoritmoGenetico()
    #generador de Individuos de almacen y de ordenes POBLACION
    matrizProductos, matrizOrdenes = AGAlmacen.iniciarAlmacen(vectorProductos,cantidadIndividuos, cantidadOrdenes)

    #COMENTAR EN CASO DE QUERER USAR VALORES ALEATORIOS
    matrizOrdenes = [[1,0,1,0,0,0,1,0,1,0,1,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,1,1,1],[1,0,1,1,0,0,1,0,1,0,1,0,1,0,0,0,0,0,0,1,0,1,1,0,0,0,0,0,0,1,1,0],[1,0,0,0,0,0,0,0,1,0,1,0,0,1,1,1,1,0,0,1,1,1,1,0,0,1,0,0,0,0,0,1],[1,0,0,0,0,0,0,0,1,0,1,0,0,1,1,1,1,0,0,1,1,1,1,0,0,1,0,0,0,0,0,1]]

    contador = 0
    vectorUtilidadTotal = []
    vectorIteracion = []
    while True:
        #SEGUNDO GA
        valorFitnessTotal = 0
        vectorFitnessTotal = []
        for i in range (len(matrizProductos)):
            for j in range (len(matrizOrdenes)):
                valorFitnessTotal = valorFitnessTotal + AGOrden.fitnessOrden(matrizProductos[i], matrizOrdenes[j], cantidadIndividuos)
            vectorFitnessTotal.append(valorFitnessTotal)  #genera un vector de (cantidadIndividuos)
            valorFitnessTotal = 0

        print(vectorFitnessTotal)

        ######BUSCAR LA MEJOR UTILIDAD EN TODOS LOS PUNTOS########
        if contador == 0:
            utilidadMejorAlmacen = min(vectorFitnessTotal)
            index = vectorFitnessTotal.index(min(vectorFitnessTotal))
            distribucionMejorAlmacen = AGAlmacen.convertirAlmacenMatriz(matrizProductos[index])
        else:
            if min(vectorFitnessTotal) < utilidadMejorAlmacen:
                utilidadMejorAlmacen = min(vectorFitnessTotal)
                index = vectorFitnessTotal.index(min(vectorFitnessTotal))
                distribucionMejorAlmacen = AGAlmacen.convertirAlmacenMatriz(matrizProductos[index])

        vectorMejoresUtilidades.append(utilidadMejorAlmacen)
        ###############################################################


        suma = 0
        for i in range(len(vectorFitnessTotal)):
            suma = suma + vectorFitnessTotal[i]
        vectorUtilidadTotal.append(suma)

        #PRIMER GA
        nuevosPadres = AGAlmacen.cruce(matrizProductos,vectorFitnessTotal,AGAlmacen.seleccionarMejorAlmacen)
        padresMutados = AGAlmacen.mutacion(nuevosPadres)
        matrizProductos = padresMutados

        vectorIteracion.append(contador)
        contador = contador + 1
        #print(contador)


        if (contador == maximoIteraciones):
            break


    print ("Mejor utilidad alcanzada:")
    print (utilidadMejorAlmacen)

    print ("Mejor almacen:")
    for i in distribucionMejorAlmacen:
        print (i)


    for i in range (len (vectorUtilidadTotal)):
        vectorUtilidadTotal[i] = vectorUtilidadTotal[i] / cantidadIndividuos
    # print("Vector Utilidad Total:",vectorUtilidadTotal)
    fig = plt.figure()
    plt.plot(vectorIteracion,vectorUtilidadTotal, 'b')
    plt.show()

    fig2 = plt.figure()
    plt.plot(vectorIteracion,vectorMejoresUtilidades,'r')
    plt.show()

if __name__ == '__main__':
    main()
