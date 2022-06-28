#!/usr/bin/env python3
from ev3dev2.motor import *
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *
#from ev3dev.ev3 import *
from ev3dev2.sound import Sound
from ev3dev2.console import *
import sys



def vira_verde():
    #motores.on_for_seconds(SpeedPercent(-20), SpeedPercent(-20), 1.2)
    global verde_esq
    global verde
    valor_esq = sensorEsq.value()
    valor_dir = sensorDir.value()

    if (valor_esq < verde_esq): #esq ve verde
        Sound().beep()
        print("Verde esquerdo", file=sys.stderr)
        motores.on_for_seconds(SpeedPercent(-50),SpeedPercent(-50),0.3)
        motores.on_for_seconds(SpeedPercent(-10),SpeedPercent(-50),0.8) #vira esquerda
        valor_esq = sensorEsq.value()
        segue_linha()
    
    elif (valor_dir < verde): #dir ve verde
        Sound().beep()
        print("Verde esquerdo", file=sys.stderr)
        motores.on_for_seconds(SpeedPercent(-50),SpeedPercent(-50),0.4)
        motores.on_for_seconds(SpeedPercent(-50),SpeedPercent(-10),0.8) #vira direita
        valor_dir = sensorDir.value()
        segue_linha()
        #motores.on_for_seconds(SpeedPercent(-50),SpeedPercent(30),1) #dobra pra direita

def ambient_light_intensity(self):
        """
        A measurement of the ambient light intensity, as a percentage.
        """
        self._ensure_mode(self.MODE_AMBIENT)
        return self.value(0) * self._scale('AMBIENT')


def segue_linha():
    global preto
    global branco
    global branco_meio
    global verde_meio
    global objetivo_meio
    global vmenor
    global vmaior
    global verde_esq

    valor_esq = sensorEsq.value()
    valor_dir = sensorDir.value() 
    valor_meio = sensorMeio.value()

    #verde = 10 #12
    valor_frontal = sensorFrontal.value()

    if valor_frontal <= 200: #<= 100 no modo ambiente // no claro, o valor é 250
        #obstaculos()
        pass
        '''valor_frontal = sensorFrontal.value()'''
    
    if 116 < valor_esq < 180 and 71 < valor_dir < 104: #faixa de valores do vermelho as 14h
        funcao_resgate()

    if (valor_dir < verde) or (valor_esq < (verde_esq)): #um ou outro ve verde
        vira_verde()
    
    if (valor_meio < branco_meio): #sensor do meio vendo preto
        kp = 0.17 #0.2
        ki = 0.01
        erros = 0
        soma_erro = 0
        #Ki pequena, bem menor que kp. kd está entre kp e ki
        
        if valor_dir > preto and valor_esq > preto: #somente o do meio vendo preto
            erro = (objetivo_meio - valor_meio)
            soma_erro += erro

            kpErro = kp*erro
            kiSoma_erro = ki*soma_erro

            motores.on(SpeedPercent(kpErro + kiSoma_erro-20), SpeedPercent(-kpErro + kiSoma_erro-20))
            

        elif valor_esq < preto and valor_dir > preto: # esquerda e meio vendo preto    
            motores.on(SpeedPercent(vmenor),SpeedPercent(vmaior))
            while (valor_dir > preto): #enquanto o direito não ver preto       
                valor_dir = sensorDir.value()

        elif valor_esq > preto and valor_dir < preto: # direita e meio vendo preto
            #Sound().beep()
            motores.on(SpeedPercent(vmaior),SpeedPercent(vmenor))
            while (valor_esq > preto): #enquanto o esquerdo não ver preto
                    valor_esq = sensorEsq.value()
        
        else: #encruzilhada / todos vendo preto
            motores.on_for_seconds(SpeedPercent(-15),(-15), 1.5)
    
    else: #sensor do meio vendo branco
        if (valor_esq < preto) and (valor_dir > preto): #esquerdo ve preto e direito ve branco
            while (valor_meio > branco_meio): #enquanto o do meio não ver preto
                motores.on(SpeedPercent(vmenor), SpeedPercent(vmaior))
                valor_meio = sensorMeio.value()

        elif (valor_esq > preto) and (valor_dir < preto): #esquerdo ve branco e direito ve preto
            while (valor_meio > branco_meio):  #enquanto o do meio não ver preto
                motores.on(SpeedPercent(vmaior),SpeedPercent(vmenor))
                valor_meio = sensorMeio.value()
        else: #todos veem branco
            motores.on(SpeedPercent(-20),SpeedPercent(-20))

def obstaculos():    
    valor_esq = sensorEsq.value()
    valor_dir = sensorDir.value()
    valor_meio = sensorMeio.value()

    motores.on_for_seconds(SpeedPercent(20),SpeedPercent(20), 1) # ré
    motores.on_for_seconds(SpeedPercent(30), SpeedPercent(-30), 1.6)
    while(valor_meio > 300):
        motores.on(SpeedPercent(-75), SpeedPercent(-30))
        valor_meio = sensorMeio.value()

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
    garra.on_for_seconds(SpeedPercent(-20), 0.6) #0.8 // quanto tempo demora para abrir a garra


def levanta_garra():
    garra.on_for_seconds(SpeedPercent(15),1.2) #1.4
    garra.on_for_seconds(SpeedPercent(9), 0.9)

