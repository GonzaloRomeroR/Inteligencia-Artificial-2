import random
import math
import numpy as np

def funcion(variables):
    #resultado = ((2*variables[0]+3)*(variables[1]-1))*(variables[2]-1)*math.sin(variables[3]) + variables[4]
    resultado = variables[0] + variables[1] + variables[2] + variables[3] * variables[4]

    return resultado


def generar():
    database = []
    etiquetas = []
    for i in range(2000):
        aux = []   #para poder hacer una matriz
        for j in range(5):
            aux.append(random.randrange(-10000,10000)/10000.0)
        database.append(aux)
        etiquetas.append([funcion(database[i])])
    np.save('data/database', database)
    np.save('data/etiquetas', etiquetas)

    print("Entrada 0:",database[0]," y su etiqueta:", etiquetas[0]);
    print("Entrada 1:",database[5]," y su etiqueta:", etiquetas[5]);
    print("Entrada 2:",database[30]," y su etiqueta:", etiquetas[30]);
    print("Entrada 3:",database[50]," y su etiqueta:", etiquetas[50]);
    print("Entrada 4:",database[100]," y su etiqueta:", etiquetas[100]);

    return database, etiquetas


if __name__ == '__main__':
    generar()
