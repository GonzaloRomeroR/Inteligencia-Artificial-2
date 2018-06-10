import math
import random
from RedMLP import RedNeuronal as RN
from generarDataSet import generar
import numpy as np
from generarDataSet import funcion

def normalizar(data, salidaDeseada):
    maximoData = 0

    for i in range(len(data)):
        for j in range(len(data[i])):
            if abs(data[i][j]) > maximoData:
                maximoData = abs(data[i][j])

    for i in range(len(data)):
        for j in range(len(data[i])):
            data[i][j] = data[i][j] / maximoData


    maximoSalida = 0

    for i in range(len(salidaDeseada)):
        for j in range(len(salidaDeseada[i])):
            if abs(salidaDeseada[i][j]) > maximoSalida:
                maximoSalida = abs(salidaDeseada[i][j])


    for i in range(len(salidaDeseada)):
        for j in range(len(salidaDeseada[i])):
            salidaDeseada[i][j] = salidaDeseada[i][j] / maximoSalida

    # Transformar entradas y salidas de 0.2 a 0.8

    maximo = 0.8
    minimo = 0.2

    for i in range(len(salidaDeseada)):
        for j in range(len(salidaDeseada[i])):
            salidaDeseada[i][j] = (maximo - minimo) * (salidaDeseada[i][j] + 1) / 2 + minimo

    for i in range(len(data)):
        for j in range(len(data[i])):
            data[i][j] = (maximo - minimo) * (data[i][j] + 1) / 2 + minimo



    return data, salidaDeseada, maximoData, maximoSalida

def estandarizar(data):
    sumatoria = 0.0
    for i in range(len(data)):
        for j in range(len(data[i])):
            sumatoria = sumatoria + data[i][j]
    media = sumatoria / (len(data) * len(data[i]))

    varianza = 0.0
    for i in range(len(data)):
        for j in range(len(data[i])):
            varianza = varianza + (data[i][j] - media) ** 2
    varianza = varianza / (len(data) * len(data[i]))
    desviacion = varianza ** 0.5

    for i in range(len(data)):
        for j in range(len(data[i])):
            data[i][j] = (data[i][j] - media) / desviacion


    return data, media, desviacion
