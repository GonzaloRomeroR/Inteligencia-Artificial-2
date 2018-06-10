import math
import random
from RedMLP import RedNeuronal as RN
from generarDataSet import generar
import numpy as np
from generarDataSet import funcion
import acondicionar

def uploadDatabase(file):
        matrix = np.load(file)
        list = matrix.tolist()
        return (list)


def main():

    data = uploadDatabase("data/dataset.npy")
    salidaDeseada = uploadDatabase("data/etiquetas.npy")
    data, media, desviacion = acondicionar.estandarizar(data)
    data, salidaDeseada, factorData, factorSalida = acondicionar.normalizar(data, salidaDeseada)
    print (data[0])
    print (factorData)
    print (salidaDeseada[0])
    print (factorSalida)

    epocas = 15
    numeroCapasOcultas = 1
    tamanoEntrada = len(data[0])
    tamanoCapaOculta = [5]
    tamanoSalida = len(salidaDeseada[0])
    ritmoAprendizaje = 0.3
    funcionActivacion = ['sigmoidal', 'sigmoidal']
    Red = RN(tamanoEntrada, tamanoCapaOculta, tamanoSalida, numeroCapasOcultas, funcionActivacion, ritmoAprendizaje)
    Red.entrenar(data, salidaDeseada, epocas)


    validaciones = 100
    errorMedio = 0
    for i in range (validaciones):
        aux = []
        for j in range(5):
            aux.append(random.randrange(-1000, 1000)/1000.0 )
        # print (aux)
        resultadoFinal = funcion(aux)
        resultado = funcion(aux)

        for i in range(len(aux)):
            aux[i] = (aux[i] - media) / desviacion

        for i in range(len(aux)):
            aux[i] = aux[i] / factorData
        resultado = resultado / factorSalida

        maximo = 0.8
        minimo = 0.2
        for i in range(len(aux)):
            aux[i] = (maximo - minimo) * (aux[i] + 1) / 2 + minimo
        resultado = (maximo - minimo) * (resultado + 1) / 2 + minimo

        categoria = Red.buscarSalidaRed(aux)
        # print ("Resultado Obtenido", categoria[0])

        categoriaFinal = (categoria[0] - minimo) * 2 / (maximo - minimo) - 1
        categoriaFinal = categoriaFinal * factorSalida
        print ("Resultado deseado:", resultadoFinal)
        print ("Resultado Obtenido", categoriaFinal)
        errorMedio = errorMedio + (resultadoFinal - categoriaFinal) ** 2
        print ("---------------")

    errorMedio = errorMedio / validaciones
    print ("Error medio:", errorMedio)




if __name__ == '__main__':
    main()
