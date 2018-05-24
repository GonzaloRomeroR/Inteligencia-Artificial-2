import random
import math #para las funciones de activacion
#------------------------------------------------------------------------------------------------------------------------------------
class Neurona:

    def __init__(self,numeroPesos, funcionActivacion):
        self.pesos = []   #pesos sinapticos
        self.funcionActivacion = funcionActivacion;
        for i in range(numeroPesos):
            self.pesos.append(random.randrange(-1000,1000)/1000.0)
        self.sesgo = random.randrange(-1000,1000)/1000.0


    def actulizarNeurona(self):
        pass


    def funcionSigmoidal(self,x):
        salida = math.tanh(x)
        return salida


    def funcionLineal(self,x):
        self.pendiente = 1/100
        salida = self.pendiente * x
        return salida

    def calculoSalida(self,data):
        #regla de propagacion
        reglaPropagacion = 0
        for i in range(len(data)):
            reglaPropagacion = reglaPropagacion + data[i]*self.pesos[i]
        reglaPropagacion = reglaPropagacion - self.sesgo

        #funcion activacion
        if(self.funcionActivacion=='sigmoidal'):
            self.salida = self.funcionSigmoidal(reglaPropagacion)

        if(self.funcionActivacion=='lineal'):
            self.salida = self.funcionLineal(reglaPropagacion)

        # print("-----------------------------------------")
        # print("Entradas:",data)
        # print("Pesos:",self.pesos)
        # print("Sesgo:",self.sesgo)
        # print("Salida:",self.salida)
        return self.salida


#------------------------------------------------------------------------------------------------------------------------------------
class Capa:

    def __init__(self,tamanoCapa,tamanoCapaAnterior,funcionActivacion):  #recibe el tamano de la capa "actual" y la anterior
        self.numeroPesos = tamanoCapaAnterior
        self.numeroNeuronas = tamanoCapa
        self.funcionActivacion = funcionActivacion
        self.neuronas = []
        for i in range(self.numeroNeuronas):
            neurona = Neurona(self.numeroPesos, funcionActivacion)
            self.neuronas.append(neurona)


    def calcularSalida(self,data):
        self.entradaCapa = data;  #es equivalente a decir la salida anterior
        self.salidas = []
        for i in range(len(self.neuronas)):
            self.salidas.append(self.neuronas[i].calculoSalida(data))
        return self.salidas


    def actualizarCapaFinal(self, salidaDeseada, ritmoAprendizaje):   #salidaActualizacion es la salida de la capa de la derecha
        self.pesosAnteriores = []
        self.deltas = []   #capa final
        for i in range(len(self.neuronas)):
            #delta
            if (self.funcionActivacion == 'sigmoidal'):
                delta = (salidaDeseada[i] - self.salidas[i]) * (1 - self.salidas[i])   #auxiliar
            if (self.funcionActivacion == 'lineal'):
                delta = (salidaDeseada[i] - self.salidas[i]) * (self.neuronas[i].pendiente)
            self.deltas.append(delta)
            #variacion
            variacionSesgo = ritmoAprendizaje * delta * -1  #porque la "entrada" del sesgo es una neurona virtual con peso -1
            variacionPesos = []
            for j in range(len(self.entradaCapa)):
                variacionPesos.append(ritmoAprendizaje * delta * self.entradaCapa[j])

            #Actualizacion de sesgo y pesos
            self.neuronas[i].sesgo = self.neuronas[i].sesgo + variacionSesgo
            for j in range(len(self.entradaCapa)):
                self.pesosAnteriores.append(self.neuronas[i].pesos[j])
                self.neuronas[i].pesos[j] = self.neuronas[i].pesos[j] + variacionPesos[j]

            # print("Nuevo sesgo CF:",self.neuronas[i].sesgo)
            # print("Nuevos pesos CF:",self.neuronas[i].pesos)


    def actualizarCapaOculta(self, deltasCA, pesosCA, ritmoAprendizaje):  #CA: capa anterior
        self.pesosAnteriores = []
        self.deltas = []
        aux = 0
        for i in range(len(self.neuronas)):
            #delta
            for j in range(len(deltasCA)):
                aux = aux + deltasCA[j] * pesosCA[j]
            if (self.funcionActivacion == 'sigmoidal'):
                aux = aux*(1 - self.salidas[i])
            if (self.funcionActivacion == 'lineal'):
                aux = aux*self.neuronas[i].pendiente
            self.deltas.append(aux)
            aux = 0
            #variacion
            variacionSesgo = ritmoAprendizaje * self.deltas[i] * -1 #porque la "entrada" del sesgo es una neurona virtual con peso -1
            variacionPesos = []
            for j in range(len(self.entradaCapa)):
                variacionPesos.append(ritmoAprendizaje * self.deltas[i] * self.entradaCapa[j])

            #Actualizacion de sesgo y pesos
            self.neuronas[i].sesgo = self.neuronas[i].sesgo + variacionSesgo
            for j in range(len(self.entradaCapa)):
                self.pesosAnteriores.append(self.neuronas[i].pesos[j])
                self.neuronas[i].pesos[j] = self.neuronas[i].pesos[j] + variacionPesos[j]

            # print("Nuevo sesgo CO:",self.neuronas[i].sesgo)
            # print("Nuevos pesos CO:",self.neuronas[i].pesos)


