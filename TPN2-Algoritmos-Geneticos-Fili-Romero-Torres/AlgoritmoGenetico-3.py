import random
import math

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
        #print(matrizIndividuos)
        return matrizIndividuos

    #iniciar Individuos del almacen y de las ordenes
    def iniciarAlmacen(self, vectorProductos, vectorOrdenes, cantidadIndividuos, cantidadOrdenes):
        self.vectorProductos = vectorProductos
        self.vectorOrdenes = vectorOrdenes
        self.matrizProductos = self.generarMatrizIndividuos(vectorProductos,cantidadIndividuos)
        self.matrizOrdenes = self.generarMatrizIndividuos(vectorOrdenes,cantidadOrdenes)

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
        return configuracionAlmacen


    def fitnessManhattan(self, matrizAlmacen, poblacionOrdenes):
        vectorFitness = []
        for i in range (len(poblacionOrdenes)):
            distanciaX = 0
            distanciaY = 0
            vectorFilas = []
            vectorColumnas = []
            vectorColumnas.append(0)
            vectorFilas.append(0)
            for j in range (len(poblacionOrdenes[i])):
                if poblacionOrdenes[i][j] == 1:
                    for k in range(len(matrizAlmacen)):     #filas del almacen
                        for h in range(len(matrizAlmacen[k])):  #columnas del almacen
                            if matrizAlmacen[k][h] == (j + 1) :
                                vectorFilas.append(k)
                                vectorColumnas.append(h)
                                break
            vectorColumnas.append(0)
            vectorFilas.append(0)
            for i in range (len(vectorFilas) - 1):
                distanciaX = distanciaX + abs(vectorFilas[i + 1] - vectorFilas[i] )
                distanciaY = distanciaY + abs(vectorColumnas[i + 1] - vectorColumnas[i] )

            distanciaManhattan = distanciaX + distanciaY
            vectorFitness.append(distanciaManhattan)
        return vectorFitness


    def mutacion(self, matrizPadres):
        probabilidad = 0.5
        for i in range(len(matrizPadres)):
            if random.randrange(100)/100.0 < probabilidad:
                index1 = random.randrange(len(matrizPadres[i]))
                index2 = random.randrange(len(matrizPadres[i]))
                aux = matrizPadres[i][index1]
                matrizPadres[i][index1] = matrizPadres[i][index2]
                matrizPadres[i][index2] = aux
        return matrizPadres




    def cruceDeOrden(self, padre1, padre2):
        ptoCruce1 = random.randrange(1, len(padre1))
        ptoCruce2 = random.randrange(1, len(padre1))
        if ptoCruce1 > ptoCruce2:
            aux = ptoCruce1
            ptoCruce1 = ptoCruce2
            ptoCruce2 = aux
        hijo1 = []
        hijo2 = []
        for i in range(len(padre1)):
            hijo1.append(0)
            hijo2.append(0)
        aux1 = []  #vector auxiliar para guardar los elementos del cruce del padre contrario
        aux2 = []
        for i in range(ptoCruce1,ptoCruce2):
            aux1.append(padre1[i])
            aux2.append(padre2[i])
            hijo1[i]=padre1[i]
            hijo2[i]=padre2[i]
        contador1=ptoCruce2
        contador2=ptoCruce2
        for i in range(ptoCruce2-1,len(padre1)):
            if padre2[i] not in aux2:
                hijo1[contador1]=padre2[i]
                contador1 = contador1 + 1
            if contador1 == len(padre1):
                contador1 = 0
            if padre1[i] not in aux1:
                hijo2[contador2]=padre1[i]
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



    def convertirCeroUno(self, matriz):
        cantidadAlmacen = len(self.almacenActual)
        matrizCeroUno = []
        vectorAuxiliar = []
        for i in range(len(matriz)):
            for j in range(cantidadAlmacen):
                vectorAuxiliar.append(0)
            matrizCeroUno.append(vectorAuxiliar)
            vectorAuxiliar = []

        for i in range (len(matrizCeroUno)):
            for j in range (len(matriz[i])):
                matrizCeroUno[i][matriz[i][j] - 1] = 1

        return matrizCeroUno

    def seleccionarMejor(self, matrizTotalHijos):
        matrizHijosCeroUno = self.convertirCeroUno(matrizTotalHijos)
        vectorUtilidad = self.fitnessManhattan(self.matrizAlmacen, matrizHijosCeroUno)

        matrizNuevosPadres = []

        for i in range(self.cantidadIndividuos):
            index = vectorUtilidad.index(max(vectorUtilidad))
            vectorUtilidad[index] = 0
            matrizNuevosPadres.append(matrizTotalHijos[index])

        return matrizNuevosPadres


    def cruce(self, poblacion, vectorFitness):
        #Seleccion de padres
        suma = 0.0
        fitnessNormalizado = []
        for i in range(len(vectorFitness)):
            suma = suma + vectorFitness[i]
        for i in range(len(vectorFitness)):
            fitnessNormalizado.append(vectorFitness[i]/suma)
        matrizPadres = []
        for i in range(self.cantidadIndividuos):
            valorRandom = random.randrange(1000) / 1000.0
            variableAuxiliar = 0
            for j in range(self.cantidadIndividuos):
                variableAuxiliar = variableAuxiliar + fitnessNormalizado[j]
                if valorRandom < variableAuxiliar:
                    matrizPadres.append(poblacion[j])
                    break

        matrizTotalHijos = []
        for i in range( len(matrizPadres) - 1):
            hijo1 , hijo2 = self.cruceDeOrden(matrizPadres[i], matrizPadres[i+1])
            matrizTotalHijos.append(hijo1)
            matrizTotalHijos.append(hijo2)

        nuevosPadres = self.seleccionarMejor(matrizTotalHijos)
        return nuevosPadres


    def fitnessOrden(self, almacenActual, vectorOrdenes, cantidadIndividuos):
        self.almacenActual = almacenActual
        self.vectorOrdenes = vectorOrdenes
        self.cantidadIndividuos = cantidadIndividuos
        poblacionOrdenes = self.generarMatrizIndividuos(vectorOrdenes, cantidadIndividuos)
        self.matrizAlmacen = self.convertirAlmacenMatriz(almacenActual)
        vectorFitness = self.fitnessManhattan(self.matrizAlmacen, poblacionOrdenes)

        poblacion = []
        vectorAuxiliar = []
        for i in range(len(poblacionOrdenes)):
            for j in range(len(poblacionOrdenes[i])):
                if poblacionOrdenes[i][j] == 1:
                    vectorAuxiliar.append(j + 1)
            poblacion.append(vectorAuxiliar)
            vectorAuxiliar = []


        contador = 0

        while True:
            vectorFitness = self.fitnessManhattan(self.matrizAlmacen, self.convertirCeroUno(poblacion))
            nuevosPadres = self.cruce(poblacion, vectorFitness)
            padresMutados = self.mutacion(nuevosPadres)
            poblacion = padresMutados

            contador = contador + 1

            if contador == 500:
                print ("Las iteraciones han excedido el valor maximo")
                break

            contadorDiferencias = 0
            for i in range (len(vectorFitness) - 1):
                if vectorFitness[i] != vectorFitness[i + 1]:
                    contadorDiferencias = contadorDiferencias + 1

            if contadorDiferencias == 0:
                break

        return vectorFitness[0]



