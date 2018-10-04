########################################
###Datos necesarios de entrada: LAeq,T, LCeq,T, LAIeq,T
###
###
#########################################

import sys
import datetime
import math


# Calculamos la correcion de tipo TONAL.
def calc_Kt():
    print("Introduce nivel del tono emergente")
    Lf = int(input())
    print("Introduce la frecuencia del tono emergente")
    Lf_frecuency = int(input())
    print("Introduce nivel de la banda derecha")
    LsRight = int(input())
    print("Introduce nivel de la banda izquierda")
    LsLeft = int(input())
    #Se calcula la media del nivel de las bandas adyacentes.
    Ls = (LsRight+LsLeft)/2

    if Lf_frecuency >= 20 and Lf_frecuency <= 125:
            if Lf - Ls < 8:
                Lt = 0
            elif Lf - Ls >= 8 and Lf - Ls <= 12:
                Lt = 3
            elif Lf - Ls > 12:
                Lt = 6
    elif Lf_frecuency > 125  and Lf_frecuency <= 400:
            if Lf - Ls < 5:
                Lt = 0
            elif Lf - Ls >= 5 and Lf - Ls <= 8:
                Lt = 3
            elif Lf - Ls > 8:
                Lt = 6
    elif Lf_frecuency > 400 and Lf_frecuency <= 10000:
            if Lf - Ls < 3:
                Lt = 0
            elif Lf - Ls >= 3 and Lf - Ls <= 5:
                Lt = 3
            elif Lf - Ls > 5:
                Lt = 6
    return Lt
# Calcula la correcion de tipo BAJA FRECUENCIA.
def calc_Kf(LCeq, LAeq):
    if LCeq - LAeq <= 10:
        Lf = 0
    elif LCeq - LAeq > 10 and LCeq - LAeq <= 15:
        Lf = 3
    elif LCeq - LAeq > 15:
        Lf = 6

    return Lf
# Calcula la correcion del tipo IMPULSIVIDAD.
def calc_Ki(LAIeq, LAeq):
    if LAIeq - LAeq <= 10:
        Li = 0
    elif LAIeq - LAeq > 10 and LAIeq - LAeq <= 15:
        Li = 3
    elif LAIeq - LAeq > 15:
        Li = 6

    return Li

# Comprueba que el maximo de las correcciones sea 9dB
def Check_Max_Correction(Kt, Kf, Ki):
    if Kt + Kf + Ki > 9:
        return 9
    else:
        return Kt + Kf + Ki

def restar_hora(hora1,hora2):
    formato = "%H:%M:%S"
    h1 = datetime.datetime.strptime(hora1, formato)
    h2 = datetime.datetime.strptime(hora2, formato)
    resultado = h2 - h1
    return str(resultado)

#Correcion del Leq por ruido de fondo LeqF representa el Lequivalente de fondo
def Calc_Background_Noise(Leq, LeqF):
    difLeq = Leq- LeqF
    if difLeq >= 15:
        return Leq
    else:
        Leq = (10*(math.log10((10**(Leq/10))-(10**(LeqF/10)))))
        return Leq

if __name__ == "__main__":

    #Recoge los valores LAeq, LCeq y LAIeq por comando.
    print("Bienvenido a la Herramienta de conformidad respecto a inspecion de actividades del RD1367")
    print("Introduzca el Nivel equivalente ponderado A de la medida")
    _LAeq = float(input())
    print("Introduzca el Nivel equivalente ponderado C de la medida")
    _LCeq = float(input())
    print("Introduzca el Nivel equivalente ponderado A con la constante temporal impulsivo (I)")
    _LAIeq = float(input())

    #Recoge los valores LAeq, LCeq y LAIeq de ruido de fondoself.
    print("Ahora debe introducir los valores de las emisiones por ruido de fondo")
    print("Introduzca el Nivel equivalente ponderado A de la medida")
    _LAeqF = float(input())
    print("Introduzca el Nivel equivalente ponderado C de la medida")
    _LCeqF = float(input())
    print("Introduzca el Nivel equivalente ponderado A con la constante temporal impulsivo (I)")
    _LAIeqF = float(input())

    #Recogida de tiempo de medidasself.
    print("Introduzca hora exacta(HH:mm:ss) del comienzo de la medida")
    h1 = input()
    print("Introduzca hora exacta(HH:mm:ss) del final de la medida")
    h2 = input()
    tiempo_medida = restar_hora(h1, h2)

    #Calcular ruido de fondo
    _LAeq = Calc_Background_Noise(_LAeq, _LAeqF)
    _LCeq = Calc_Background_Noise(_LCeq, _LCeqF)
    _LAIeq = Calc_Background_Noise(_LAIeq, _LAIeqF)

    #Calculos de las correcciones.
    print("¿Hay correcion tonal? s/n")
    if input() == "s":
        Kt = calc_Kt()
    else:
        Kt = 0
    Kf = calc_Kf(_LCeq, _LAeq)
    Ki = calc_Ki(_LAIeq, _LAeq)

    T_Correction = Check_Max_Correction(Kt, Kf, Ki)

    _LAeqK = math.trunc(_LAeq + T_Correction + 0.5)
    print("LAeqk Total: ", _LAeqK, "dBA")
