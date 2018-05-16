import random
import math
class Neurona:

    def __init__(self, numeroPesos, funcionActivacion):
        self.pesos = []
        self.funcionActivacion = funcionActivacion
        for i in range(numeroPesos):
            self.pesos.append((random.randrange(-1000,1000)/1000.0))
        #print("Pesos")
        #print(self.pesos)
        self.sesgo = random.randrange(-1000,1000)/1000.0
        #print("Sesgos")
        #print(self.sesgo)

    def actualizarNeurona(self):
        pass

    def funcionSigmoidal(self, reglaPropagacion):
        z = math.tanh(reglaPropagacion)
        return z

    def funcionLineal():
        pass

    def calculoSalida(self, data):
        reglaPropagacion = 0
        for i in range(len(data)):
            reglaPropagacion = reglaPropagacion + data[i] * self.pesos[i]
        reglaPropagacion = reglaPropagacion - self.sesgo


        if self.funcionActivacion == "sigmoidal":
            self.salida = self.funcionSigmoidal(reglaPropagacion)

        if self.funcionActivacion == "lineal":
            pass

        return self.salida

    # def buscarSalidaNeurona(self, vector):
    #     salida = 0
    #     for i in range(len(self.pesos)):
    #         salida = salida + self.pesos[i] * vector[i]
    #     return salida



class Capa:

    def __init__(self, tamanoCapa, tamanoCapaAnterior, funcionActivacion):
        self.numeroPesos = tamanoCapaAnterior
        self.numeroNeuronas = tamanoCapa
        self.funcionActivacion = funcionActivacion
        self.neuronas = []
        for i in range(self.numeroNeuronas):
            neurona = Neurona(self.numeroPesos, funcionActivacion)
            self.neuronas.append(neurona)

    def actualizarCapaFinal(self, salidaDeseada, ritmoAprendizaje):
        self.pesosAnteriores = []
        self.deltas = []
        for i in range(len(self.neuronas)):
            if self.funcionActivacion == "sigmoidal":
                delta = (salidaDeseada[i] - self.salidas[i]) * (1 - self.salidas[i])
            if self.funcionActivacion == "lineal":
                pass
            self.deltas.append(delta)
            variacionSesgo = ritmoAprendizaje * delta * -1
            variacionPesos = []
            for j in range(len(self.entradaCapa)):
                variacionPesos.append(ritmoAprendizaje * delta * self.entradaCapa[j])

            self.neuronas[i].sesgo = self.neuronas[i].sesgo + variacionSesgo
            for j in range(len(self.entradaCapa)):
                self.pesosAnteriores.append(self.neuronas[i].pesos[j])
                self.neuronas[i].pesos[j] = self.neuronas[i].pesos[j] + variacionPesos[j]
            #print("Nuevos Parametros")
            #print(self.neuronas[i].pesos)
            #print(self.neuronas[i].sesgo)
            #print ("------------------------")

    def actualizarCapaOculta(self, deltasCA, pesosCA, ritmoAprendizaje ):
        self.pesosAnteriores = []
        self.deltas = []
        aux = 0
        for i in range(len(self.neuronas)):
            for j in range(len(deltasCA)):
                aux = aux + deltasCA[j] * pesosCA[j]

            if self.funcionActivacion == "sigmoidal":
                aux = aux * (1 - self.salidas[i])

            if self.funcionActivacion == "lineal":
                pass
            self.deltas.append(aux)

            variacionSesgo = ritmoAprendizaje * self.deltas[i] * -1
            variacionPesos = []
            for j in range(len(self.entradaCapa)):
                variacionPesos.append(ritmoAprendizaje * self.deltas[i] * self.entradaCapa[j])

            self.neuronas[i].sesgo = self.neuronas[i].sesgo + variacionSesgo
            for j in range(len(self.entradaCapa)):
                self.pesosAnteriores.append(self.neuronas[i].pesos[j])
                self.neuronas[i].pesos[j] = self.neuronas[i].pesos[j] + variacionPesos[j]
            #print("Nuevos Parametros")
            #print(self.neuronas[i].pesos)
            #print(self.neuronas[i].sesgo)
            #print ("------------------------")
            aux = 0



    def calcularSalida(self, data):
        self.entradaCapa = data
        self.salidas = []
        for i in range(len(self.neuronas)):
            self.salidas.append ( self.neuronas[i].calculoSalida(data))
        return self.salidas


    # def buscarSalidaCapa(self, vector):
    #     salidasCapa = []
    #     for i in range(len(self.neuronas)):
    #         salidasCapa.append(self.neuronas[i].buscarSalidaNeurona(vector))
    #     return salidasCapa



class RedNeuronal:

    def __init__(self, tamanoEntrada, tamanoCapaOculta, tamanoSalida, numeroCapasOcultas, funcionActivacion, ritmoAprendizaje):
        self.ritmoAprendizaje = ritmoAprendizaje
        self.tamanoEntrada = tamanoEntrada
        self.tamanoCapaOculta = tamanoCapaOculta
        self.tamanoSalida = tamanoSalida
        self.numeroCapasOcultas = numeroCapasOcultas
        self.capas = []
        for i in range(numeroCapasOcultas):
            if i == 0:
                capa = Capa(tamanoCapaOculta[i], tamanoEntrada, funcionActivacion[i])
                self.capas.append(capa)
            else:
                capa = Capa(tamanoCapaOculta[i], tamanoCapaOculta[i - 1], funcionActivacion[i])
                self.capas.append(capa)
        capa = Capa(tamanoSalida, tamanoCapaOculta[-1], funcionActivacion[-1])
        self.capas.append(capa)
        ##print (len(self.capas))

    def entrenar(self, data, salidaDeseada, epocas):
        for k in range(epocas):
            for j in range(len (data)):
                for i in range(len(self.capas)):
                    if i == 0:
                        salidaCapaAnterior = self.capas[i].calcularSalida(data[j])
                    else:
                        salidaCapaAnterior = self.capas[i].calcularSalida(salidaCapaAnterior)
                    #print(salidaCapaAnterior)
                for i in range(len(self.capas)):
                    if i == 0:
                        self.capas[-i - 1].actualizarCapaFinal(salidaDeseada[j], self.ritmoAprendizaje)
                    else:
                        self.capas[-i - 1].actualizarCapaOculta(self.capas[-i].deltas, self.capas[-i].pesosAnteriores, self.ritmoAprendizaje)

    def clasificar(self, vector):
        pass

    def buscarSalidaRed(self, vector):
        for i in range (len(self.capas)):
            vector = self.capas[i].calcularSalida(vector)
        return vector
