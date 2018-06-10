import math
import random
from RedMLP import RedNeuronal as RN
from generarDataSet import generar
import numpy as np
from generarDataSet import funcion
import acondicionar
import pickle

def test():
    with open('training/Red.pkl', 'rb') as input:
        Red = pickle.load(input)
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
                aux[i] = (aux[i] - Red.media) / Red.desviacion

            for i in range(len(aux)):
                aux[i] = aux[i] / Red.factorData
            resultado = resultado / Red.factorSalida

            maximo = 0.8
            minimo = 0.2
            for i in range(len(aux)):
                aux[i] = (maximo - minimo) * (aux[i] + 1) / 2 + minimo
            resultado = (maximo - minimo) * (resultado + 1) / 2 + minimo

            categoria = Red.buscarSalidaRed(aux)
            # print ("Resultado Obtenido", categoria[0])

            categoriaFinal = (categoria[0] - minimo) * 2 / (maximo - minimo) - 1
            categoriaFinal = categoriaFinal * Red.factorSalida
            print ("Resultado deseado:", resultadoFinal)
            print ("Resultado Obtenido", categoriaFinal)
            errorMedio = errorMedio + (resultadoFinal - categoriaFinal) ** 2
            print ("---------------")

        errorMedio = errorMedio / validaciones
        print ("Error medio:", errorMedio)




if __name__ == '__main__':
    test()
