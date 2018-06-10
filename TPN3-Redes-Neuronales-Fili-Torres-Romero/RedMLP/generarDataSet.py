import math
import random
import numpy as np

def funcion(vector):
    #resultado = (2 * vector[0] + 3) * (vector[1] - 1) * (vector[2] - 1) * math.sin(vector[3]) + vector[4]
    resultado = vector[0] + vector[1] + vector[2] + vector[3] * vector[4]
    return resultado

def generar():
    dataset = []
    etiquetas = []
    for i in range(20000):
        aux = []
        for j in range(5):
            aux.append(random.randrange(-1000, 1000)/1000.0)
        dataset.append(aux)
        etiquetas.append([funcion(dataset[i])])
        np.save('data/dataset', dataset)
        np.save('data/etiquetas', etiquetas)
        # np.savetxt('data/dataset', dataset, delimiter=',')
        # np.savetxt('data/etiquetas', etiquetas, delimiter=',')
    return dataset, etiquetas


if __name__ == '__main__':
    generar()
