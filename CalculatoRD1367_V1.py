#!/usr/bin/python3
# -*- coding: utf-8 -*-
########################################
#Herramienta para calcular las correciones de los valores por emisiones según#
#el RD1367 y permite obtener la declaración de conformidad de la situación#
#Más informacón en el manual de usuario#
#######################################
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
#Correcion del Leq por ruido de fondo LeqF representa el Lequivalente de fondo
def Calc_Background_Noise(Leq, LeqF):
    difLeq = Leq - LeqF
    if difLeq >= 15:
        return Leq
    else:
        Leq = (10*(math.log10((10**(Leq/10))-(10**(LeqF/10)))))
        return Leq
#Recoge por teclado el tipo de area acústica donde se realizan las mediciones
def take_area():
    print('Ahora seleccione el tipo de área acústica donde ha realizado las mediciones:')
    print('1: Suelo uso sanitario, docente y cultural que que requiera una especial proteción contra la contaminación acústica')
    print('2: Suelo de uso residencial')
    print('3: Suelo de uso terciario distinto del contemplado en el 4')
    print('4: Suelo de uso recreativo y espectaculos')
    print('5: Suelo de uso industrial')
    area = int(input())
    return area
#Comprueba si el nivel se cumple en cada caso e imprime en pantalla el resultado
def check_value(stage, Leq):
    if stage == 1:
        Lim1 = 40 + 5
        Lim2 = 50 + 5
    if stage == 2:
        Lim1 = 45 + 5
        Lim2 = 55 + 5
    if stage == 3:
        Lim1 = 50 + 5
        Lim2 = 60 + 5
    if stage == 4:
        Lim1 = 53 + 5
        Lim2 = 63 + 5
    if stage == 5:
        Lim1 = 55 + 5
        Lim2 = 65 + 5
#A los limites establecido por la ley les sumo 5dB de margen que hay que darle según lo establecido
    if Leq > Lim1:
        print('No cumple la declaración de conformidad para periodo noche')
        if Leq > Lim2:
            print('No cumple la declaración de conformidad para periodo día y tampoco para perido tarde')
        else:
            print('Sí que cumple la declaraación de conformidad para periodo día y periodo tarde')
    else:
        print('Sí que cumple la declaración de conformidad')


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
    #Calculo el LA equivalente corregido total
    _LAeqK = math.trunc(_LAeq + T_Correction + 0.5)
    area = take_area()
    check_value(area, _LAeqK)
    print("LAeqk Total: ", _LAeqK, "dBA")
    print('Valor de correciones: ', T_Correction)