#------------------------------------------------------------------------------------------------------------------------------------
class RedNeuronal:

    def __init__(self, tamanoEntrada, tamanoCapaOculta, tamanoSalida, numeroCapasOcultas, funcionesActivacion, ritmoAprendizaje):
        self.tamanoEntrada=tamanoEntrada
        self.tamanoCapaOculta=tamanoCapaOculta
        self.tamanoSalida=tamanoSalida
        self.numeroCapasOcultas=numeroCapasOcultas
        self.ritmoAprendizaje = ritmoAprendizaje
        self.capas = []   #vector de capas
        for i in range(numeroCapasOcultas):
            if i==0:
                capa = Capa(tamanoCapaOculta[i],tamanoEntrada, funcionesActivacion[i])  #recibe el tamano de la capa "actual" y la anterior
                self.capas.append(capa)
            else:
                capa = Capa(tamanoCapaOculta[i],tamanoCapaOculta[i-1], funcionesActivacion[i])
                self.capas.append(capa)
        capa = Capa(tamanoSalida, tamanoCapaOculta[-1], funcionesActivacion[-1])
        self.capas.append(capa)
        #print(len(self.capas))


    def entrenar(self, data, salidaDeseada, epocas):
        for k in range(epocas):
            for j in range(len(data)):
                #Calculo de cada salida
                for i in range(len(self.capas)):
                    if i==0:
                        salidaCapaAnterior = self.capas[i].calcularSalida(data[j])
                    else:
                        salidaCapaAnterior = self.capas[i].calcularSalida(salidaCapaAnterior)

                #Actualizacion de los pesos y sesgos de la Red
                for i in range(len(self.capas)):
                    if i==0:
                        self.capas[-i-1].actualizarCapaFinal(salidaDeseada[j], self.ritmoAprendizaje)
                    else:
                        self.capas[-i-1].actualizarCapaOculta(self.capas[-i].deltas, self.capas[-i].pesosAnteriores, self.ritmoAprendizaje)


    def clasificar(self, vector):
        pass


    def buscarSalida(self, vector):
        for i in range(len(self.capas)):
            vector = self.capas[i].calcularSalida(vector)
        return vector

    def mostrarRed(self):
        for i in range(len(self.capas)):
            print("Capa: ", i)
            for j in range(len(self.capas[i].neuronas)):
                print("Neurona: ", j)
                print ("Pesos: ",self.capas[i].neuronas[j].pesos)
                print ("Sesgo: ",self.capas[i].neuronas[j].sesgo)
