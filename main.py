#!/usr/bin/env python3
from ev3dev2.motor import *
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *
#from ev3dev.ev3 import *
from ev3dev2.sound import Sound
from ev3dev2.console import *
import sys



def vira_verde(valor_esq,valor_dir,verde):
    motores.on_for_seconds(SpeedPercent(-20), SpeedPercent(-20), 1.2)
    print("Verde2", file=sys.stderr)

    '''valor_esq = sensorEsq.value()
    valor_dir = sensorDir.value() 
    verde_esq = 0
    verde_dir = 0

    if (valor_esq < verde):
        verde_esq = 1
        verde_dir = 0
    elif (valor_dir < verde):
        verde_esq = 0  
        verde_dir = 1

    while( (valor_esq != preto-5) and (valor_dir != preto-5)):         #enquanto os dois sensores não verem preto
        motores.on_for_seconds(SpeedPercent(-20), SpeedPercent(-20), 0.2)       #anda um pouco pra passsar do verde
        valor_esq = sensorEsq.value()
        valor_dir = sensorDir.value() 

    #vira conforme a cor
    if(verde_esq == 1):             #tem que virar pra esquerda
        motores.on_for_seconds(SpeedPercent(-10),SpeedPercent(-60),1) #esquerda

    if(verde_dir == 1):             #tem que virar pra direita
        motores.on_for_seconds(SpeedPercent(-60),SpeedPercent(-10),1) #direita'''
    
    valor_esq = sensorEsq.value()
    valor_dir = sensorDir.value()

    if (valor_esq < verde): #esq ve verde
        motores.on_for_seconds(SpeedPercent(-10),SpeedPercent(-60),1) #esquerda
        #motores.on_for_seconds(SpeedPercent(30),SpeedPercent(-50),1) #dobra pra esquerda
    elif (valor_dir < verde): #dir ve verde
        motores.on_for_seconds(SpeedPercent(-60),SpeedPercent(-10),1) #direita

        #motores.on_for_seconds(SpeedPercent(-50),SpeedPercent(30),1) #dobra pra direita

def ambient_light_intensity(self):
        """
        A measurement of the ambient light intensity, as a percentage.
        """
        self._ensure_mode(self.MODE_AMBIENT)
        return self.value(0) * self._scale('AMBIENT')


def segue_linha(preto):
    verde = 14
    branco = 200 #dentro da sala
    valor_frontal = sensorFrontal.value()

    if valor_frontal > 150: #<= 100 no modo ambiente               #no claro, o valor é 250
        obstaculos(preto)
        '''valor_frontal = sensorFrontal.value()'''
        
    valor_esq = sensorEsq.value()
    valor_dir = sensorDir.value() 
    vmenor = 100 
    vmaior = -100

    verde_esq = False
    verde_dir = False

    #bom valor de agressividade = 60 e -60 // 70 e -70

    sensorDir_valores.append(valor_dir)
    sensorEsq_valores.append(valor_esq)

    #print(valor_esq, file=sys.stderr)
    #print(sensorDir_valores, file=sys.stderr)

    if (valor_esq < verde) and valor_dir >= verde:
        Sound().beep()
        motores.on(SpeedPercent(vmaior),SpeedPercent(vmenor))
        verde_esq = True
    
    elif (valor_dir < verde) and valor_esq >= verde:
        Sound().beep()
        Sound().beep()
        motores.on(SpeedPercent(vmenor),SpeedPercent(vmaior))
        verde_dir = True

    elif (valor_esq < (preto - 5)) and (valor_dir < (preto + 5)): #ambos veem valor menor que preto
        ultimos_valoresEsq = sensorEsq_valores[-100:]
        ultimos_valoresDir = sensorDir_valores[-100:]
        ultimos_valoresEsq.sort()
        #print(ultimos_valoresEsq, file=sys.stderr)
        ultimos_valoresDir.sort()
            
        if len(ultimos_valoresEsq) > 100 and ultimos_valoresEsq[54] < branco: #se o esquerdo andou vendo muito preto -> vira pra esquerda
            motores.on(SpeedPercent(vmenor),SpeedPercent(vmaior))
            time.sleep(0.4)
            

        elif len(ultimos_valoresDir) > 100 and ultimos_valoresDir[54] < branco: #se o direito andou vendo muito preto -> vira pra direita (virada bruta)
            motores.on(SpeedPercent(vmaior),SpeedPercent(vmenor))
            time.sleep(0.4)

        else:
            if verde_esq == True:
                motores.on(SpeedPercent(vmenor),SpeedPercent(vmaior))
                verde_esq = False

            elif verde_dir == True:
                print("Beep", file=sys.stderr)
                motores.on(SpeedPercent(vmaior),SpeedPercent(vmenor))
                verde_dir = False

            else: # dois pretos
                motores.on_for_seconds(SpeedPercent(0), SpeedPercent(0),1)
                motores.on_for_seconds(SpeedPercent(-20),SpeedPercent(-20),1)

    elif (valor_esq < preto) and (valor_dir > preto): #só esquerdo ve valor menor que preto -> dobra pra esquerda
        motores.on(SpeedPercent(vmenor),SpeedPercent(vmaior)) 
        

    elif (valor_esq > preto) and (valor_dir < preto): #só direito ve valor menor que preto -> dobra pra direita
        motores.on(SpeedPercent(vmaior),SpeedPercent(vmenor)) 
        

    else: #ambos veem valores maiores que preto (dois branco)
        motores.on(SpeedPercent(-20),SpeedPercent(-20))
    
