from RedNeuronalClases import RedNeuronal as RN
from GenerarDataSet import generar
from GenerarDataSet import funcion
import numpy as np


def normalizar(data, salidaDeseada):
    # print("Data:",data)
    # print("SalidaDeseada:",salidaDeseada)
    maximoData = 0
    for i in range(len(data)):
        for j in range(len(data[i])):
            if abs(data[i][j]) > maximoData:
                maximoData = abs(data[i][j])
    for i in range(len(data)):
        for j in range(len(data[i])):
            data[i][j] = data[i][j]/maximoData

    maximoSalida = 0
    for i in range(len(salidaDeseada)):
        for j in range(len(salidaDeseada[i])):
            if abs(salidaDeseada[i][j]) > maximoSalida:
                maximoSalida = abs(salidaDeseada[i][j])
    for i in range(len(salidaDeseada)):
        for j in range(len(salidaDeseada[i])):
            salidaDeseada[i][j] = salidaDeseada[i][j]/maximoSalida

    # print("maximoData:",maximoData)
    print("maximoSalida:",maximoSalida)

    return data, salidaDeseada, maximoData, maximoSalida

def normalizar2(data):
    # print("Data:",data)
    # print("SalidaDeseada:",salidaDeseada)
    maximoData = 0
    for j in range(len(data)):
        if abs(data[j]) > maximoData:
            maximoData = abs(data[j])
    for j in range(len(data)):
        data[j] = data[j]/maximoData
    return data, maximoData


def uploadDatabase(file):
    matrix = np.load(file)
    list = matrix.tolist()
    return list


def main():

    #PARA GENERAR EL DATABASE
    #data, salidaDeseada = generar()
    # print(data[0], salidaDeseada[0])


    #LEER EL DATASET
    data = uploadDatabase("data/database.npy")
    salidaDeseada = uploadDatabase("data/etiquetas.npy")
    data, salidaDeseada, factorData, factorSalida = normalizar(data, salidaDeseada)


    #DATA DE PRUEBA
    # entrada = [0.8, 0.35, 0.43]
    # data = []
    # data.append(entrada)
    # # data.append(entrada)
    # # data.append(entrada)
    # # data.append(entrada)
    #
    # sal = [-1]
    # salidaDeseada = []
    # salidaDeseada.append(sal)
    # salidaDeseada.append(sal)
    # salidaDeseada.append(sal)
    # salidaDeseada.append(sal)


    #PARAMETROS DE LA RED
    epocas = 50
    numeroCapasOcultas = 1
    tamanoEntrada = len(data[0])
    tamanoCapaOculta = [10]
    tamanoSalida = 1
    funcionesActivacion = ['sigmoidal','lineal']
    ritmoAprendizaje = 0.15


    #CREO LA RED
    Red = RN(tamanoEntrada, tamanoCapaOculta, tamanoSalida, numeroCapasOcultas, funcionesActivacion, ritmoAprendizaje)


    #ENTRENAMIENTO DE LA RED
    Red.entrenar(data, salidaDeseada, epocas)
    #Red.clasificar(entrada)


    #TEST DE LA RED
#     ('Entrada 0:', [13.98, 19.38, 74.15, 10.49, 68.91], ' y su etiqueta:', [830.3759])
# ('Entrada 1:', [-69.28, -32.53, -40.32, 17.04, -89.44], ' y su etiqueta:', [-1666.1875999999997])
# ('Entrada 2:', [78.54, -62.81, 72.26, 13.91, -42.96], ' y su etiqueta:', [-509.58360000000005])
# ('Entrada 3:', [43.54, 46.34, 28.87, -86.3, -10.57], ' y su etiqueta:', [1030.941])
# ('Entrada 4:', [85.04, 69.51, 85.97, 97.27, -36.92], ' y su etiqueta:', [-3350.6884])
    entrada = [13.98, 19.38, 74.15, 10.49, 68.91]
    resultado = funcion(entrada)
    print("Resultado: ", resultado)
    # entrada, factorEntrada = normalizar2(entrada)
    print ("factorData: ", factorData,"; factorSalida:", factorSalida)
    for i in range(len(entrada)):
        entrada[i] = entrada[i] / factorData
    resultado = funcion(entrada)
    print("Resultado: ", resultado)
    salida = Red.buscarSalida(entrada)
    print("Salida NORMALIZADA de ", entrada, " es: ", salida)
    for i in range(tamanoSalida):
        salida = salida[i] * factorSalida
    print("Salida de ", entrada, " es: ", salida)

    #Red.mostrarRed()



if __name__ == '__main__':
    main()
