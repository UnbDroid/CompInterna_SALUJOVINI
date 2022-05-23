#!/usr/bin/env python3
from ev3dev2.motor import *
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *
#from ev3dev.ev3 import *
from ev3dev2.console import *

#Árvore Genealógica do Reginaldo:
#Padrinho: Joshua


def segue_linha():
    preto = 30
    verde = 6
    valor_esq = sensorEsq.value()
    valor_dir = sensorDir.value()
    vmenor = 30
    vmaior = -50

    sensor_dir_valores.append(valor_dir)
    sensor_esq_valores.append(valor_esq)

    if (valor_esq < preto) and (valor_dir < preto): #ambos veem valor menor que preto
        if (sum(sensor_esq_valores[-90:])/90) <= preto: #se o esquerdo andou vendo muito preto -> vira pra direita (virada bruta)
            motores.on(SpeedPercent(vmaior),SpeedPercent(vmenor))
        elif (sum(sensor_dir_valores[-90:])/90) <= preto: #se o direito andou vendo muito preto -> vira pra esquerda (virada bruta)
            motores.on(SpeedPercent(vmenor),SpeedPercent(vmaior))
        else:
            motores.on(SpeedPercent(-10),SpeedPercent(-10))

    elif (valor_esq < preto) and (valor_dir > preto): #só esquerdo ve valor menor que preto -> dobra pra esquerda
        motores.on(SpeedPercent(vmenor),SpeedPercent(vmaior)) 

    elif (valor_esq > preto) and (valor_dir < preto): #só direito ve valor menor que preto -> dobra pra direita
        motores.on(SpeedPercent(vmaior),SpeedPercent(vmenor)) 

    else: #ambos veem valores maiores que preto
        motores.on(SpeedPercent(-25),SpeedPercent(-25))
        ''' if (sum(sensor_esq_valores[-20:])/20) <= preto: #se o esquerdo andou vendo muito preto -> vira pra direita (virada bruta)
            motores.on(SpeedPercent(vmaior),SpeedPercent(vmenor))

        elif    (sum(sensor_dir_valores[-20:])/20) <= preto: #se o direito andou vendo muito preto -> vira pra esquerda (virada bruta)
            motores.on(SpeedPercent(vmenor),SpeedPercent(vmaior))
        else: #ambos andam vendo branco'''



def leitor_cor():
    print("SensorEsquerdo = ", sensorEsq.value()) #valores esq: branco (59) // preto (10) // verde (4 - 9)
    print("SensorDireito = ", sensorDir.value()) # valores dir: branco (70) // preto (7) // verde (4) // verde é menor que 6


'''
def calibra_sensores():
    sensors.color3.onLightDetected(LightIntensityMode.Reflected, Light.Dark, function (){
        brick.showString("dark", 2)})

    sensors.color3.onLightDetected(LightIntensityMode.Reflected, Light.Bright, function ():
        brick.showString("bright", 2)
    )
    console.sendToScreen()
    console.log("move color sensor")
    console.log("over DARK and BRIGHT color")
    console.log("and stop moving when done")
    console.log("press ENTER when ready")
    brick.buttonEnter.pauseUntil(ButtonEvent.Pressed)
    sensors.color3.calibrateLight(LightIntensityMode.Reflected)
    brick.showValue("dark", sensors.color3.threshold(Light.Dark), 4)
    brick.showValue("bright", sensors.color3.threshold(Light.Bright), 5)
    forever(function ():
        brick.showValue("reflected light", sensors.color3.light(LightIntensityMode.Reflected), 1)
    )
'''




def inicio():
    while True:
        segue_linha()
        

motores = MoveTank(OUTPUT_A,OUTPUT_B)
garra = Motor(OUTPUT_C)

sensorEsq = ColorSensor(INPUT_3)
sensorDir = ColorSensor(INPUT_1)
ultrassom = UltrasonicSensor(INPUT_2)
sensor_esq_valores = []
sensor_dir_valores = []

inicio()