def movimento_estoque():
    estoque.on_for_seconds(SpeedPercent(-10), 0.55) #sobe
    time.sleep(5)
    estoque.on_for_seconds(SpeedPercent(20), 0.35) #desce
    time.sleep(10)

def funcao_estoque():

    motores.on_for_seconds(SpeedPercent(-35), SpeedPercent(35), 2)#giro 180°
    motores.on_for_seconds(SpeedPercent(10), SpeedPercent(10), 0.5)
    estoque.on_for_seconds(SpeedPercent(-10), 0.55)#sobe
    motores.on_for_seconds(SpeedPercent(100), SpeedPercent(100), 0.3)
    motores.on_for_seconds(SpeedPercent(-100), SpeedPercent(-100), 0.3)
    time.sleep(2)
    estoque.on_for_seconds(SpeedPercent(20), 0.35) #desce

    motores.on_for_seconds(SpeedPercent(35), SpeedPercent(-35), 1)#giro 90°


def funcao_resgate():
    global preto
    valor_esq = sensorEsq.value()
    valor_dir = sensorDir.value()
    valor_frontal = sensorFrontal.value()
    #vermelho esq 116-180, dir 71-104 as 14h
    parede_garra = 140 #nivel de luminosidade que o sensor do meio detecta na parede com a garra no meio. #330 as 14h, 380 as 15 500 as 16h
    normal_sem_garra = 120 #nivel de luminosidade que o sensor do meio detecta normalmente 530 as 14h, 600 as 16h, 122 as 18
    motores.off()
    abaixa_garra()
    #time.sleep(0.5)
    garra.off()
    time.sleep(0.001)
    while valor_frontal + 40 > (parede_garra + 10):
        motores.on(SpeedPercent(-35),SpeedPercent(-35))
        valor_frontal = sensorFrontal.value()
        if valor_esq < preto or valor_dir < preto:
            levanta_garra()
            funcao_estoque()
        
    motores.on_for_seconds(SpeedPercent(15),SpeedPercent(15),0.5)
    levanta_garra()
    time.sleep(0.2)
    if sensorFrontal.value() > normal_sem_garra - 50 + 80: # vendo parede
        motores.on_for_seconds(SpeedPercent(-30),SpeedPercent(30),1)# direita 90°
        funcao_resgate()
    else:
        Sound().beep()
        funcao_resgate()    
    '''
        motores.on(SpeedPercent(0),SpeedPercent(0))
    else:
        Sound().beep()'''
        

def funcao_garra():
    abaixa_garra()
    time.sleep(2)
    motores.on_for_seconds(SpeedPercent(-40), SpeedPercent(-40),2)
    levanta_garra()
    time.sleep(2)

def leitor_cor():
    print("SensorEsquerdo = ", sensorEsq.value()) #valores esq: branco (59) // preto (10) // verde (4 - 9)
    print("SensorDireito = ", sensorDir.value()) # valores dir: branco (70) // preto (7) // verde (4) // verde é menor que 6
def anda():
    motores.on(SpeedPercent(-30),SpeedPercent(-30))
    valor_esq = sensorEsq.value()
    valor_dir = sensorDir.value()
    print(valor_esq,valor_dir)
    if 116 < valor_esq < 180 and 71 < valor_dir < 104:
        Sound().beep()
        funcao_resgate()
    
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
    '''Sound().beep()
    time.sleep(5)
    Sound().beep()'''
    calibra_sensores()
    
    while True:  
        valor_frontal = sensorFrontal.value()     
        #sensorFrontal_valores.append(valor_frontal)

        anda()
        #motores.follow_line(kp = 0.6 , ki =1 , kd =1 , speed=SpeedPercent(30), 500, True, 600)
        
        
#Definição de motores e sensores

motores = MoveTank(OUTPUT_A,OUTPUT_B)
garra = Motor(OUTPUT_C)
estoque = Motor(OUTPUT_D)

sensorEsq = ColorSensor(INPUT_3)
sensorDir = ColorSensor(INPUT_1)
sensorMeio = LightSensor(INPUT_4)
sensorFrontal = LightSensor(INPUT_2)
#sensorFrontal = Sensor(INPUT_2)

#Definição de Listas

sensorEsq_valores = []
sensorDir_valores = []
sensorMeio_valores = []
sensorFrontal_valores = []
verdeEsq_valores = []
verdeDir_valores = []
pretoEsq_valores = []
pretoDir_valores = []

#Definição de variáveis

preto = 45
branco = 130 #160
branco_meio = 550 #600 às 16 e 18hrs // 550 às 14hrs // 500 às ??
objetivo_meio = 450 #450 às 14hrs e 16:30 // 500 às 16
verde_meio = 400
vmenor = 10 #42 #esses valores deixam a curv mais aberta, se a distância entre os valores for alta. O que é bom na curva do quadrado
vmaior = -35#valores: 35,-75 // 42 e -30 -> bom valor de agressividade = 60 e -60 // 70 e -70
verde = 16 #16 às 14hrs
verde_esq = verde + 12 #+ 6 + 2

inicio()
#valores_sCor(sensorEsq,sensorDir)
#calibra_sensores()
#calibra_verde()

#le 45 por segundo no branco

#quadrado -> dominancia de sensor (Esq,Dir,Esq)
#Triangulo -> dominancia de sensor (Esq)
