import math
import random
from RedMLP import RedNeuronal as RN
from generarDataSet import generar

def funcion(vector):
    resultado = (2 * vector[0] + 3) * (vector[1] - 1) * (vector[2] - 1) * math.sin(vector[3]) + vector[4]
    return resultado

def main():
    ##########################################################
    data = [[0.80, 0.35, 0.43],[0 ,0, 0],[-0.35 ,-0.8, 0.43]]
    salidaDeseada = [[0.9,0,0],[0,0.9,0],[0,0,0.9]]#]
    ##########################################################


    #####################################################################
    # data, salidaDeseada = generar()
    # maxData = max([sublist[-1] for sublist in data])
    # maxSalidaDeseada = max([sublist[-1] for sublist in salidaDeseada])
    # # for i in range(len(data)):
    # #     for j in range(len(data[i])):
    # #         data[i][j] = data[i][j] / maxData
    # for i in range(len(salidaDeseada)):
    #     for j in range(len(salidaDeseada[i])):
    #         salidaDeseada[i][j] = salidaDeseada[i][j] / maxSalidaDeseada
    ####################################################################


    epocas = 100
    numeroCapasOcultas = 1
    tamanoEntrada = len(data[0])
    tamanoCapaOculta = [3]
    tamanoSalida = len(salidaDeseada[0])
    ritmoAprendizaje = 0.3
    funcionActivacion = ['sigmoidal', 'sigmoidal', 'sigmoidal']
    Red = RN(tamanoEntrada, tamanoCapaOculta, tamanoSalida, numeroCapasOcultas, funcionActivacion, ritmoAprendizaje)
    #data = leerDataSet(/path/to/dataset)
    Red.entrenar(data, salidaDeseada, epocas)

    #################################################################
    # for i in range (50):
    #     aux = []
    #     for j in range(5):
    #         aux.append(random.randrange(-10000, 10000)/1000.0)
    #     resultado = funcion(aux)
    #     categoria = Red.buscarSalidaRed(aux)
    #     print ("---------------")
    #     print (resultado)
    #     print (categoria)
    #################################################################




    ##########################################################
    categoria = Red.buscarSalidaRed([0.80, 0.35, 0.43])
    print (categoria)

    categoria = Red.buscarSalidaRed([0 ,0, 0])
    print (categoria)

    categoria = Red.buscarSalidaRed([-0.35 ,-0.8, 0.43])
    print (categoria)
    ##########################################################

if __name__ == '__main__':
    main()
