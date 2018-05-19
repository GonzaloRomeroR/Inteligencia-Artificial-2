import os
import numpy as np
import random
import math

class Neurona:

    def pesosAleatorios(self, cantidadPesos):
        pesos = []
        for i in range(cantidadPesos):
            pesos.append(random.randrange(1000) / 1000.0 - 0.5)
        return pesos


    def generarPesos(self, cantidadPesos):
        pesos = self.pesosAleatorios(cantidadPesos)
        return pesos

    def __init__(self, cantidadPesos):
        self.RadioInicial = 0.99
        self.RadioFinal = 0.01
        self.ritmoInicial = 0.99
        self.ritmoFinal = 0.01
        self.pesos = self.generarPesos(cantidadPesos)

    def actualizarNeurona(self, vecindad, entrada, t, tr):
        ritmo = self.ritmoInicial + (self.ritmoFinal - self.ritmoInicial) * (t / tr)
        for i in range(len(self.pesos)):
            self.pesos[i] = self.pesos[i] * ritmo * vecindad * (entrada[i][0] - self.pesos[i])

    def funcionSimilitud(self, entradas):
        sumatoria = 0
        for k in range(len(entradas)):
            sumatoria = sumatoria + (self.pesos[k] - entradas[k][0]) ** 2
        d = sumatoria ** 0.5
        return d

    def funcionVecindad(self, i, j, filaG, columnaG, t, tr):
        distancia = ((i - filaG) ** 2 + (j -columnaG) ** 2) ** 0.5
        radio = self.RadioInicial + (self.RadioFinal - self.RadioInicial) * (t / tr)
        vecindad = 0
        if distancia > radio:
            vecindad = 0
        else:
            vecindad = 1
        return vecindad


    def calcularVecindad(self, i, j, filaG, columnaG, t, tr):
        vecindad = self.funcionVecindad(i, j, filaG, columnaG, t, tr)
        return vecindad



def crearRed(filas, columnas, cantidadPesos):
    red = []
    for i in range(filas):
        aux = []
        for j in range(columnas):
            aux.append(Neurona(cantidadPesos))
        red.append(aux)
    return red


def cargarDatos():
    matrizTotal = []
    lista = []
    for archivos in os.listdir("data"):
        matriz = np.load("data/" + archivos)
        lista = matriz.tolist()
        for i in lista:
            matrizTotal.append(i)
    return (matrizTotal)

def actualizarRed(red, data, iteraciones):
    for t in range(iteraciones):
        distanciaMinima = 10000
        filaG = '-'
        columnaG = '-'
        entrada = data[random.randrange(len(data))]
        for i in range(len(red)):
            for j in range(len(red[i])):
                if abs(red[i][j].funcionSimilitud(entrada)) < distanciaMinima:
                    distanciaMinima = abs(red[i][j].funcionSimilitud(entrada))
                    filaG = i
                    columnaG = j

        for i in range(len(red)):
            for j in range(len(red[i])):
                vecindad = red[i][j].calcularVecindad(i, j, filaG, columnaG, t, iteraciones)
                red[i][j].actualizarNeurona(vecindad, entrada, t, iteraciones)

def obtenerValor(red, vector):
    minimo = 10000
    for i in range(len(red)):
        for j in range(len(red[i])):
            print (red[i][j].funcionSimilitud(vector))
            if abs(red[i][j].funcionSimilitud(vector)) < minimo:
                minimo = abs(red[i][j].funcionSimilitud(vector))
                filaG = i
                columnaG = j
    return filaG, columnaG






def main():
    itxNeurona = 1
    filasRed = 20
    columnasRed = 20
    iteraciones = itxNeurona * filasRed * columnasRed
    data = cargarDatos()
    red = crearRed(filasRed, columnasRed, len(data[0]))
    actualizarRed(red, data, iteraciones)
    print(obtenerValor(red, data[0]))
    print(obtenerValor(red, data[10]))
    print(obtenerValor(red, data[15]))
    print(obtenerValor(red, data[20]))
    print(obtenerValor(red, data[30]))


if __name__ == '__main__':
    main()
