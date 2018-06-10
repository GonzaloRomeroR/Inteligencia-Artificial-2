from datasetPendulo import PenduloInvertido
import pickle
import matplotlib.pyplot as plt


def test():
    anguloInicial = 0.5
    velocidadInicial = -1.2
    masaCarrito = 5
    masaBarra = 1
    longitud = 0.5
    diferencialTiempo = 0.01
    pendulo = PenduloInvertido (anguloInicial,velocidadInicial,masaCarrito,masaBarra,longitud,diferencialTiempo)

    with open('training/Red.pkl', 'rb') as input:

        Red = pickle.load(input)
        h = 0
        while True:
            h = h + 1
            aux = [pendulo.angulo, pendulo.velocidad]

            for i in range(len(aux)):
                aux[i] = (aux[i] - Red.media) / Red.desviacion

            for i in range(len(aux)):
                aux[i] = aux[i] / Red.factorData

            maximo = 0.8
            minimo = 0.2
            for i in range(len(aux)):
                aux[i] = (maximo - minimo) * (aux[i] + 1) / 2 + minimo

            fuerza = Red.buscarSalidaRed(aux)

            fuerza = (fuerza[0] - minimo) * 2 / (maximo - minimo) - 1
            fuerza = fuerza * Red.factorSalida
            # print ("Resultado Obtenido", categoria[0])
            pendulo.control(fuerza)
            print (h)
            if h == 500:
                break

    fig = plt.figure()
    plt.plot(pendulo.vectorTiempo,pendulo.vectorAngulos,'r')
    plt.plot(pendulo.vectorTiempo,pendulo.vectorVelocidad)
    #plt.scatter(pendulo.vectorTiempo,pendulo.vectorAceleracion)
    plt.show()


if __name__ == '__main__':
    test()