#    motores.on_for_seconds(SpeedPercent(-50), SpeedPercent(-50),0.2)


def obstaculos(preto):    
    valor_esq = sensorEsq.value()
    valor_dir = sensorDir.value()
    perto = 150

    motores.on_for_seconds(SpeedPercent(20),SpeedPercent(20), 1) # ré
    motores.on_for_seconds(SpeedPercent(30),SpeedPercent(-50),1.24) #dobra pra esquerda

    valor_ultrassom = ultrassom.value()
    if valor_ultrassom < 80:
        while valor_ultrassom < 80:
            motores.on(SpeedPercent(-50),SpeedPercent(-50))
            valor_ultrassom = ultrassom.value()
            Sound().beep()
    else:
        while valor_ultrassom >= 80:
            motores.on(SpeedPercent(-50),SpeedPercent(-50))
            valor_ultrassom = ultrassom.value()
            print(valor_ultrassom, file=sys.stderr)
        while valor_ultrassom < 80:
            motores.on(SpeedPercent(-50),SpeedPercent(-50))
            valor_ultrassom = ultrassom.value()
            print(valor_ultrassom, file=sys.stderr)

    motores.on_for_seconds(SpeedPercent(-50),SpeedPercent(10),1.6 ) #dobra pra direita

    valor_ultrassom = ultrassom.value()
    if valor_ultrassom < 100:
        while valor_ultrassom < 100:
            motores.on(SpeedPercent(-50),SpeedPercent(-50))
            valor_ultrassom = ultrassom.value()
            Sound().beep()
    else:
        while valor_ultrassom >= 100:
            motores.on(SpeedPercent(-50),SpeedPercent(-50))
            valor_ultrassom = ultrassom.value()
            print(valor_ultrassom, file=sys.stderr)
        while valor_ultrassom < 100:
            motores.on(SpeedPercent(-50),SpeedPercent(-50))
            valor_ultrassom = ultrassom.value()
            print(valor_ultrassom, file=sys.stderr)
    motores.on_for_seconds(SpeedPercent(-50),SpeedPercent(30),1.2) #dobra pra direita
    
    while valor_esq > preto and valor_dir > preto:
        motores.on(SpeedPercent(-20),SpeedPercent(-20)) #vai reto
        valor_esq = sensorEsq.value()
        valor_dir = sensorDir.value()

    motores.on_for_seconds(SpeedPercent(30),SpeedPercent(-50),1.2) #dobra pra esquerda'''
    
    valor_ultrassom = ultrassom.value()
    print(valor_ultrassom)

    valor_frontal = sensorFrontal.value()
    segue_linha(preto)
    

def calibrate_white(self):
    (self.red_max, self.green_max, self.blue_max) = self.raw


def calibra_sensores():
    print('Comeco')
    time.sleep(10)
    #ambient_light_intensity(sensorFrontal)
    calibrate_white(sensorEsq)
    calibrate_white(sensorDir)
    
    
def abaixa_garra():
    garra.on_for_seconds(SpeedPercent(-15), 0.4)
    garra.on_for_seconds(SpeedPercent(-9), 0.7)
    garra.on_for_seconds(SpeedPercent(-10), 0.8)#0.8
    time.sleep(2)

def levanta_garra():
    garra.on_for_seconds(SpeedPercent(15),1.4)
    #garra.on_for_seconds(SpeedPercent(9), 0.7)
    time.sleep(2)

def funcao_estoque():
    estoque.on_for_seconds(SpeedPercent(-10), 0.55) #sobe
    time.sleep(5)
    estoque.on_for_seconds(SpeedPercent(20), 0.35) #desce
    time.sleep(10)

def funcao_garra():
    abaixa_garra()
    motores.on_for_seconds(SpeedPercent(-40), SpeedPercent(-40),2)
    levanta_garra()

def leitor_cor():
    print("SensorEsquerdo = ", sensorEsq.value()) #valores esq: branco (59) // preto (10) // verde (4 - 9)
    print("SensorDireito = ", sensorDir.value()) # valores dir: branco (70) // preto (7) // verde (4) // verde é menor que 6

def valores_sCor(sensorEsq,sensorDir):
    i = 0
    
    while i < 5:
        motores.on(SpeedPercent(-50),SpeedPercent(-50))
        sensorDir_valores.append(sensorDir.value())
        sensorEsq_valores.append(sensorEsq.value())
        i += 1

    print(sensorDir_valores, file=sys.stderr)
    print(sensorEsq_valores, file=sys.stderr)

def inicio():
    '''valores_sCor(sensorEsq,sensorDir)'''
    #calibra_sensores()
    while True:   
        valor_frontal = sensorFrontal.value()     
        segue_linha(preto)
        
motores = MoveTank(OUTPUT_A,OUTPUT_B)
garra = Motor(OUTPUT_C)
estoque = Motor(OUTPUT_D)

sensorEsq = ColorSensor(INPUT_3)
sensorDir = ColorSensor(INPUT_1)
ultrassom = UltrasonicSensor(INPUT_4)
sensorFrontal = LightSensor(INPUT_2)
#sensorFrontal = Sensor(INPUT_2)
sensorEsq_valores = []
sensorDir_valores = []
sensorFrontal_valores = []

preto = 45

inicio()

#le 45 por segundo no branco
