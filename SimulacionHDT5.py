# -*- coding: cp1252 -*-
#Universidad del valle de Guatemala
#ADT- Hoja de trabajo 5
#Esteban Avalos, 15059
#Didier Salazar, 15487
#Simulacion de como una computadora procesa instrucciones, variando la cantidad de CPU, RAM y velocidad de procesamiento.
#Se tomo como refencia codigo de ejemplos publicados en blackboard.


import simpy
import random

def ejecutar(medio, lapso, ram, memory, instrucciones, velocidad):
    global time
    global timeAcum
    #Inicia la simulacion para el primer suceso, y así en paralelo con los siguientes procesos.
    yield medio.timeout(lapso)
    print('Tiempo actual: %f -- Ejecuta un proceso, se utiliza: %d de RAM.' % (medio.now, memory))
    actualTime = medio.now
    yield ram.get(memory)
    print('Tiempo actual: %f -- Instruccion en proceso de ejecucion, se esta utilizando: %d de RAM.' % (medio.now, memory))
    contador = 0
    while contador < instrucciones:
        with cpu.request() as solicitud:
            yield solicitud
            if(instrucciones-contador)>=velocidad:
                efectuar = velocidad
            else:
                efectuar = (instrucciones-contador)
            print"Tiempo actual: %f -- Instruccion en proceso de ejecucion, el cpu ejecutara %d instrucciones." % (medio.now,efectuar)
            yield medio.timeout(efectuar/velocidad)
            contador += efectuar
            print ("Tiempo actual: %f -- Instruccion en proceso de ejecucion, ejecutando..."% (medio.now))
        estado= random.randint(1,2)
        if estado == 1 and contador<instrucciones:
            with esperar.request() as solicitud2:
                yield solicitud2
                yield medio.timeout(1)
                print "Tiempo actual: %f -- Instruccion en proceso de ejecucion, se espera, las operaciones han sido finalizadas." % (medio.now)	
    yield ram.put(memory)
    print('Tiempo actual: %f --Instruccion procesada y ejecutada totalmente, queda %d de RAM'% (medio.now, memory))	
    timeAcum += (medio.now - actualTime)	
    time.append(medio.now - actualTime)
#Definicion de variables de la simulacion.
espacioRam = 100
velocidad = 3.0 
timeAcum = 0.00
procesos = 100
time = []
medio = simpy.Environment()
cpu = simpy.Resource (medio, capacity = 1)
ram = simpy.Container(medio, init=espacioRam, capacity = espacioRam)
esperar = simpy.Resource(medio, capacity=2)
		

#Semilla para calcular los numeros random.	
random.seed(2411)

#El intervalo es cambiado en este punto.
intervalo = 1
for i in range(procesos):
    lapso = random.expovariate(1.0/intervalo)
    memory = random.randint(1,10)
    instrucciones = random.randint(1,10)
    medio.process(ejecutar(medio, lapso, ram, memory, instrucciones, velocidad))	
medio.run()
#Se imprime el tiempo promedio de procesamiento y la desviacion estandar del mismo.
print "--------------------------"
promedio = (timeAcum/procesos)
print('El promedio de tiempo de ejecucion de los procesos es de: %f ----' % (promedio))
sumatoria =0
for x in time:
    sumatoria += (x-promedio) **2
	
desviacion= (sumatoria/(procesos-1))**0.5	
print "--------------------------"
print('La Desviacion Estandar del promedio de tiempo de ejecucion es de: %f' %(desviacion))
