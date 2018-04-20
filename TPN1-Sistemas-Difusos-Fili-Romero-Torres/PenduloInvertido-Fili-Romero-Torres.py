from math import sin
from math import cos
import matplotlib.pyplot as plt
import math
import time
import os
class PenduloInvertido:

    def __init__(self,anguloInicial,velocidadInicial,masaCarrito,masaBarra,longitud,diferencialTiempo):

        self.angulo = anguloInicial
        self.velocidad = velocidadInicial
        self.masaCarrito = masaCarrito
        self.masaBarra = masaBarra
        self.longitud = longitud
        self.aceleracion = 0
        self.gravedad = 9.8
        self.dt = diferencialTiempo
        self.sumaTiempo = 0
        self.vectorAngulos = []
        self.vectorVelocidad = []
        self.vectorAceleracion = []
        self.vectorTiempo = []

    def mostrarValores(self):
        print ("Angulo: %f" % self.angulo)
        print ("Velocidad: %f" % self.velocidad)

    def control(self, fuerza):
        self.vectorTiempo.append(self.sumaTiempo)
        self.sumaTiempo = self.sumaTiempo + self.dt
        self.calcularAceleracion(fuerza)
        self.calcularVelocidad()
        self.calcularPosicion()
        return self.angulo, self.velocidad

    def calcularAceleracion(self,fuerza):
        #print("Fuerza: %f" % fuerza)
        auxiliar = self.gravedad * sin(self.angulo) + cos(self.angulo) * ((-fuerza- self.masaCarrito * self.longitud* self.velocidad **  2 * sin(self.angulo)) /(self.masaBarra + self.masaCarrito))
        auxiliar2 = self.longitud * (4/3 - (self.masaBarra * cos(self.angulo) ** 2 / (self.masaBarra + self.masaCarrito)))
        self.aceleracion=auxiliar/auxiliar2
        self.vectorAceleracion.append(self.aceleracion)
        #print ("Aceleracion: %f" % self.aceleracion)

    def calcularVelocidad(self):
        self.velocidad = self.velocidad + self.aceleracion * self.dt
        self.vectorVelocidad.append(self.velocidad)

    def calcularPosicion(self):
        self.angulo = self.angulo + self.velocidad * self.dt + 1/2 * self.aceleracion * self.dt ** 2
        self.vectorAngulos.append(self.angulo)

    def getAngulo(self):
        return self.angulo

    def getVelocidad(self):
        return self.velocidad

class Borrosificador:

    def __init__(self):
        pass

    def funcionTriangular(self,inicio,centro,fin,x):
        if x < inicio:
            return 0
        if (x >= inicio) and (x <= centro):
            return (x - inicio)/(centro - inicio)
        if (x >= centro) and (x <= fin):
            return (fin - x)/(fin - centro)
        if x > fin:
            return 0

    def calculoPertenenciaAngulo( self, angulo ):

        NG = self.funcionTriangular(-5*math.pi/4 ,-math.pi/2, -math.pi/4, angulo)
        NP = self.funcionTriangular(-math.pi/2 , -math.pi/4, 0 ,angulo)
        Z = self.funcionTriangular(-math.pi/4 , 0, math.pi/4 ,angulo)
        PP = self.funcionTriangular( 0, math.pi/4 , math.pi/2,angulo)
        PG = self.funcionTriangular(math.pi/4 , math.pi/2, 5*math.pi/4,angulo)
        perteneciasAngulo = {"NG":NG ,"NP":NP, "Z":Z, "PP":PP, "PG":PG}
        return perteneciasAngulo

    def calculoPertenenciaVelocidad( self, velocidad ):

        NG=self.funcionTriangular(-1.5 ,-1, -0.5, velocidad)
        NP=self.funcionTriangular(-1 , -0.5, 0 ,velocidad)
        Z=self.funcionTriangular(-0.5 , 0, 0.5 ,velocidad)
        PP=self.funcionTriangular( 0, 0.5 , 1,velocidad)
        PG=self.funcionTriangular(0.5 , 1, 1.5,velocidad)
        perteneciasVelocidad={"NG":NG ,"NP":NP, "Z":Z, "PP":PP, "PG":PG}
        return perteneciasVelocidad


