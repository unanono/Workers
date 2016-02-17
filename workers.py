#!/usr/bin/env python

import urllib2
from Queue import Queue
from multiprocessing import Process, Queue as MQ
from time import sleep
import sys
import random
#import httplib


#http_proxy = 'http://proxy:3128/'
#https_proxy = 'http://proxy:3128/'
#proxy_handler = urllib2.ProxyHandler({'https': https_proxy,
#                                      'http': http_proxy})
#opener = urllib2.build_opener(proxy_handler)
#urllib2.install_opener(opener)


class Worker(Process):
    '''Proceso que realiza la tarea pasada en el parametro task'''
    def __init__(self, task, colaentrada, colasalida):
        super(Worker, self).__init__()
        self.colaentrada = colaentrada
        self.colasalida = colasalida
        self.id = random.randint(0, 99)
        self.task = task

    def run(self):
        while 1:
            data = self.colaentrada.get()
            result = self.task(data)
            self.colasalida.put(result)
            sleep(0.1)


class WorkerManager():
    def __init__(self, workersn, task):
        self.workersn = workersn
        self.colaentrada = MQ()
        self.colasalida = MQ()
        self.outfile = sys.argv[1]
        self.workerslist = []
        self.task = task
        self.taskinqueue = Queue()
        #colaentrada.put(l)

    def prepare_workers(self):
        wl = self.workerslist
        t = self.task
        ci = self.colaentrada
        co = self.colasalida
        #Creo los workers, los arranco y los pongo en una lista
        for i in range(self.workersn):
            wi = Worker(t, ci, co)
            wi.start()
            wl.append(wi)

    def run(self):
        try:
            tq = self.taskinqueue
            ci = self.colaentrada
            while not tq.empty():
                #Saco los resultado de la cola de salida
                #ul = colasalida.get()
                #Pongo las tareas en la cola de los workers
                #para que la levante algun worker desocupado
                ci.put(tq.get())
        except KeyboardInterrupt as e:
            print e.message
            #of = file(outfile, 'w')
            #for l in links:
            #    if '?' in l:
            #        of.write(l + '\n')
            #of.close()

    def stop(self):
        #Paro cada worker y espero que termine
        wl = self.workerslist
        for wi in wl:
            wi.terminate()
            wi.join()


server = ''
maindomain = sys.argv[2]


if __name__ == '__main__':
    mp_main()
