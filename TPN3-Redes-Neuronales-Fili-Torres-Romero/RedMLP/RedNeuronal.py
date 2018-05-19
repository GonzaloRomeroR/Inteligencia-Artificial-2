import math
import random
from RedMLP import RedNeuronal as RN
from generarDataSet import generar
import numpy as np

def funcion(vector):
    resultado = (2 * vector[0] + 3) * (vector[1] - 1) * (vector[2] - 1) * math.sin(vector[3]) + vector[4]
    return resultado

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

    return data, salidaDeseada, maximoData, maximoSalida

def uploadDatabase(file):
        matrix = np.load(file)
        list = matrix.tolist()
        return (list)

def main():
    ##########################################################
    # data = [[0.80, 0.35, 0.43],[0 ,0, 0], [-0.35 ,-0.8, 0.43]]
    # salidaDeseada = [[-1, 0, 0], [0, -1, 0], [0, 0, -1]]
    ##########################################################


    data, salidaDeseada = generar()
    data, salidaDeseada, factorData, factorSalida = normalizar(data, salidaDeseada)

    # data = uploadDatabase("data/dataset.npy")
    # salidaDeseada = uploadDatabase("data/etiquetas.npy")
    # data, salidaDeseada, factorData, factorSalida = normalizar(data, salidaDeseada)

    epocas = 10
    numeroCapasOcultas = 1
    tamanoEntrada = len(data[0])
    tamanoCapaOculta = [10]
    tamanoSalida = len(salidaDeseada[0])
    ritmoAprendizaje = 0.3
    funcionActivacion = ['sigmoidal', 'sigmoidal']
    Red = RN(tamanoEntrada, tamanoCapaOculta, tamanoSalida, numeroCapasOcultas, funcionActivacion, ritmoAprendizaje)
    Red.entrenar(data, salidaDeseada, epocas)

    #################################################################
    print (factorData)

    for i in range (10):
        aux = []
        for j in range(5):
            aux.append(random.randrange(-10000, 10000)/1000.0 / factorData )
        print (aux)
        categoria = Red.buscarSalidaRed(aux)
        aux2 = []
        for i in range(len(aux)):
            aux2.append(aux[i] * factorData)

        resultado = funcion(aux2)
        print ("---------------")
        print (resultado)
        print (categoria[0] * factorSalida)
    #################################################################
    Red.mostrarRed()

    ##########################################################
    # categoria = Red.buscarSalidaRed([0.80, 0.35, 0.43])
    # print (categoria)
    #
    # categoria = Red.buscarSalidaRed([0 ,0, 0])
    # print (categoria)
    #
    # categoria = Red.buscarSalidaRed([-0.35 ,-0.8, 0.43])
    # print (categoria)
    ##########################################################

if __name__ == '__main__':
    main()