class MotorInferencia:
    def __init__(self):
        self.base = BaseReglas()
        self.matrizBase = self.base.getReglas()
        self.fuerzaBase = 250.0

    def calcularMatrizCentros(self):

        self.matrizCentros = []
        for i in range(len(self.matrizBase[0])):
            auxiliar = []
            for j in range(len(self.matrizBase[0])):
                auxiliar.append(0)
            self.matrizCentros.append(auxiliar)
            auxiliar = []


        for i in range(len(self.matrizBase[0])):
            for j in range(len(self.matrizBase[0])):
                if self.matrizBase[i][j] == "Z":
                    self.matrizCentros[i][j] = 0 * self.fuerzaBase
                elif self.matrizBase[i][j] == "PP":
                    self.matrizCentros[i][j] = 1 * self.fuerzaBase
                elif self.matrizBase[i][j] == "PG":
                    self.matrizCentros[i][j] = 2 * self.fuerzaBase
                elif self.matrizBase[i][j] == "NP":
                    self.matrizCentros[i][j] = -1 * self.fuerzaBase
                elif self.matrizBase[i][j] == "NG":
                    self.matrizCentros[i][j] = -2 * self.fuerzaBase
        return self.matrizCentros


    def calcularMatrizMinimos(self,diccionarioAngulos,diccionarioVelocidades):
        self.valores = ["NG", "NP", "Z", "PP", "PG"]


        self.matrizMinimos = []
        for i in range(len(self.matrizBase[0])):
            auxiliar = []
            for j in range(len(self.matrizBase[0])):
                auxiliar.append(0)
            self.matrizMinimos.append(auxiliar)
            auxiliar = []

        for i in range(len(self.valores)):
            for j in range(len(self.valores)):
                self.matrizMinimos[i][j] = min(diccionarioVelocidades[self.valores[i]],diccionarioAngulos[self.valores[j]])

        return self.matrizMinimos



class BaseReglas:

    def __init__(self):
        # Filas velocidad, columnas angulo
        self.matriz = [["NG","NG","NP","NP","NP"], ["NG","NP","NP","NP","Z"],
            ["NP","NP","Z","PP","PP"],["Z","PP","PP","PP","PG"],["PP","PP","PP","PG","PG"]]

    def getReglas(self):
        return self.matriz

class Desborrosificador:

    def __init__(self):
        pass

    def calcularFuerza(self, matrizCentros, matrizMinimos):
        self.matrizCentros = matrizCentros
        self.matrizMinimos = matrizMinimos
        self.sumaNumerador = 0
        self.sumaDenominador = 0
        for i in range(len(matrizCentros[0])):
            for j in range(len(matrizCentros[0])):
                self.sumaNumerador = self.sumaNumerador + float(self.matrizCentros[i][j]) * float(self.matrizMinimos[i][j])
                self.sumaDenominador = self.sumaDenominador + self.matrizMinimos[i][j]


        self.fuerza = self.sumaNumerador/self.sumaDenominador
        return self.fuerza







def main():
    anguloInicial = 0.5
    velocidadInicial = -1.2
    masaCarrito = 5
    masaBarra = 1
    longitud = 0.5
    diferencialTiempo = 0.01
    pendulo = PenduloInvertido (anguloInicial,velocidadInicial,masaCarrito,masaBarra,longitud,diferencialTiempo)
    print(velocidadInicial)
    borrosificador= Borrosificador()
    base = BaseReglas()
    motor = MotorInferencia()
    desbor = Desborrosificador()
    i=0
    while True:
        i = i + 1
        #print()
        #print("NUEVA ITERACION")
        #pendulo.mostrarValores()
        perteneciaAngulo = borrosificador.calculoPertenenciaAngulo(pendulo.getAngulo())
        pertenenciaVelocidad = borrosificador.calculoPertenenciaVelocidad(pendulo.getVelocidad())
        #print ("Pertenecia Angulo:")
        #print (perteneciaAngulo)
        #print ("Pertenencia Velocidad")
        #print (pertenenciaVelocidad)
        #print(base.getReglas())
        matrizCentros = motor.calcularMatrizCentros()
        #print ("Matriz de Centros:")
        #print (matrizCentros)
        matrizMinimos = motor.calcularMatrizMinimos(perteneciaAngulo,pertenenciaVelocidad)
        #print ("Matriz de Minimos")
        #print(matrizMinimos)
        fuerza = desbor.calcularFuerza(matrizCentros,matrizMinimos)
        #print ("Fuerza: %f" % fuerza )
        pendulo.control(fuerza)
        os.system('clear')
        #pendulo.mostrarValores()
        #time.sleep(6)
        if i==1000:
            break


    fig = plt.figure()
    plt.plot(pendulo.vectorTiempo,pendulo.vectorAngulos,'r')
    plt.plot(pendulo.vectorTiempo,pendulo.vectorVelocidad)
    #plt.scatter(pendulo.vectorTiempo,pendulo.vectorAceleracion)
    plt.show()

if __name__ == '__main__':
    main()