def main():

    cantidadAlmacen = 16
    cantidadOrdenes = 15
    cantidadIndividuos = 10
    productosPorOrden = 10
    vectorProductos = []
    vectorOrdenes = []
    for i in range(cantidadAlmacen):
        vectorProductos.append(i + 1)
    #print(vectorProductos)

    for i in range(cantidadAlmacen):
        if i < productosPorOrden:
            vectorOrdenes.append(1)
        else:
            vectorOrdenes.append(0)
    #print(vectorOrdenes)

    AGAlmacen = AlgoritmoGenetico()
    AGOrden = AlgoritmoGenetico()
    #generador de Individuos de almacen y de ordenes
    matrizProductos, matrizOrdenes = AGAlmacen.iniciarAlmacen(vectorProductos,vectorOrdenes,cantidadIndividuos, cantidadOrdenes)


    ############################################################################################################################
    #
    valorFitnessTotal = 0
    vectorFitnessTotal = []
    for i in range (len(matrizProductos)):
        for j in range (len(matrizOrdenes)):
            valorFitnessTotal = valorFitnessTotal + AGOrden.fitnessOrden(matrizProductos[i], matrizOrdenes[j], cantidadIndividuos)
        vectorFitnessTotal.append(valorFitnessTotal)
        valorFitnessTotal = 0
    print (vectorFitnessTotal)



if __name__ == '__main__':
    main()
