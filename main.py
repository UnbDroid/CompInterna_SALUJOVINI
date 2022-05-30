#!/usr/bin/env python3
from ev3dev2.motor import *
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *
#from ev3dev.ev3 import *
from ev3dev2.console import *

def vira_verde(valor_esq,valor_dir,verde):
    motores.on_for_seconds(SpeedPercent(-20), SpeedPercent(-20), 1.2)
    if (valor_esq < verde): #esq ve verde
        motores.on_for_seconds(SpeedPercent(30),SpeedPercent(-50),1) #dobra pra esquerda
    elif (valor_dir < verde): #dir ve verde
        motores.on_for_seconds(SpeedPercent(-50),SpeedPercent(30),1) #dobra pra direita

def ambient_light_intensity(self):
        """
        A measurement of the ambient light intensity, as a percentage.
        """
        self._ensure_mode(self.MODE_AMBIENT)
        return self.value(0) * self._scale('AMBIENT')


def segue_linha(preto):
    verde = 18
    valor_frontal = sensorFrontal.value()
    sensorFrontal_valores.append(valor_frontal)

    ultimos_valores_frontal = sensorFrontal_valores[-10:]
    ultimos_valores_frontal.sort()
    if len(ultimos_valores_frontal) >= 10 and ultimos_valores_frontal[5] <= 30:
            obstaculos(preto)

    '''if valor_frontal <= 30:
        obstaculos(preto)'''
    valor_esq = sensorEsq.value()
    valor_dir = sensorDir.value()
    vmenor = 30
    vmaior = -50

    sensorDir_valores.append(valor_dir)
    sensorEsq_valores.append(valor_esq)

    if (valor_esq < verde) or (valor_dir < verde - 6): #sensor esquerdo ou direito vê o verde
        vira_verde(valor_esq,valor_dir,verde)

    elif (valor_esq < (preto - 5)) and (valor_dir < (preto + 5)): #ambos veem valor menor que preto
        if (sum(sensorEsq_valores[-90:])/90) <= (preto - 5): #se o esquerdo andou vendo muito preto -> vira pra direita (virada bruta)
            motores.on(SpeedPercent(vmaior),SpeedPercent(vmenor))
            time.sleep(0.4)
        elif (sum(sensorDir_valores[-90:])/90) <= (preto + 5): #se o direito andou vendo muito preto -> vira pra esquerda (virada bruta)
            motores.on(SpeedPercent(vmenor),SpeedPercent(vmaior))
            time.sleep(0.4)
        else: # dois pretos
            motores.on_for_seconds(SpeedPercent(0), SpeedPercent(0),1)
            motores.on_for_seconds(SpeedPercent(-20),SpeedPercent(-20),1)

    elif (valor_esq < preto) and (valor_dir > preto): #só esquerdo ve valor menor que preto -> dobra pra esquerda
        motores.on(SpeedPercent(vmenor),SpeedPercent(vmaior)) 

    elif (valor_esq > preto) and (valor_dir < preto): #só direito ve valor menor que preto -> dobra pra direita
        motores.on(SpeedPercent(vmaior),SpeedPercent(vmenor)) 

    else: #ambos veem valores maiores que preto (dois branco)
        motores.on(SpeedPercent(-20),SpeedPercent(-20))

def obstaculos(preto):    
    valor_ultrassom = ultrassom.value()
    valor_esq = sensorEsq.value()
    valor_dir = sensorDir.value()
    perto = 20
        
    motores.on_for_seconds(SpeedPercent(0),SpeedPercent(0),10) 

    '''motores.on_for_seconds(SpeedPercent(-50),SpeedPercent(30),1) #dobra pra direita

    while valor_ultrassom >= perto:
        motores.on(SpeedPercent(-20),SpeedPercent(-20))
    
    while valor_ultrassom <= perto:
        motores.on(SpeedPercent(-20),SpeedPercent(-20))

    motores.on_for_seconds(SpeedPercent(30),SpeedPercent(-50),1) #dobra pra esquerda

    while valor_ultrassom <= perto:
        motores.on(SpeedPercent(-20),SpeedPercent(-20))

    motores.on_for_seconds(SpeedPercent(30),SpeedPercent(-50),1) #dobra pra esquerda
    while valor_esq > preto and valor_dir > preto:
        motores.on(SpeedPercent(-20),SpeedPercent(-20))
    motores.on_for_seconds(SpeedPercent(-50),SpeedPercent(30),1) #dobra pra direita
    segue_linha()'''

def calibrate_white(self):
    (self.red_max, self.green_max, self.blue_max) = self.raw


def calibra_sensores():
    print('Comeco')
    time.sleep(10)
    ambient_light_intensity(sensorFrontal)
    calibrate_white(sensorEsq)
    calibrate_white(sensorDir)
    
def abaixa_garra():
    braco.on_for_seconds(SpeedPercent(-15), 0.4)
    braco.on_for_seconds(SpeedPercent(-9), 0.7)
    braco.on_for_seconds(SpeedPercent(-10), 1)#0.8
    time.sleep(2)

def levanta_garra():
    braco.on_for_seconds(SpeedPercent(15),1.4)
    #braco.on_for_seconds(SpeedPercent(9), 0.7)
    time.sleep(2)

def funcao_garra():
    abaixa_garra()
    tank_drive.on_for_seconds(SpeedPercent(-40), SpeedPercent(-40),2)
    levanta_garra()

def leitor_cor():
    print("SensorEsquerdo = ", sensorEsq.value()) #valores esq: branco (59) // preto (10) // verde (4 - 9)
    print("SensorDireito = ", sensorDir.value()) # valores dir: branco (70) // preto (7) // verde (4) // verde é menor que 6

def inicio():
    '''calibra_sensores()'''
    while True:
        segue_linha(preto)
        

motores = MoveTank(OUTPUT_A,OUTPUT_B)
garra = Motor(OUTPUT_C)

sensorEsq = ColorSensor(INPUT_3)
sensorDir = ColorSensor(INPUT_1)
ultrassom = UltrasonicSensor(INPUT_4)
sensorFrontal = LightSensor(INPUT_2)
sensorEsq_valores = []
sensorDir_valores = []
sensorFrontal_valores = []
preto = 45

inicio()
