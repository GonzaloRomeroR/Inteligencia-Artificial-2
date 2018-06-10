import math
import random
from RedMLP import RedNeuronal as RN
from generarDataSet import generar
import numpy as np
from generarDataSet import funcion
import acondicionar
import pickle

def uploadDatabase(file):
    matrix = np.load(file)
    list = matrix.tolist()
    return (list)


def train():

    data = uploadDatabase("data/datasetPendulo.npy")
    salidaDeseada = uploadDatabase("data/etiquetasPendulo.npy")
    data, media, desviacion = acondicionar.estandarizar(data)
    data, salidaDeseada, factorData, factorSalida = acondicionar.normalizar(data, salidaDeseada)
    epocas = 15
    numeroCapasOcultas = 1
    tamanoEntrada = len(data[0])
    tamanoCapaOculta = [2]
    tamanoSalida = len(salidaDeseada[0])
    ritmoAprendizaje = 0.3
    funcionActivacion = ['sigmoidal', 'sigmoidal']
    Red = RN(tamanoEntrada, tamanoCapaOculta, tamanoSalida, numeroCapasOcultas, funcionActivacion, ritmoAprendizaje)
    Red.ingresarParametos(factorData, factorSalida, media, desviacion)
    Red.entrenar(data, salidaDeseada, epocas)

    with open('training/Red.pkl', 'wb') as output:
        pickle.dump(Red, output, pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    train()
