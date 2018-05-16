import math
import random

def funcion(vector):
    resultado = (2 * vector[0] + 3) * (vector[1] - 1) * (vector[2] - 1) * math.sin(vector[3]) + vector[4]
    return resultado

def generar():
    dataset = []
    etiquetas = []
    for i in range(20000):
        aux = []
        for j in range(5):
            aux.append(random.randrange(-10000, 10000)/100.0)
        dataset.append(aux)
        etiquetas.append([funcion(dataset[i])])
    return dataset, etiquetas


if __name__ == '__main__':
    generar()
