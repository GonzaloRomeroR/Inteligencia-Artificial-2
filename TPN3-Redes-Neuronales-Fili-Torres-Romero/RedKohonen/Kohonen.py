import os
import numpy as np
import random

#-------------------------------------------------------------------------------
class Neurona:

    def __init__(self, cantidadPesos):
        self.ritmoInicial = 0.99  #ritmo de aprendizaje inicial -> alpha sub cero
        self.ritmoFinal = 0.01   #alpha sub f
        self.radioInicial = 0.99
        self.radioFinal = 0.01
        self.pesos = self.generarPesos(cantidadPesos)


    def generarPesos(self, cantidadPesos):    #por si usamos distintas formas de inicializar los pesos
        pesos = self.pesosAleatorios(cantidadPesos)
        return pesos

    def pesosAleatorios(self, cantidadPesos):
        pesos = []
        for i in range(cantidadPesos):
            pesos.append(random.randrange(1000)/1000.0-0.5)
        return pesos

    def actualizarNeurona(self, entradas, vecindad, t, iteraciones):
        ritmo = self.ritmoInicial + (self.ritmoFinal - self.ritmoInicial) * (t/iteraciones)
        for i in range(len(self.pesos)):
            self.pesos[i] = self.pesos[i] + ritmo * vecindad * (entradas[i][0] - self.pesos[i])

    def funcionSimilitud(self, entradas):  #distancia Euclidea
        sumatoria = 0
        for k in range(len(entradas)):
            # sumatoria = sumatoria + (self.pesos[k] + entradas[k]) ** 2      <----este seria el mas general
            sumatoria = sumatoria + (self.pesos[k] + entradas[k][0]) ** 2    #tenemos que hacerlo asi porque la data es lista de lista de lista (cada componente, a pesar de ser uno solo, esta entre corchetes)
        distanciaEuclidea = sumatoria ** 0.5
        return distanciaEuclidea

    def calcularVecindad(self, i, j, filaG, columnaG, t, tr):
        vecindad = self.funcionVecindad(i, j, filaG, columnaG, t, tr)
        return vecindad

    def funcionVecindad(self, i, j, filaG, columnaG, t , tr):
        distancia = ((i-filaG)**2 + (j-columnaG)**2) ** 0.5
        radio = self.radioInicial + (self.radioFinal - self.radioInicial)*(t/tr)
        vecindad = 0
        if distancia > radio:
            vecindad = 0
        else:
            vecindad = 1
        return vecindad

#-------------------------------------------------------------------------------
def cargarDatos():
    matrizTotal = []
    lista = []
    for archivos in os.listdir("data"):   #The method listdir() returns a list containing the names of the entries in the directory given by path
        matriz = np.load("data/" + archivos)
        lista = matriz.tolist()
        for i in lista:
            matrizTotal.append(i)
    return matrizTotal

#-------------------------------------------------------------------------------
def crearRed(filas, columnas, cantidadPesos):    #filas = i, columnas=j
    red = []
    for i in range(filas):
        aux = []
        for j in range(columnas):
            aux.append(Neurona(cantidadPesos))
        red.append(aux)
    return red

#-------------------------------------------------------------------------------
def actualizarRed(red, data, iteraciones):
    for t in range(iteraciones):
        distMinima = 10000
        filaG = '-'
        columnaG = '-'
        entrada = data[random.randrange(len(data))]
        for i in range(len(red)):
            for j in range(len(red[i])):
                # red[i][j].actualizarNeurona(data[random.randrange(len(data))])
                if abs(red[i][j].funcionSimilitud(entrada)) < distMinima:
                    distMinima = abs(red[i][j].funcionSimilitud(entrada))
                    filaG = i      #parametros de la neurona ganadora
                    columnaG = j
        for i in range(len(red)):
            for j in range(len(red[i])):
                vecindad = red[i][j].calcularVecindad(i, j, filaG, columnaG, t, iteraciones)
                red[i][j].actualizarNeurona(entrada, vecindad, t, iteraciones)

#-------------------------------------------------------------------------------
def obtenerResultado(red, entrada):
    distanciaMinima = 10000
    for i in range(len(red)):
        for j in range(len(red[i])):
            distancia = red[i][j].funcionSimilitud(entrada)
            if distancia < distanciaMinima:
                distanciaMinima = distancia
                filaG = i
                columnaG = j

    print("Neurona ganadora:",filaG,columnaG)
    print("==========================================================")
    # for i in range(len(entrada)):
    #     print(entrada[i][0]-red[filaG][columnaG].pesos[i])
    # print(entrada)
    # print('----------------------------------------------------------')
    # print(red[filaG][columnaG].pesos)

#-------------------------------------------------------------------------------
def main():
    data = cargarDatos()
    # for i in data:
    #     print(i)
    # print(len(data))  #33 (16 o 17 tornillos y 16 o 17 tuercas)
    # print(len(data[0]))  #441 componentes que representan cada tuerca o tornillo
    filasRed = 20
    columnasRed = 20
    itxNeurona = 10  #iteracion por neurona
    iteraciones = itxNeurona * filasRed * columnasRed  #iteraciones totales
    red = crearRed(filasRed, columnasRed, len(data[0]))
    actualizarRed(red, data, iteraciones)

    obtenerResultado(red, data[0])
    obtenerResultado(red, data[10])
    obtenerResultado(red, data[15])
    obtenerResultado(red, data[20])
    obtenerResultado(red, data[30])


if __name__ == '__main__':
    main()
